# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgChat(object):
    def setupUi(self, dlgChat):
        dlgChat.setObjectName("dlgChat")
        dlgChat.resize(400, 360)
        dlgChat.setBaseSize(QtCore.QSize(400, 280))
        dlgChat.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icons/chat1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgChat.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(dlgChat)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtChatMessages = QtWidgets.QTextEdit(dlgChat)
        self.txtChatMessages.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.txtChatMessages.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.txtChatMessages.setObjectName("txtChatMessages")
        self.verticalLayout.addWidget(self.txtChatMessages)
        self.toolbar = QtWidgets.QToolBar(dlgChat)
        self.verticalLayout.addWidget(self.toolbar)
        self.txtNewMessage = QtWidgets.QTextEdit(dlgChat)
        self.txtNewMessage.setMinimumSize(QtCore.QSize(0, 40))
        self.txtNewMessage.setMaximumSize(QtCore.QSize(16777215, 80))
        self.txtNewMessage.setFrameShape(QtWidgets.QFrame.HLine)
        self.txtNewMessage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.txtNewMessage.setLineWidth(1)
        self.txtNewMessage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtNewMessage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtNewMessage.setObjectName("txtNewMessage")
        self.verticalLayout.addWidget(self.txtNewMessage)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnSendMsg = QtWidgets.QPushButton(dlgChat)
        self.btnSendMsg.setMinimumSize(QtCore.QSize(0, 20))
        self.btnSendMsg.setMaximumSize(QtCore.QSize(16777215, 20))
        self.btnSendMsg.setAutoDefault(True)
        self.btnSendMsg.setDefault(True)
        self.btnSendMsg.setFlat(True)
        self.btnSendMsg.setObjectName("btnSendMsg")
        self.horizontalLayout.addWidget(self.btnSendMsg)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgChat)
        self.buttonBox.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonBox.setMaximumSize(QtCore.QSize(16777215, 20))
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(dlgChat)
        self.buttonBox.accepted.connect(dlgChat.accept)
        self.buttonBox.rejected.connect(dlgChat.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgChat)
        dlgChat.setTabOrder(self.txtNewMessage, self.btnSendMsg)
        dlgChat.setTabOrder(self.btnSendMsg, self.txtChatMessages)

    def retranslateUi(self, dlgChat):
        _translate = QtCore.QCoreApplication.translate
        self.btnSendMsg.setText(_translate("dlgChat", "Send"))

import client.resources_rc
