from time import time

from config.config_common import *

# FORMAT_ = {FIELD_NAME: , FIELD_VALUE: , FIELD_TYPE: , FIELD_LENGTH: }

FORMAT_ACCOUNT_NAME = {FIELD_NAME: FIELD_ACCOUNT_NAME, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 24}
FORMAT_ACTION = {FIELD_NAME: FIELD_ACTION, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 15}
FORMAT_ALERT = {FIELD_NAME: FIELD_ALERT, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 128}
FORMAT_CHAT = {FIELD_NAME: FIELD_ROOM, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 25}
FORMAT_CONTACT_NAME = {FIELD_NAME: FIELD_CONTACT_NAME, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 24}
FORMAT_ENCODING = {FIELD_NAME: FIELD_ENCODING, FIELD_VALUE: 'utf-8', FIELD_TYPE: str, FIELD_LENGTH: 8}
FORMAT_ERROR = {FIELD_NAME: FIELD_ERROR, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 128}
FORMAT_MESSAGE = {FIELD_NAME: FIELD_MESSAGE, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 500}
FORMAT_TIME = {FIELD_NAME: FIELD_TIME, FIELD_VALUE: 20170101, FIELD_TYPE: int, FIELD_LENGTH: 10}
FORMAT_MSG_TYPE = {FIELD_NAME: FIELD_MSG_TYPE, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 15}
FORMAT_QUANTITY = {FIELD_NAME: FIELD_QUANTITY, FIELD_VALUE: 000, FIELD_TYPE: int, FIELD_LENGTH: 3}
FORMAT_RECEIVER = {FIELD_NAME: FIELD_RECEIVER, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 25}
FORMAT_RESPONSE = {FIELD_NAME: FIELD_RESPONSE, FIELD_VALUE: 000, FIELD_TYPE: int, FIELD_LENGTH: 3}
FORMAT_SENDER = {FIELD_NAME: FIELD_SENDER, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 25}
FORMAT_STATUS = {FIELD_NAME: FIELD_STATUS, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 128}
FORMAT_USER = {FIELD_NAME: FIELD_USER, FIELD_VALUE: '', FIELD_TYPE: dict, FIELD_LENGTH: 3}
FORMAT_USERID = {FIELD_NAME: FIELD_USERID, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 24}


class ProtocolDescriptor:

    def __init__(self, name, value, type_name, max_length):
        self.name = '_' + name
        self.type = type_name
        self.value = value
        self.max_length = max_length

    def __get__(self, instance, cls):
        return getattr(instance, self.name)

    def __set__(self, instance, value):

        if not isinstance(value, self.type):
            raise TypeError('{}{} should be \'{}\' type.'.format(
                instance.__class__.__name__, self.name, self.type.__name__))

        try:
            value_length = len(value)
        except TypeError:
            value_length = len(str(value))

        if value_length > self.max_length:
            raise ValueError('Length of {}{}={} should not exceed {} symbols.'.format(
                instance.__class__.__name__, self.name, value, self.max_length))

        setattr(instance, self.name, value)


