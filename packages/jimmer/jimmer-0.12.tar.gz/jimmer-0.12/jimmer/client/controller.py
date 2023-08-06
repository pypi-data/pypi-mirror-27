from os import listdir
from os.path import abspath, join, isdir, isfile
from sys import argv, exit

from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMenu, QGridLayout, QToolButton, QAction
from PyQt5.QtGui import QIcon, QPixmap, QFont, QTextCursor

from client.client import Client
from client.storage import ClientStore
from client.view import MainWindow, ChatWindow, LoginWindow
from client.html_parser import HtmlToShortTag
from config.config_common import ACT_CONTACT_LIST, ACT_MSG, ACT_JOIN, ACT_LEAVE
from config.config_common import FIELD_ACTION, FIELD_USERID, FIELD_MESSAGE, FIELD_SENDER, FIELD_RECEIVER, FIELD_TIME
from config.config_common import CHAT_TITLE
from config.config_common import is_chat
from protocol.protocol import JIMActionMessage
from server.store import is_sqlite_db


class ClientGuiController:
    def __init__(self, client):

        self.actions_dict = {
            ACT_CONTACT_LIST: self.add_contact_item,
            ACT_MSG: self.update_chat
        }

        self.client = client
        self.client.add_observer(self)
        self.client_view = MainWindow(self)

        self.html_parser = HtmlToShortTag()
        self.chats = {}
        self.message_queue = {}
        self.login = None
        self.store = None
        self.chat = None
        self.sender = None
        self.receiver = None
        self.incoming_message = None

        self.client_view.show()
        self.start_login()

    def connect_clicked(self):
        if self.client.connected:
            self.get_disconnected()
        else:
            self.get_connected()

    def get_connected(self):
        try:
            if self.client.start_session():

                self.incoming_message = IncomingMessageThread(self.client)
                self.incoming_message.get_incoming.connect(self.get_incoming, Qt.QueuedConnection)
                self.incoming_message.start()

                self.client.outcoming_msg = JIMActionMessage.presence(self.client.as_dict).as_dict

                self.client_view.btnConnect.setText('Connected as \'{}\'.'.format(self.client.account_name))
                self.client_view.statusMessage.clearMessage()
                self.client_view.btnAdd.setEnabled(True)
                self.client_view.btnDel.setEnabled(True)
                self.client_view.btnGetContacts.setEnabled(True)
                self.client_view.btnChat.setEnabled(True)
                self.client_view.lstContacts.setEnabled(True)
                self.client_view.lnContact.setEnabled(True)
                self.get_contacts()

        except ConnectionError:
            self.client_view.statusMessage.showMessage(
                'Server {}:{} is unavailable'.format(self.client.server_address, self.client.server_port))

    def get_disconnected(self):
        for chat in self.chats.values():
            chat.close()
        self.client.outcoming_msg = JIMActionMessage.quit().as_dict
        self.client.end_session()
        self.client_view.btnConnect.setText('Disconnected. Click to connect')
        self.client_view.btnAdd.setEnabled(False)
        self.client_view.btnDel.setEnabled(False)
        self.client_view.lnContact.setEnabled(False)
        self.client_view.btnGetContacts.setEnabled(False)
        self.client_view.btnChat.setText('Chat')
        self.client_view.btnChat.setEnabled(False)
        self.client_view.lstContacts.clear()
        self.client_view.lstContacts.setEnabled(False)
        if self.incoming_message.isRunning():
            self.incoming_message.exit()

    def get_contacts(self):
        self.client_view.lstContacts.clear()
        with ClientStore(self.store) as store:
            store.clear_contacts()
        self.client.outcoming_msg = JIMActionMessage.get_contacts(self.client.account_name).as_dict

    def add_contact(self):
        _name = self.client_view.lnContact.text()
        if _name and not self.client_view.lstContacts.findItems(_name, Qt.MatchExactly) and not is_chat(_name):
            self.client.outcoming_msg = JIMActionMessage.add_contact(self.client.account_name, _name).as_dict
            self.client_view.lnContact.clear()
            self.add_contact_item(_name)
        elif _name and not self.client_view.lstContacts.findItems(_name, Qt.MatchExactly) and is_chat(_name):
            # self.client_view.statusMessage.showMessage('To join the chat, please click \'Join\'.'.format(_name), 2000)
            self.chat_clicked()
        elif _name:
            self.client_view.statusMessage.showMessage('\'{}\' already in contacts.'.format(_name), 2000)

    def del_contact(self):
        _name = self.client_view.lnContact.text()
        if _name:
            self.client.outcoming_msg = JIMActionMessage.del_contact(self.client.account_name, _name).as_dict
            self.client_view.lnContact.clear()
            self.del_contact_item()
            with ClientStore(self.store) as store:
                store.del_contact(_name)

    def add_contact_item(self, contact):
        _contact = None
        if isinstance(contact, dict):
            _contact = contact.get(FIELD_USERID)
        elif isinstance(contact, str):
            _contact = contact

        with ClientStore(self.store) as store:
            store.get_or_create_contact(_contact)

        self.client_view.lstContacts.addItem(_contact)
        # self.client_view.lstContacts.sortItems()

    def del_contact_item(self):
        self.client_view.lstContacts.takeItem(self.client_view.lstContacts.currentRow())

    def contact_selected(self):
        _text = self.client_view.lstContacts.currentItem().text()
        self.client_view.lnContact.setText(_text)
        if _text in self.chats:
            self.client_view.btnChat.setText(ACT_LEAVE.capitalize())
        else:
            self.client_view.btnChat.setText(ACT_JOIN.capitalize())

    def get_incoming(self, message):
        # print('-->', message)
        _action = message.get(FIELD_ACTION)
        if _action:
            self.actions_dict.get(_action)(message)

        _contact = message.get(FIELD_SENDER)
        if _contact:
            self.save_message(_contact, message.get(FIELD_MESSAGE), message.get(FIELD_TIME))

    def get_outcoming(self):
        if self.client.outcoming_msg:
            # print('<---', self.client.outcoming_msg)
            self.client.send_message(self.client.outcoming_msg)

            _contact = self.client.outcoming_msg.get(FIELD_RECEIVER)
            if _contact:
                self.save_message(
                    _contact, self.client.outcoming_msg.get(FIELD_MESSAGE), self.client.outcoming_msg.get(FIELD_TIME))

    def save_message(self, *args):
        with ClientStore(self.store) as store:
            store.add_message(args)

    def chat_clicked(self):
        _chat = self.client_view.lnContact.text()
        _chat_action = self.client_view.btnChat.text().lower()

        if _chat and not is_chat(_chat):
            self.client_view.statusMessage.showMessage('Selected contact is not chat.', 2000)
        elif _chat and _chat_action == ACT_JOIN:
            self.client_view.btnChat.setText(ACT_LEAVE.capitalize())
            self.start_chat()
        elif _chat and _chat_action == ACT_LEAVE:
            self.client_view.btnChat.setText(ACT_JOIN.capitalize())
            self.chats.get(_chat).close()

    def start_chat(self):
        self.sender = self.client.account_name
        self.receiver = self.client_view.lnContact.text()

        if self.receiver not in self.chats:

            if is_chat(self.receiver):
                self.client.outcoming_msg = JIMActionMessage.join_chat(self.client.account_name, self.receiver).as_dict
                if not self.client_view.lstContacts.findItems(self.receiver, Qt.MatchExactly):
                    self.add_contact_item(self.receiver)

            self.chat = ChatWindow(self, self.receiver, self.client_view)
            self.chat.setWindowTitle(CHAT_TITLE.format(self.sender, self.receiver))
            self.update_toolbar()
            self.chat.show()

            self.chats.update({self.receiver: self.chat})

            if self.message_queue.get(self.receiver):
                while self.message_queue.get(self.receiver):
                    self.update_chat(self.message_queue.get(self.receiver).pop(0))
                self.client_view.lstContacts.findItems(self.receiver, Qt.MatchExactly)[0].setBackground(Qt.transparent)

    def update_chat(self, *args):
        try:
            _chat, _message = args
        except ValueError:
            _message = args[0]

            if is_chat(_message.get(FIELD_RECEIVER)):
                _chat = self.chats.get(_message.get(FIELD_RECEIVER))
            else:
                _chat = self.chats.get(_message.get(FIELD_SENDER))

        if _chat:
            _chat.txtChatMessages.moveCursor(QTextCursor.End)

            if isinstance(_message, str):
                _chat.txtChatMessages.insertHtml(_message)
                _chat.txtChatMessages.insertHtml('<br />')
            elif isinstance(_message, dict):
                _chat.txtChatMessages.insertHtml(
                    '<b>{}:</b> {}'.format(_message.get(FIELD_SENDER), _message.get(FIELD_MESSAGE)))
                _chat.txtChatMessages.insertHtml('<br />')

        else:
            self.client_view.lstContacts.findItems(
                _message.get(FIELD_SENDER), Qt.MatchExactly)[0].setBackground(Qt.cyan)
            _contact = _message.get(FIELD_SENDER)
            if _contact not in self.message_queue:
                self.message_queue.update({_contact: []})
            self.message_queue.get(_contact).append(_message)

    def end_chat(self, chat):
        if is_chat(chat):
            self.client.outcoming_msg = JIMActionMessage.leave_chat(self.client.account_name, chat).as_dict
            self.client_view.btnChat.setText(ACT_JOIN.capitalize())
        self.chats = {k: v for k, v in self.chats.items() if k != chat}

    def message_ready(self, chat):
        _chat = self.chats.get(chat)
        self.html_parser.feed(_chat.txtNewMessage.toHtml())
        _message = self.html_parser.tagged_message
        if _message:
            _chat.txtNewMessage.clear()
            self.client.outcoming_msg = JIMActionMessage.to_user(self.sender, chat, _message).as_dict
            self.update_chat(_chat, '<b>You:</b> {}'.format(_message))

    def start_login(self):
        self.login = LoginWindow(self, self.client_view)
        self.login.show()

    def get_client(self):
        _client = self.login.lnLogin.text()
        self.store = join('client', 'db', '{}.client.sqlite'.format(_client))
        print(abspath(self.store), is_sqlite_db(self.store))
        if _client:
            self.client.account_name = _client
            self.get_connected()
        else:
            self.start_login()

    def exit(self):
        self.client_view.close()

    def defaults(self):
        self.client_view.btnChat.setText(ACT_JOIN.capitalize())

    def update_toolbar(self):
        iconTextBold = QIcon()
        iconTextBold.addPixmap(QPixmap(":/images/icons/b.jpg"), QIcon.Normal, QIcon.Off)
        iconTextItalic = QIcon()
        iconTextItalic.addPixmap(QPixmap(":/images/icons/i.jpg"), QIcon.Normal, QIcon.Off)
        iconTextUnderline = QIcon()
        iconTextUnderline.addPixmap(QPixmap(":/images/icons/u.jpg"), QIcon.Normal, QIcon.Off)
        self.chat.bold = QAction(iconTextBold, 'Bold', self.chat)
        self.chat.bold.setCheckable(True)
        self.chat.italic = QAction(iconTextItalic, 'Italic', self.chat)
        self.chat.italic.setCheckable(True)
        self.chat.underline = QAction(iconTextUnderline, 'Underline', self.chat)
        self.chat.underline.setCheckable(True)

        self.chat.bold.triggered.connect(self.set_text_format(self.chat.bold))
        self.chat.italic.triggered.connect(self.set_text_format(self.chat.italic))
        self.chat.underline.triggered.connect(self.set_text_format(self.chat.underline))

        smiles_icn = QIcon()
        smiles_icn.addPixmap(QPixmap(":/images/smiles/blum1.gif"))
        self.chat.smiles_btn = QToolButton()
        self.chat.smiles_btn.setIcon(smiles_icn)
        self.chat.smiles_btn.setMenu(self.get_smiles())
        self.chat.smiles_btn.clicked.connect(self.chat.smiles_btn.showMenu)

        self.chat.toolbar.addWidget(self.chat.smiles_btn)
        self.chat.toolbar.addAction(self.chat.bold)
        self.chat.toolbar.addAction(self.chat.italic)
        self.chat.toolbar.addAction(self.chat.underline)

    def get_smiles(self):
        smiles_folder = join('client', 'images', 'smiles')
        if isdir(smiles_folder):
            _smiles = [name for name in listdir(abspath(smiles_folder)) if isfile(join(smiles_folder, name))]
            _menu = QMenu()
            _layout = QGridLayout()
            _menu.setLayout(_layout)
            _count = 0
            for row in range(5):
                for column in range(5):
                    try:
                        _smile = join(smiles_folder, _smiles[_count])
                        _icon = QIcon(_smile)
                        _button = QToolButton(self.chat)
                        _button.setFixedSize(QSize(32, 32))
                        _button.setIcon(_icon)
                        _button.setIconSize(_button.size())
                        _button.setAutoRaise(True)
                        _button.setToolTip(_smiles[_count].split('.')[0])
                        _button.clicked.connect(self.insert_smile(_smile, _button.parent()))
                        _layout.addWidget(_button, row, column)
                        _count += 1

                    except IndexError:
                        break

            return _menu

        else:
            self.chat.smiles_btn.setEnabled(False)

    @staticmethod
    def insert_smile(smile, chat):
        def insert():
            chat.txtNewMessage.textCursor().insertImage(smile)
            chat.smiles_btn.menu().hide()
        return insert

    @staticmethod
    def set_text_format(button):
        def text_format():
            chat = button.parent()

            if button is chat.bold and chat.txtNewMessage.fontWeight() == QFont.Normal:
                chat.txtNewMessage.setFontWeight(QFont.Black)
            elif button is chat.bold and chat.txtNewMessage.fontWeight() == QFont.Black:
                chat.txtNewMessage.setFontWeight(QFont.Normal)
            elif button is chat.italic:
                chat.txtNewMessage.setFontItalic(not chat.txtNewMessage.fontItalic())
            elif button is chat.underline:
                chat.txtNewMessage.setFontUnderline(not chat.txtNewMessage.fontUnderline())

            if chat.txtNewMessage.textCursor().selectedText():
                button.setChecked(not button.isChecked())

        return text_format


class IncomingMessageThread(QThread):

    get_incoming = pyqtSignal(dict)

    def __init__(self, client):
        self.client = client
        super().__init__()

    def run(self):
        while True:
            _message = self.client.msg_queue.get()
            # print('-->', _message)
            self.get_incoming.emit(_message)

            if self.client.msg_queue.empty():
                self.client.msg_queue.task_done()


def main():
    client_app = QApplication(argv)
    ClientGuiController(Client())
    client_app.exec()


if __name__ == '__main__':
    exit(main())
