import abc
import asyncio
import logging

from ... import parse
from ..._util import obj_dict



logger = logging.getLogger(__name__)


class _Request:
    method = 'GET' or 'POST'
    _host = None # default to server host
    _server = None
    _client = None

    @abc.abstractmethod
    def _make_path(self, **kwargs):
        "generates the full HTTP request path"

    def _make_data(self, **kwargs):
        "generates the GET params or POST form data for the request"
        return None

    @abc.abstractmethod
    def _load(self):
        "loads response data into this object, and possibly also into the client db"

    __repr__ = obj_dict.repr

    @classmethod
    def request(cls, *a, **kw):
        return asyncio.ensure_future(cls.__request(*a, **kw))

    @classmethod
    async def __request(cls, client, server, **kwargs):
        self = cls(client, server, **kwargs)
        self.logger.info("%s %s...", self.method, self.url)
        await client._request_throttle.turn()
        self._text = await self._request()
        self.logger.debug("Importing data requested from %s...", self.url)
        self._load()
        self.logger.info("...finished loading %s.", self.url)
        return self

    def __init__(self, client, server, **kwargs):
        self.logger = logger.getChild(type(self).__name__)
        self._client = client
        self._server = server
        self.url = 'https://%s/%s' % (self._host or self._server.host, self._make_path(**kwargs))
        self._request_data = self._make_data(**kwargs)

    async def _request(self):
        if self.method == 'GET':
            request = self._client._web_session.get(self.url, params=self._request_data)
        elif self.method == 'POST':
            data = dict(self._request_data)
            if self._server:
                data.setdefault('fkey', (await self._server._fkey_request).fkey)
            request = self._client._web_session.post(self.url, data=data)
        else:
            raise ValueError('invalid .method')

        async with request as response:
            self.logger.debug("%s response from %s...", response.status, self.url)
            text = await response.text()
            self.logger.debug("...fully loaded")
            return text


class FKeyPage(_Request):
    def _load(self):
        self.data = parse.FKey(self._text)

        self.fkey = self.data.fkey


class StackChatFKey(FKeyPage):
    method = 'GET'

    def _make_path(self):
        return ''


class StackOverflowFKey(FKeyPage):
    method = 'GET'

    _host = 'stackoverflow.com'

    def _make_path(self):
        return 'users/login'


class MetaStackExchangeFKey(FKeyPage):
    method = 'GET'

    _host = 'meta.stackexchange.com'

    def _make_path(self):
        return 'users/login'


class StackSiteLogin(FKeyPage):
    method = 'POST'

    def _make_path(self, **kw):
        return 'users/login'

    def _make_data(self, fkey, email, password):
        return {
            'fkey': fkey,
            'email': email,
            'password': password
        }

    def _load(self):
        self.data = parse.ParseHTML(self._text)


class StackOverflowLogin(StackSiteLogin):
    _host = 'stackoverflow.com'


class MetaStackExchangeLogin(StackSiteLogin):
    _host = 'meta.stackexchange.com'


class RoomWSAuth(_Request):
    method = 'POST'

    def _make_path(self, room_id):
        return 'ws-auth'
    
    def _make_data(self, room_id):
        return {'roomid': room_id}

    def _load(self):
        self.data = parse.ParseJSON(self._text)



class RoomMessages(_Request):
    method = 'POST'

    def _make_path(self, room_id, before_message_id=None):
        self._room_id = room_id
        return 'chats/%s/events' % (room_id,)

    def _make_data(self, room_id, before_message_id=None):
        return {
            'mode': 'Messages',
            'msgCount': 500,
            'before': before_message_id or ''
        }

    def _load(self):
        self.data = parse.RoomMessages(self._text)

        self.logger.debug("Inserting RoomMessages data.")
        
        with self._client.sql_session() as sql:
            self.room = self._server._get_or_create_room(sql, self._room_id)
            self.messages = []

            for m in self.data._data['events']:
                if m['event_type'] == 1:
                    message = self._server._get_or_create_message(sql, m['message_id'])
                    message.mark_updated()

                    message.room_meta_id = self.room.meta_id
                    message.content_html = m.get('content', '')
                    message.parent_message_id = m.get('parent_message_id')
                    if message.parent_message_id:
                        parent = self._server._get_or_create_message(sql, message.parent_message_id)

                    if m.get('user_id'):
                        owner = self._server._get_or_create_user(sql, m['user_id'])
                        owner.mark_updated()

                        owner.name = m['user_name']
                        message.owner_meta_id = owner.meta_id
                    
                    self.messages.append(message)



