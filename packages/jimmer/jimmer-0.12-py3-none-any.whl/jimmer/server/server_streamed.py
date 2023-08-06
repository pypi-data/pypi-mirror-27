import argparse
import json
import logging
import re
from logging.handlers import TimedRotatingFileHandler
from os.path import abspath, join
from queue import Queue
from socketserver import StreamRequestHandler, ThreadingTCPServer, TCPServer
from threading import Thread

from config.config_common import *
from protocol.protocol import JIMResponseMessage, JIMActionMessage, RESPONSE_OK
from server.storage import ServerStore, Client


server_log = join('server', 'log', 'server')
print(abspath(server_log))

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)-s', level=logging.DEBUG,
    handlers=[TimedRotatingFileHandler(server_log, 'midnight')])


class ServerHandler(StreamRequestHandler):
    connected_clients = {}

    def __init__(self, request, client_address, server):
        self.queue = Queue()
        self.data = {}
        self.response = None
        self.logger = logging.getLogger(Server.__name__.lower())

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

        StreamRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        _action = None
        while _action != ACT_QUIT:

            self.data = self.request.recv(MAX_DATA)

            if self.data:
                print('<---', self.data.decode())
                _js = json.loads(json.dumps(self.data.decode()))
                _js = re.sub('}{', '}|{', _js)
                _js = re.split('\|', _js)
                self.data = [json.loads(msg) for msg in _js]

                for message in self.data:
                    self.logger.debug(
                        self.log_messages.get(self.handle.__name__).get(MSG_RECEIVE).get(SUCCESSFUL_MSG_KEY).format(
                            self.handle.__name__, *self.client_address, message))

                    if REQUIRED_JIM_CLIENT_FIELDS.issubset(message.keys()):
                        for response in ServerResponse(message, self.client_address, self.connection).results:
                            print('--->', response.as_dict)
                            self.request.sendall(json.dumps(response.as_dict).encode())
                            self.logger.debug(
                                self.log_messages.get(self.handle.__name__).get(MSG_SEND).get(SUCCESSFUL_MSG_KEY).format(
                                    self.handle.__name__, *self.client_address, response.as_dict))

                        _action = message.get(FIELD_ACTION)

                    else:
                        self.response = JIMResponseMessage({'response': 400, 'error': 'Wrong message format.'}).as_dict

                self.data.clear()

            else:
                break
                # sleep(1)

        self.connected_clients = {k: v for k, v in self.connected_clients.items() if v != self.connection}
        self.connection.close()
        print('Client {}:{} disconnected'.format(*self.client_address))


class Server(ThreadingTCPServer, TCPServer):
    def __init__(self):

        self.log_messages = {
            self.serve_forever.__name__: {
                SUCCESSFUL_MSG_KEY: SERVER_START_SUCC_MSG,
                UNSUCCESSFUL_MSG_KEY: SERVER_START_UNSUCC_MSG},
            self.handle_request.__name__: {
                SUCCESSFUL_MSG_KEY: SERVER_WAITING_CONN_SUCC_MSG,
                UNSUCCESSFUL_MSG_KEY: SERVER_WAITING_CONN_UNSUCC_MSG},
            self.verify_request.__name__: {
                SUCCESSFUL_MSG_KEY: SERVER_CLIENT_CONNECTED_SUCC_MSG,
                UNSUCCESSFUL_MSG_KEY: SERVER_CLIENT_CONNECTED_UNSUCC_MSG},
            self.process_request.__name__: {
                SUCCESSFUL_MSG_KEY: SERVER_CLIENT_PROCCESSING_SUCC_MSG,
                UNSUCCESSFUL_MSG_KEY: SERVER_CLIENT_PROCCESSING_UNSUCC_MSG},
            self.finish_request.__name__: {
                SUCCESSFUL_MSG_KEY: SERVER_CLIENT_PROCCESSING_SUCC_MSG,
                UNSUCCESSFUL_MSG_KEY: SERVER_CLIENT_PROCCESSING_UNSUCC_MSG},
            self.close_request.__name__: {
                SUCCESSFUL_MSG_KEY: SERVER_CLIENT_CLOSEREQ_SUCC_MSG,
                UNSUCCESSFUL_MSG_KEY: SERVER_CLIENT_CLOSEREQ_UNSUCC_MSG},
            self.shutdown.__name__: {
                SUCCESSFUL_MSG_KEY: SERVER_STOP_SUCC_MSG,
                UNSUCCESSFUL_MSG_KEY: SERVER_STOP_UNSUCC_MSG},
        }

        self.logger = logging.getLogger(__class__.__name__.lower())
        self.name = __class__.__name__.lower()
        server_address = 'server_address'
        server_port = 'server_port'
        server_address_help = 'Server ip address. Optional.'
        server_port_help = 'Server port. Optional.'

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-a', type=str, dest=server_address, default=DEFAULT_ADDRESS, help=server_address_help)
        arg_parser.add_argument(
            '-p', type=str, dest=server_port, default=DEFAULT_PORT, help=server_port_help)

        try:
            self.server_address = arg_parser.parse_args().server_address
            self.server_port = arg_parser.parse_args().server_port
            self.server_address = (self.server_address, self.server_port)
        except SystemExit:
            self.server_address = DEFAULTS_ADDRESS_PORT

        TCPServer.__init__(self, server_address=DEFAULTS_ADDRESS_PORT, RequestHandlerClass=ServerHandler)
        self.logger.debug(self.__init__.__name__)


class ServerResponse(JIMResponseMessage):

    @staticmethod
    def get_presence(*args):
        _message, _address, _connection = args
        _client = Client(_message.get(FIELD_USER))
        ServerHandler.connected_clients.update({_client.clientName: _connection})
        with ServerStore() as store:
            if store.get_or_create(_client) and store.upd_history(_client, _address):
                return [RESPONSE_OK]

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
                return []

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
            _msg_receiver = ServerHandler.connected_clients.get(_receiver)
            if _msg_receiver:
                print('--->', _message)
                _msg_receiver.sendall(json.dumps(_message).encode())
                return [RESPONSE_OK]
        else:
            with ServerStore() as store:
                _contacts = store.get_contacts(Client(_message.get(FIELD_RECEIVER)))

            if _contacts:
                _receivers = {
                    k: v for k, v in ServerHandler.connected_clients.items() if k in _contacts and k != _sender}
                for r in _receivers.values():
                    print('--->', type(_message), _message)
                    r.sendall(json.dumps(_message).encode())

                return [RESPONSE_OK]

    @staticmethod
    def quit(*args):
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
        super().__init__(self.results)


def server_start():
    server = Server()
    thr = Thread(target=server.serve_forever)
    thr.setDaemon(True)
    thr.start()
    thr.join()


if __name__ == '__main__':
    server_start()
