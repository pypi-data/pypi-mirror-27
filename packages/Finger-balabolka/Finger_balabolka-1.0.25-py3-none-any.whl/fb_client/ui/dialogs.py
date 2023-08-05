import sys
from PyQt5 import QtWidgets, QtGui

from fb_client.accounts.account import UserManager
from fb_client.utils.utils import get_path

from .ui_files import enter_ui, help_ui, about_ui


class EnterDialog(QtWidgets.QDialog):
    '''Класс входа в чат'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = UserManager
        self.data = {}
        self.initUI()
        self.all_users = self.get_names()
        self.ui.comboBox.addItems(self.all_users)

    def initUI(self):
        self.ui = enter_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.register_btn)
        self.ui.pushButton_3.clicked.connect(self.enter_chat)
        self.ui.pushButton_2.clicked.connect(sys.exit)

    def get_names(self):
        '''Имена из БД'''
        users = self.user()
        users = users.get_users()
        all_users = [user.username for user in users]
        return all_users

    def register_btn(self):
        '''регистрация пользователя
            todo - проверка на существование!!!
        '''
        name, ok = QtWidgets.QInputDialog.getText(self, 'Новый пользователь', 'Имя(nickname):')
        if ok:
            # ничего уменее не пришло в голову((
            if len(name.split()) > 1:
                name = ''.join(name.split())
            user = self.user()
            username = user.create_user(name)
            self.all_users.append(username.username)
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(self.all_users)

    def enter_chat(self):
        user = self.user()
        user_obj = user.get_user(self.ui.comboBox.currentText())
        self.data["user"] = user_obj
        self.accept()


class HelpDialog(QtWidgets.QDialog):
    '''Помощь в чате'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.ui = help_ui.Ui_Dialog()
        self.ui.setupUi(self)


class AboutDialog(QtWidgets.QDialog):
    '''О программе'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.ui = about_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label_3.setPixmap(QtGui.QPixmap(get_path("icon.png")))