class TranscriptDay(_Request):
    method = 'GET'

    def _make_path(
            self,
            room_id=None,
            message_id=None,
            date=None):
        target_room_id = room_id
        target_message_id = message_id
        target_date = date

        if message_id:
            if room_id:
                raise AttributeError("room_id not supported with message_id")
            if date:
                raise AttributeError("date not supported with message_id")
        elif not room_id:
            raise AttributeError("room_id xor message_id required")

        path = 'transcript'

        if target_message_id:
            path += '/message/%s' % (target_message_id)
        else:
            path += '/%s' % (target_room_id)
            if target_date:
                path += '/%s/%s/%s' % (
                    target_date.year, target_date.month, target_date.day)
            path += '/0-24'

        return path

    def _load(self):
        self.data = parse.TranscriptDay(self._text)

        self.logger.debug("Inserting TranscriptDay data.")

        with self._client.sql_session() as sql:
            self.room = self._server._get_or_create_room(sql, self.data.room_id)
            self.room.mark_updated()
            self.room.name = self.data.room_name

            self.messages = {}
            self.users = {}

            for m in self.data.messages:
                message = self._server._get_or_create_message(sql, m.id)
                message.mark_updated()
                message.content_html = m.content_html
                message.content_text = m.content_text
                message.room_meta_id = self.room.meta_id

                self.messages[m.id] = message

                if m.parent_message_id:
                    if m.parent_message_id in self.messages:
                        parent = self.messages[m.parent_message_id]
                    else:
                        parent = self._server._get_or_create_message(sql, m.parent_message_id)
                    message.parent_message_id = m.parent_message_id

                owner = self.users.get(m.owner_user_id)
                if not owner:
                    if m.owner_user_id:
                        owner = self._server._get_or_create_user(sql, m.owner_user_id)
                        if not owner.name:
                            owner.mark_updated()
                            # XXX: this is the name as of the time of the message, so it should really
                            # be treated as an update from that time, except that we don't have message
                            # timestamps implemented yet, so we'll just use the first name we see.
                            owner.name = m.owner_user_name
                    else:
                        # deleted owner, default to Community.
                        owner = self._server._get_or_create_user(sql, -1)
                    self.users[m.owner_user_id] = owner
                message.owner_meta_id = owner.meta_id


class UserInfo(_Request):
    def _make_path(
            self,
            user_id,
            rooms='current' or 'frequent'):
        return '/users/%s?tab=general&rooms=%s' % (user_id, rooms)

    _load = NotImplemented


class UserRecent(_Request):
    def _make_path(
            self,
            user_id,
            page=1 or int()):
        return '/users/%s?tab=recent&page=%s' % (user_id, page)

    _load = NotImplemented


class UserList(_Request):
    def _make_path(
            self,
            tab='all' or 'online' or 'active',
            sort='recent' or 'reputation' or 'activity',
            filter='',
            page=1):
        return '/users?tab=%s&sort=%s&filter=%s&pageSize=100&page=%s' % (tab, sort, filter, page)

    _load = NotImplemented


class RoomInfo(_Request):
    def _make_path(
            self,
            room_id,
            users='current' or 'frequent'):
        return '/rooms/info/%s?tab=general&users=%s' % (room_id, users)

    _load = NotImplemented


class RoomAccess(_Request):
    def _make_path(
            self,
            room_id):
        return '/rooms/info/%s?tab=access' % (room_id,)

    _load = NotImplemented


class RoomList(_Request):
    def _make_path(
            self,
            tab='all' or 'favorite' or 'events' or 'mine',
            sort='active' or 'event' or 'people' or 'created',
            filter='',
            page=1,
            nohide=True):
        return '/users?tab=%s&sort=%s&filter=%s&pageSize=100&page=%s&nohide=%s' % (tab, sort, filter, page, nohide)

    _load = NotImplemented


class MessageSearch(_Request):
    def _make_path(
            self,
            query,
            sort='newest' or 'relevance' or 'stars',
            room_id='',
            user_id='',
            page=1):
        return '/search?q=%s&Room=%s&User=%s&page=%s&pagesize=100&sort=%s' % (query, room_id, user_id, page, sort)

    _load = NotImplemented
