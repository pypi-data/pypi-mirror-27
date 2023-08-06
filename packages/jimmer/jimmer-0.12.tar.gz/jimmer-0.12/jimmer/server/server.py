import asyncio
import json
import logging

from config.config_common import is_chat
from config.config_common import DEFAULT_ADDRESS, DEFAULT_PORT
from config.config_common import MAX_DATA, REQUIRED_JIM_CLIENT_FIELDS
from config.config_common import ACT_PRESENCE, ACT_QUIT, ACT_MSG, ACT_JOIN, ACT_LEAVE
from config.config_common import ACT_GET_CONTACTS, ACT_ADD_CONTACT, ACT_DEL_CONTACT
from config.config_common import FIELD_ACTION, FIELD_RESPONSE, FIELD_QUANTITY, CODE_ACCEPTED
from config.config_common import FIELD_USER, FIELD_USERID, FIELD_CONTACT_NAME, FIELD_ROOM, FIELD_SENDER, FIELD_RECEIVER
from config.config_common import MSG_RECEIVE, MSG_SEND, SUCCESSFUL_MSG_KEY, UNSUCCESSFUL_MSG_KEY
from config.config_common import SERVER_CLIENT_RECV_SUCC_MSG, SERVER_CLIENT_RECV_UNSUCC_MSG
from config.config_common import SERVER_CLIENT_SEND_SUCC_MSG, SERVER_CLIENT_SEND_UNSUCC_MSG
from config.config_common import SERVER_START_SUCC_MSG
from protocol.protocol import JIMResponseMessage, JIMActionMessage, RESPONSE_OK
from server.storage import ServerStore, Client
from logging.handlers import TimedRotatingFileHandler
from os.path import join


class Server:
    connected_clients = {}

    def __init__(self, host=DEFAULT_ADDRESS, port=DEFAULT_PORT, log='server', loop=None):

        self.host = host
        self.port = port
        self.log = join('server', 'log', log)
        self.logger = logging.getLogger(__class__.__name__.lower())
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(name)s %(message)-s', level=logging.DEBUG,
            handlers=[TimedRotatingFileHandler(self.log, 'midnight')])

        self.log_messages = {
            self.handle.__name__: {
                MSG_RECEIVE: {
                    SUCCESSFUL_MSG_KEY: SERVER_CLIENT_RECV_SUCC_MSG,
                    UNSUCCESSFUL_MSG_KEY: SERVER_CLIENT_RECV_UNSUCC_MSG},
                MSG_SEND: {
                    SUCCESSFUL_MSG_KEY: SERVER_CLIENT_SEND_SUCC_MSG,
                    UNSUCCESSFUL_MSG_KEY: SERVER_CLIENT_SEND_UNSUCC_MSG},
            }
        }

        self._loop = loop or asyncio.get_event_loop()
        self._server = asyncio.start_server(self.handle, host=self.host, port=self.port)
        self.logger.debug(self.__init__.__name__)

    def start(self, and_loop=True):
        self._server = self._loop.run_until_complete(self._server)
        logging.info(SERVER_START_SUCC_MSG.format(self.start.__name__, self.host, self.port))
        print('Server started at {}:{}'.format(self.host, self.port))
        if and_loop:
            self._loop.run_forever()

    def stop(self, and_loop=True):
        self._server.close()
        if and_loop:
            self._loop.close()

    @asyncio.coroutine
    def handle(self, reader, writer):
        peer = writer.get_extra_info('peername')
        socket = writer.get_extra_info('socket')

        while not reader.at_eof():
            data = yield from reader.read(MAX_DATA)
            print('-->', data.decode())
            data = json.loads(data.decode())
            self.logger.debug(
                self.log_messages.get(self.handle.__name__).get(MSG_RECEIVE).get(SUCCESSFUL_MSG_KEY).format(
                    self.handle.__name__, *peer, data))

            if REQUIRED_JIM_CLIENT_FIELDS.issubset(data.keys()):
                for response in ServerResponse(data, peer, socket).results:
                    print('<--', response.as_dict)
                    writer.write(json.dumps(response.as_dict).encode())

                    self.logger.debug(
                        self.log_messages.get(self.handle.__name__).get(MSG_SEND).get(SUCCESSFUL_MSG_KEY).format(
                            self.handle.__name__, *peer, response.as_dict))

            else:
                writer.write(json.dumps(JIMResponseMessage(
                    {'response': 400, 'error': 'Wrong message format.'}).as_dict))


