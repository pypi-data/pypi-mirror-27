import logging
import re
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from os.path import abspath, join

from config.config_common import *

SERVER_LOGGER_NAME = 'server'
CLIENT_LOGGER_NAME = 'client'
LOGS_DIR = join(CLIENT_LOGGER_NAME, 'log')
print(abspath(LOGS_DIR))
LEVEL_FIELD = 'level'
MESSAGE_FIELD = 'message'
NAME_FIELD = 'name'
MESSAGES = 'log_messages'
RE_MESSAGE = re.compile(r'\{(\w+)\}')

CLIENT_INIT_SUCC_MSG = 'Client started successfully.'
CLIENT_INIT_UNSUCC_MSG = 'Client start failure. Client was not started.'
CLIENT_CONN_SUCC_MSG = 'Successfully connected with server {server_address}:{server_port}.'
CLIENT_CONN_UNSUCC_MSG = 'Can not connect to server {server_address}:{server_port}.'
CLIENT_DISCONN_SUCC_MSG = 'Successfully disconnected from server {server_address}:{server_port}.'
CLIENT_DISCONN_UNSUCC_MSG = 'Connection closed by server or connection fails.'
CLIENT_SEND_MSG_SUCC = 'Message sent to server {server_address}:{server_port}.\n\t\t\t\t\t\tMessage data: {message_data}'
CLIENT_SEND_MSG_UNSUCC = 'Message \'{action}\' was not send to server {server_address}:{server_port}.'
CLIENT_RECV_MSG_SUCC = 'Message received from server {server_address}:{server_port}.\n\t\t\t\t\t\tMessage data: {incoming_msg}'
CLIENT_RECV_MSG_UNSUCC = 'No any data or incorrect data received from server {server_address}:{server_port} or connection fails.'

log_messages = {
    'client': {
        '__init__': {
            SUCCESSFUL_MSG_KEY: CLIENT_INIT_SUCC_MSG,
            UNSUCCESSFUL_MSG_KEY: CLIENT_INIT_UNSUCC_MSG},
        'start_session': {
            SUCCESSFUL_MSG_KEY: CLIENT_CONN_SUCC_MSG,
            UNSUCCESSFUL_MSG_KEY: CLIENT_CONN_UNSUCC_MSG},
        'end_session': {
            SUCCESSFUL_MSG_KEY: CLIENT_DISCONN_SUCC_MSG,
            UNSUCCESSFUL_MSG_KEY: CLIENT_DISCONN_UNSUCC_MSG},
        'send_message': {
            SUCCESSFUL_MSG_KEY: CLIENT_SEND_MSG_SUCC,
            UNSUCCESSFUL_MSG_KEY: CLIENT_SEND_MSG_UNSUCC},
        'receive_message': {
            SUCCESSFUL_MSG_KEY: CLIENT_RECV_MSG_SUCC,
            UNSUCCESSFUL_MSG_KEY: CLIENT_RECV_MSG_UNSUCC}},
}


class Log:

    handlers = {SERVER_LOGGER_NAME: [TimedRotatingFileHandler, 'midnight'],
                CLIENT_LOGGER_NAME: [logging.FileHandler, 'a']}

    def __init__(self, **kwargs):
        self.level = kwargs.get(LEVEL_FIELD)
        self.message = None

    def __call__(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            result = f(*args, **kwargs)

            if result is not False:
                self.message = log_messages.get(args[0].name).get(f.__name__).get(SUCCESSFUL_MSG_KEY)
            else:
                self.message = log_messages.get(args[0].name).get(f.__name__).get(UNSUCCESSFUL_MSG_KEY)

            logger = args[0].__getattribute__(NAME_FIELD)
            log_file = join(LOGS_DIR, logger)
            log_handler_params = Log.handlers.get(logger)[1]
            log_handler = Log.handlers.get(logger)[0](log_file, log_handler_params)

            logger = logging.getLogger(logger)
            logger.propagate = False
            log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)-s')
            log_handler.setFormatter(log_formatter)
            logger.addHandler(log_handler)
            logger.setLevel(logging.DEBUG)
            logger.log(self.level, f.__name__ + ' ' + self.message_format(self.message, args))
            logger.removeHandler(log_handler)

            return result
        return decorated

    def message_format(self, message, args):
        message_parameters = RE_MESSAGE.findall(message)
        message_parameters_dict = {}
        for parameter in message_parameters:
            try:
                setattr(self, parameter, args[0].__getattribute__(parameter))
            except AttributeError:
                # print(message, args)
                setattr(self, parameter, args[1])

            if parameter not in message_parameters_dict.keys():
                message_parameters_dict.update({parameter: None})
            message_parameters_dict.update({parameter: self.__getattribute__(parameter)})

        return message.format(**message_parameters_dict)
