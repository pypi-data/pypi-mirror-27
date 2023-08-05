from PyQt5 import QtWidgets, QtGui

from fb_client.utils.utils import get_path

from .ui_files import acc_set_ui


class AccSetiingsDialog(QtWidgets.QDialog):
    '''Класс входа в чат'''
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.initUI()
        self.user = user
        self.fname = {}

    def initUI(self):
        self.ui = acc_set_ui.Ui_Dialog()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(get_path("add_icon.png")),
                                     QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.addButton.setIcon(icon)
        self.ui.addButton.clicked.connect(self.add_avatar)

    def add_avatar(self):
        '''Создание аватарки'''
        fname = QtWidgets.QFileDialog.getOpenFileName(self,
                                                           'Open file',
                                                           '/home')[0]
        print(fname)

        pixmap = QtGui.QPixmap(fname)
        self.ui.load_avatar.setPixmap(pixmap)
        self.fname['fname'] = fname