class ServerResponse:
    @staticmethod
    def get_presence(*args):
        _message, _address, _connection = args
        _client = Client(_message.get(FIELD_USER))
        Server.connected_clients.update({_client.clientName: _connection})
        with ServerStore() as store:
            if store.get_or_create(_client) and store.upd_history(_client, _address):
                return [RESPONSE_OK]

    @staticmethod
    def get_contacts(*args):
        _message, _address, _connection = args
        _response = []
        with ServerStore() as store:
            _contacts = store.get_contacts(Client(_message.get(FIELD_USERID)))

        if _contacts:
            _response = [JIMResponseMessage({FIELD_RESPONSE: CODE_ACCEPTED, FIELD_QUANTITY: len(_contacts)})]
            _response.extend(JIMActionMessage.contact_list(c) for c in _contacts)

        return _response

    @staticmethod
    def add_contact(*args):
        _message, _client, _connection = args
        with ServerStore() as store:
            _client = store.get_client(Client(_message.get(FIELD_USERID)))
            _contact = store.get_client(Client(_message.get(FIELD_CONTACT_NAME)))
            if _client and _contact:
                store.add_contact(_client, _contact)
                return [RESPONSE_OK]
            else:
                return [JIMResponseMessage({'response': 400, 'error': 'User not found.'})]

    @staticmethod
    def del_contact(*args):
        _message, _address, _connection = args
        with ServerStore() as store:
            _client = store.get_client(Client(_message.get(FIELD_USERID)))
            _contact = store.get_client(Client(_message.get(FIELD_CONTACT_NAME)))
            if _client and _contact:
                store.del_contact(_client, _contact)
                return [RESPONSE_OK]

    @staticmethod
    def join_chat(*args):
        _message, _address, _connection = args
        with ServerStore() as store:
            _client = store.get_client(Client(_message.get(FIELD_USERID)))
            _chat = store.get_or_create(Client(_message.get(FIELD_ROOM)))
            store.add_contact(_client, _chat)
            store.add_contact(_chat, _client)
            return [RESPONSE_OK]

    @staticmethod
    def leave_chat(*args):
        _message, _address, _connection = args
        with ServerStore() as store:
            _client = store.get_client(Client(_message.get(FIELD_USERID)))
            _chat = store.get_or_create(Client(_message.get(FIELD_ROOM)))
            store.del_contact(_chat, _client)
            return [RESPONSE_OK]

    @staticmethod
    def get_chat_message(*args):
        _message, _address, _connection = args
        _sender = _message.get(FIELD_SENDER)
        _receiver = _message.get(FIELD_RECEIVER)
        if not is_chat(_receiver):
            _msg_receiver = Server.connected_clients.get(_receiver)
            if _msg_receiver:
                print('-->', _message)
                _msg_receiver.sendall(json.dumps(_message).encode())
                return [RESPONSE_OK]
        else:
            with ServerStore() as store:
                _contacts = store.get_contacts(Client(_message.get(FIELD_RECEIVER)))

            if _contacts:
                _receivers = {k: v for k, v in Server.connected_clients.items() if k in _contacts and k != _sender}
                for r in _receivers.values():
                    print('-->', _message)
                    r.sendall(json.dumps(_message).encode())

                return [RESPONSE_OK]

    @staticmethod
    def quit(*args):
        _message, _address, _connection = args
        Server.connected_clients = {k: v for k, v in Server.connected_clients.items() if v != _connection}
        # _connection.close()
        print('Client {}:{} disconnected'.format(*_address))

        return [RESPONSE_OK]

    action_response = {
        ACT_PRESENCE: get_presence,
        ACT_QUIT: quit,
        ACT_ADD_CONTACT: add_contact,
        ACT_DEL_CONTACT: del_contact,
        ACT_GET_CONTACTS: get_contacts,
        ACT_MSG: get_chat_message,
        ACT_JOIN: join_chat,
        ACT_LEAVE: leave_chat,
    }

    def __init__(self, *args):
        self.message, self.client, self.sock = args
        self.results = self.action_response.get(self.message.get(FIELD_ACTION)).__func__(*args)


if __name__ == '__main__':
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
