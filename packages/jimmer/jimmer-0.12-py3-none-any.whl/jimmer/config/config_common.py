# defaults
DEFAULT_ADDRESS = '127.0.0.1'
DEFAULT_PORT = 7777
DEFAULTS_ADDRESS_PORT = (DEFAULT_ADDRESS, DEFAULT_PORT)
MAX_CLIENTS = 10
MAX_DATA = 1024

# Help messages
SERVER_ADDRESS_HELP = 'Server ip address. Optional.'
SERVER_PORT_HELP = 'Server port. Optional.'

# Window titles
CHAT_TITLE = 'jimmer - {} in chat with {}'

# Server log messages format
SUCCESSFUL_MSG_KEY = 'successful'
UNSUCCESSFUL_MSG_KEY = 'unsuccessful'
MSG_RECEIVE = 'receive'
MSG_SEND = 'send'

SERVER_START_SUCC_MSG = '{}\t\t\tServer started successfully at {}:{}.'
SERVER_START_UNSUCC_MSG = '{}\t\tServer can not start at {}:{}.'
SERVER_STOP_SUCC_MSG = '{}\t\tServer stopped at {}:{}.'
SERVER_STOP_UNSUCC_MSG = '{} {} {}.'
SERVER_WAITING_CONN_SUCC_MSG = '{}\t\tServer waiting clients connections at {}:{}.'
SERVER_WAITING_CONN_UNSUCC_MSG = '{} {} {}'
SERVER_CLIENT_CONNECTED_SUCC_MSG = '{}\t\tClient connected {}:{}.'
SERVER_CLIENT_CONNECTED_UNSUCC_MSG = '{} {} {}'
SERVER_CLIENT_RECV_SUCC_MSG = '{}\t\tMessage received from client {}:{}.\n\t\t\t\t\t\tMessage: {}'
SERVER_CLIENT_RECV_UNSUCC_MSG = '{} {} {}'
SERVER_CLIENT_SEND_SUCC_MSG = '{}\t\tMessage sent to client {}:{}.\n\t\t\t\t\t\tMessage: {}'
SERVER_CLIENT_SEND_UNSUCC_MSG = '{}\t\t\t\tNo data received from client {}:{}. Or connection fails.'
SERVER_CLIENT_PROCCESSING_SUCC_MSG = '{}\t\tClient {}:{}'
SERVER_CLIENT_PROCCESSING_UNSUCC_MSG = '{} {} {}'
SERVER_CLIENT_CLOSEREQ_SUCC_MSG = '{}\t\tClient request closed {}:{}.'
SERVER_CLIENT_CLOSEREQ_UNSUCC_MSG = '{} {} {}'
SERVER_CLIENT_CONN_CLOSE_SUCC_MSG = '{}\t\tClient disconnected {}:{}.'
SERVER_CLIENT_CONN_CLOSE_UNSUCC_MSG = '{} {} {}'

# Message fields
FIELD_ACCOUNT_NAME = 'account_name'
FIELD_ACTION = 'action'
FIELD_ALERT = 'alert'
FIELD_ROOM = 'room'
FIELD_CONTACT_NAME = 'contact_name'
FIELD_ENCODING = 'encoding'
FIELD_ERROR = 'error'
FIELD_MESSAGE = 'message'
FIELD_MSG_TIME = 'time'
FIELD_MSG_TYPE = 'msgtype'
FIELD_PASSWORD = 'password'
FIELD_QUANTITY = 'quantity'
FIELD_RECEIVER = 'to'
FIELD_RESPONSE = 'response'
FIELD_SENDER = 'from'
FIELD_STATUS = 'status'
FIELD_TIME = 'time'
FIELD_USER = 'user'
FIELD_USERID = 'user_id'

# Protocol format fields
FIELD_NAME = 'name'
FIELD_VALUE = 'value'
FIELD_TYPE = 'type_name'
FIELD_LENGTH = 'max_length'

# Protocol actions
ACT_ADD_CONTACT = 'add_contact'
ACT_DEL_CONTACT = 'del_contact'
ACT_GET_CONTACTS = 'get_contacts'
ACT_CONTACT_LIST = 'contact_list'
ACT_AUTHENTICATE = 'authenticate'
ACT_JOIN = 'join'
ACT_LEAVE = 'leave'
ACT_MSG = 'msg'
ACT_PRESENCE = 'presence'
ACT_PROBE = 'probe'
ACT_QUIT = 'quit'

CODE_OK = 200
CODE_ACCEPTED = 202

REQUIRED_JIM_CLIENT_FIELDS = {FIELD_ACTION, FIELD_TIME}
REQUIRED_JIM_SERVER_FIELDS = {FIELD_RESPONSE}

CLIENT_ERROR = 'client_error'
CLIENT_ERROR_MSG = 'Wrong client message format!'

ANSWER_OK = 'OK'
ANSWER_WRONG_JSON = 'Wrong JSON'
ANSWERS_CODES = {ANSWER_OK: 200,
                 ANSWER_WRONG_JSON: 400}

SQLITE_HEADER_SIZE = 100
SQLITE_HEADER_STRING_LENGTH = 16
SQLITE_HEADER_DESCRIPTION = b'SQLite format 3\x00'
SERVER_DB = 'db/server.sqlite'
CLIENT_DB = 'db/client.sqlite'


def is_chat(arg):
    if arg.startswith('#'):
        return True
