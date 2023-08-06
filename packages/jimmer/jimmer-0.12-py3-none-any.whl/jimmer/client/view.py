from PyQt5.QtWidgets import QMainWindow, QDialog, QDialogButtonBox, QAction, QToolButton, QMenu
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from client.models.ui.chat import Ui_dlgChat
from client.models.ui.login import Ui_dlgLogin
from client.models.ui.client import Ui_MainWindow

from os.path import join, abspath, isfile, isdir
from os import listdir


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)

        self.controller = controller

        self.btnConnect.clicked.connect(controller.connect_clicked)
        self.btnGetContacts.clicked.connect(controller.get_contacts)
        self.btnAdd.clicked.connect(controller.add_contact)
        self.btnDel.clicked.connect(controller.del_contact)
        self.btnChat.clicked.connect(controller.chat_clicked)
        self.lnContact.textEdited.connect(controller.defaults)
        self.lstContacts.clicked.connect(controller.contact_selected)
        self.lstContacts.doubleClicked.connect(controller.start_chat)

    def closeEvent(self, QCloseEvent):
        if self.controller.client.connected:
            self.controller.get_disconnected()


class ChatWindow(QDialog, Ui_dlgChat):
    def __init__(self, *args):
        self.controller, self.contact, _parent = args
        self.new_message = ''
        super().__init__(_parent)
        self.setupUi(self)
        # self.toolbar = QtWidgets.QToolBar(dlgChat)
        # self.verticalLayout.addWidget(self.toolbar)
        self.buttonBox.button(QDialogButtonBox.Close).setFlat(True)
        self.btnSendMsg.clicked.connect(self.message_ready)
        self.buttonBox.rejected.connect(self.close)

    def closeEvent(self, QCloseEvent):
        self.controller.end_chat(self.contact)

    def message_ready(self):
        self.controller.message_ready(self.contact)


class LoginWindow(QDialog, Ui_dlgLogin):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(controller.get_client)
        self.buttonBox.rejected.connect(self.parent().close)

    def closeEvent(self, QCloseEvent):
        self.parent().close()
