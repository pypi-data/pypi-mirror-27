# класс пользовательского интерфеса

import sys
from PyQt5 import QtWidgets, QtGui

from fb_client.accounts.account import UserManager
from fb_client.core.handlers import GuiReciever
from fb_client.protocol.jim import Messages
from fb_client.utils.utils import get_path

from .ui_files.client_ui import Ui_MainWindow
from .dialogs import EnterDialog, HelpDialog, AboutDialog
from .acc_settings import AccSetiingsDialog


class UserGUI(QtWidgets.QMainWindow):
    '''Класс графического интерфейса'''
    messages = Messages()

    def __init__(self, socket, parent=None):
        super().__init__()
        # иницилизация клиента
        self.user = None
        self.socket = socket
        self.thread = None
        self.contacts = []
        # Иконки для контактов
        self.icon_contact = QtGui.QIcon()
        self.icon_contact.addPixmap(QtGui.QPixmap(get_path("finger-man.png")),
                                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(get_path("icon.png")),
                                          QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.initUI()

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(self.icon)
        self.center()
        self.start_chat()
        self.set_avatar()
        # MENU
        self.ui.actionExit.triggered.connect(self.quit)
        self.ui.actionAccSet.triggered.connect(self.acc_settings)
        self.ui.actionHelp.triggered.connect(self.get_help)
        self.ui.actionAbout.triggered.connect(self.about)
        # Buttons and chatContacts
        self.ui.addButton.clicked.connect(self.add_contact)
        self.ui.delButton.clicked.connect(self.del_contact)
        self.ui.sendButton.clicked.connect(self.send)
        self.ui.chatText.returnPressed.connect(self.send)
        self.ui.contactListWidget.itemDoubleClicked.connect(self.add_privat)

    def center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
            (screen.height()-size.height())/2)

    def start_chat(self):
        ''' Вывод диалога входа, загрузка начальных параметров
            Контакт лист, имя и тд
        '''
        enter_dialog = EnterDialog(parent=self)
        enter = enter_dialog.exec()
        if enter == QtWidgets.QDialog.Accepted:
            data = enter_dialog.data
            self.user = data["user"]
            presence = self.messages.presence_msg(account_name=self.user.username)
            self.socket.send_msg(presence)
            data_msg = self.socket.get_msg()
            response = data_msg.get('alert', None)
            msg = """<p style="margin-top:0px; margin-bottom:0px;
                         margin-left:0px; margin-right:0px;
                        -qt-block-indent:0; text-indent:0px;">
                    <span style="color:red;">SERVER#</span>
                {}</p>""".format(response)
            #msg = "<SERVER> {}".format(response)
            #self.ui.chatWindow.append(msg)
            self.ui.chatWindow.insertHtml(msg)
            self.ui.username.setText(self.user.username)
            contacts = data_msg.get('contacts', None)
            if contacts:
                self.contacts = contacts
            self.get_contacts()

    def acc_settings(self):
        '''Параметры аккаунта'''
        user_manager = UserManager()
        acc = AccSetiingsDialog(self.user, parent=self)
        dialog = acc.exec()
        if dialog == QtWidgets.QDialog.Accepted:
            user_manager.create_avatar(acc.fname['fname'], self.user)
            self.set_avatar()

    def set_avatar(self):
        '''Уставить аватар'''
        if self.user.avatar is None:
            self.ui.avatar.setPixmap(QtGui.QPixmap(get_path("icon.png")))
        else:
            self.ui.avatar.setPixmap(QtGui.QPixmap(self.user.avatar))

    def get_help(self):
        '''Выводит диалог с описанием чата'''
        hd = HelpDialog(parent=self)
        hd.exec()

    def about(self):
        '''Выводит диалог с описанием программы'''
        ab = AboutDialog(parent=self)
        ab.exec()

    def get_chat(self):
        '''Метод для вызова в потоке'''
        return self.ui.chatWindow

    def get_contacts(self):
        '''Получить контакты'''
        self.ui.contactListWidget.clear()
        for contact in self.contacts:
            item = QtWidgets.QListWidgetItem()
            item.setIcon(self.icon_contact)
            item.setText(contact)
            self.ui.contactListWidget.addItem(item)

    def add_contact(self):
        '''добавление контакта'''
        contact_name, ok = QtWidgets.QInputDialog.getText(self,
                                                          'Новый контакт',
                                                          'Имя(nickname):')
        if ok:
            add_contact = self.messages.edit_contact('add',
                                                     self.user.username,
                                                     contact_name)
            self.socket.send_msg(add_contact)
            self.contacts.append(contact_name)
            self.get_contacts()

    def del_contact(self):
        '''удаление контакта'''
        item = self.ui.contactListWidget.currentIndex()
        contact_name = item.data()
        del_contact = self.messages.edit_contact('del',
                                                 self.user.username,
                                                 contact_name)
        self.socket.send_msg(del_contact)
        self.contacts.remove(contact_name)
        self.get_contacts()

    def add_privat(self):
        '''по двойному клику устанавливает команду на приватное сообщение'''
        name = self.ui.contactListWidget.currentIndex().data()
        self.ui.chatText.setStyleSheet('color: purple')
        msg = self.ui.chatText.setText('/ш {}'.format(name))

    def send(self):
        '''Отправка сообщения!'''
        # Нужно переделать с broadcast на '#all'!!!!!!!!!!
        action = 'broadcast'
        to = '#all'
        name=self.user.username
        msg = self.ui.chatText.text()
        if msg.startswith('/ш'):
            action = 'msg'
            line = msg.split()
            to = line[1]
            msg = ' '.join(line[2:])
        message = self.messages.get_user_msg(action, msg, to=to, name=name)
        self.socket.send_msg(message)
        show_msg = """<p><span style="color:green;">Вы#</span>
                        {}</p>""".format(msg)
        self.ui.chatWindow.append(show_msg)
        self.ui.chatText.clear()
        self.ui.chatText.setStyleSheet('color: black')

    def quit(self):
        '''посылает сообщение серверу об отключение клиента и выходит'''
        message = self.messages.action(username=self.user.username)
        self.socket.send_msg(message)
        if self.thread:
            self.thread.exit()
        self.close()
