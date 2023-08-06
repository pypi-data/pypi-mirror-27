import argparse
import json
import re
from logging import INFO
from socket import AF_INET, SOCK_STREAM
from socket import socket
from threading import Thread
from time import sleep
from queue import Queue

from config.config_common import DEFAULT_PORT, MAX_DATA
from config.log_config import Log


class Client:

    @property
    def as_dict(self):
        attrs_dict = {}
        for attr in self.__dict__:
            try:
                val = (getattr(self, attr))
                if attr not in attrs_dict.keys():
                    attrs_dict.update({attr: None})
                attrs_dict.update({attr: val})
            except AttributeError:
                pass
        return attrs_dict

    @Log(level=INFO)
    def __init__(self, account_name=None, password=None, status=None):
        self.name = __class__.__name__.lower()
        self.account_name = account_name
        self.password = password
        self.status = status
        self._outcoming_msg = {}
        self._observers = []
        self.msg_queue = Queue()
        self.connected = False
        self.tcp_socket = None
        self.receiver = None
        self.received_data = None
        self.sender = None

        server_address = 'server_address'
        server_port = 'server_port'
        server_address_help = 'Server ip address. Required.'
        server_port_help = 'Server port. Optional.'
        mode = 'mode'
        mode_help = 'Set client\'s mode for read/write.'

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(server_address, type=str, help=server_address_help)
        arg_parser.add_argument(server_port, type=int, nargs='?', default=DEFAULT_PORT, help=server_port_help)
        arg_parser.add_argument(mode, type=str, help=mode_help)

        # self.server_address = arg_parser.parse_args().server_address
        # self.server_port = arg_parser.parse_args().server_port
        # self.mode = arg_parser.parse_args().mode
        self.server_address = '127.0.0.1'
        self.server_port = 7777

    def __repr__(self):
        return self.account_name

    @property
    def outcoming_msg(self):
        return self._outcoming_msg

    @outcoming_msg.setter
    def outcoming_msg(self, data):
        self.outcoming_msg.clear()
        self.outcoming_msg.update(data)
        self.notify_outcoming()

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_outcoming(self):
        for observer in self._observers:
            observer.get_outcoming()

    @Log(level=INFO)
    def start_session(self, address=None):
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        if not address:
            address = (self.server_address, self.server_port)

            self.tcp_socket.connect(address)
            self.connected = True

            self.receiver = Thread(target=self.receive_message, daemon=True)
            self.receiver.start()

            return True

    @Log(level=INFO)
    def end_session(self):
        sleep(0.1)
        self.connected = False
        self.tcp_socket.close()

    @Log(level=INFO)
    def send_message(self, message):
        if self.tcp_socket.send(json.dumps(message).encode()):
            return True
        else:
            return False

    @Log(level=INFO)
    def receive_message(self):

        while self.connected:

            try:
                self.received_data = self.tcp_socket.recv(MAX_DATA)
                if self.received_data:
                    _json_string = json.loads(json.dumps(self.received_data.decode()))
                    for m in [json.loads(i) for i in re.findall(r'{[^{}]*}', _json_string)]:
                        self.msg_queue.put(m)

                else:
                    break

            except ConnectionError:
                break