class JIMActionMessage:

    action = ProtocolDescriptor(**FORMAT_ACTION)
    account_name = ProtocolDescriptor(**FORMAT_ACCOUNT_NAME)
    chat = ProtocolDescriptor(**FORMAT_CHAT)
    contact_name = ProtocolDescriptor(**FORMAT_CONTACT_NAME)
    encoding = ProtocolDescriptor(**FORMAT_ENCODING)
    message = ProtocolDescriptor(**FORMAT_MESSAGE)
    msgtime = ProtocolDescriptor(**FORMAT_TIME)
    msgtype = ProtocolDescriptor(**FORMAT_MSG_TYPE)
    receiver = ProtocolDescriptor(**FORMAT_RECEIVER)
    status = ProtocolDescriptor(**FORMAT_STATUS)
    sender = ProtocolDescriptor(**FORMAT_SENDER)
    user = ProtocolDescriptor(**FORMAT_USER)
    user_id = ProtocolDescriptor(**FORMAT_USERID)

    user_fields = [FIELD_ACCOUNT_NAME, FIELD_PASSWORD, FIELD_STATUS]

    __slots__ = {
        action.name, user.name, user_id.name, chat.name, msgtime.name, message.name, msgtype.name,
        account_name.name, contact_name.name, status.name, sender.name, receiver.name, encoding.name,
    }

    def __init__(self, **kwargs):
        self.msgtime = int(time())
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def as_dict(self):
        attrs_dict = {}
        for attr in self.__slots__:
            try:
                val = (getattr(self, attr))
                attr = attr.lstrip('_')
                if attr not in attrs_dict.keys():
                    attrs_dict.update({attr: None})
                attrs_dict.update({attr: val})
            except AttributeError:
                pass
        return attrs_dict

    @staticmethod
    def presence(user, msgtype='status'):
        user = {key: value for key, value in user.items() if key in JIMActionMessage.user_fields}
        return JIMActionMessage(action=ACT_PRESENCE, user=user, msgtype=msgtype)

    @staticmethod
    def authenticate(user):
        user = {key: value for key, value in user.items() if key in JIMActionMessage.user_fields}
        return JIMActionMessage(action=ACT_AUTHENTICATE, user=user)

    @staticmethod
    def get_contacts(user):
        return JIMActionMessage(action=ACT_GET_CONTACTS, user_id=user)

    @staticmethod
    def add_contact(user, contact):
        return JIMActionMessage(action=ACT_ADD_CONTACT, user_id=user, contact_name=contact)

    @staticmethod
    def del_contact(user, contact):
        return JIMActionMessage(action=ACT_DEL_CONTACT, user_id=user, contact_name=contact)

    @staticmethod
    def contact_list(user):
        return JIMActionMessage(action=ACT_CONTACT_LIST, user_id=user)

    @staticmethod
    def join_chat(user, chat):
        return JIMActionMessage(action=ACT_JOIN, user_id=user, chat=chat)

    @staticmethod
    def leave_chat(user, chat):
        return JIMActionMessage(action=ACT_LEAVE, user_id=user, chat=chat)

    @staticmethod
    def to_user(user, contact, message, encoding='utf-8'):
        return JIMActionMessage(action=ACT_MSG, sender=user, receiver=contact, message=message, encoding=encoding)

    @staticmethod
    def to_chat(user, contact, message):
        return JIMActionMessage(action=ACT_MSG, sender=user, receiver=contact, message=message)

    @staticmethod
    def probe():
        return JIMActionMessage(action=ACT_PROBE)

    @staticmethod
    def quit():
        return JIMActionMessage(action=ACT_QUIT)


class JIMResponseMessage:
    alert = ProtocolDescriptor(**FORMAT_ALERT)
    error = ProtocolDescriptor(**FORMAT_ERROR)
    quantity = ProtocolDescriptor(**FORMAT_QUANTITY)
    response = ProtocolDescriptor(**FORMAT_RESPONSE)
    response_time = ProtocolDescriptor(**FORMAT_TIME)

    __slots__ = {
        response.name, quantity.name, alert.name, error.name, response_time.name
    }

    def __init__(self, *args):
        if isinstance(args[0], list):
            pass
        elif isinstance(args[0], dict):
            for k, v in args[0].items():
                setattr(self, k, v)

    @property
    def as_dict(self):
        attrs_dict = {}
        for attr in self.__slots__:
            try:
                val = (getattr(self, attr))
                attr = attr.lstrip('_')
                if attr not in attrs_dict.keys():
                    attrs_dict.update({attr: None})
                attrs_dict.update({attr: val})
            except AttributeError:
                pass
        return attrs_dict


RESPONSE_OK = JIMResponseMessage({FIELD_RESPONSE: CODE_OK})


if __name__ == '__main__':
    user = {FIELD_ACCOUNT_NAME: 'NewUser', FIELD_STATUS: 'Hey, Im here!', FIELD_PASSWORD: 'userPwd'}
    user2 = {FIELD_ACCOUNT_NAME: 'NewUser2', FIELD_STATUS: 'Hey, Im here!', FIELD_PASSWORD: 'userPwd2'}
    print(JIMActionMessage.presence(user).as_dict)
    print(JIMActionMessage.authenticate(user).as_dict)
    print(JIMActionMessage.probe().as_dict)
    print(JIMActionMessage.quit().as_dict)
    RESPONSE_OK = JIMResponseMessage({FIELD_RESPONSE: CODE_OK})
    print(RESPONSE_OK.as_dict)
    print(JIMResponseMessage({FIELD_RESPONSE: 400, FIELD_ERROR: 'None'}).as_dict)
    print(JIMActionMessage.get_contacts(user[FIELD_ACCOUNT_NAME]).as_dict)
    print(JIMActionMessage.add_contact(user[FIELD_ACCOUNT_NAME], contact='newcontact').as_dict)
    print(JIMActionMessage.to_user(user.get(FIELD_ACCOUNT_NAME), user2.get(FIELD_ACCOUNT_NAME), 'Hey, Im here!').as_dict)
