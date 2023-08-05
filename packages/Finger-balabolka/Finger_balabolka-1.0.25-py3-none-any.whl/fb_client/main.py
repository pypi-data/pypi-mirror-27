#!/usr/bin/env python

# Клиент чата Finger balabolka

import sys
import socket

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSlot

from fb_client.core.client import Client
from fb_client.core.handlers import GuiReciever
from fb_client.utils.utils import get_params
from fb_client.ui.gui_class import UserGUI


params = get_params()
app = QtWidgets.QApplication(sys.argv)
client = Client(**params)
userGUI = UserGUI(client)
window = userGUI.get_chat()


@pyqtSlot(str)
def update_chat(data):
    ''' Отображение сообщения в чате
    '''
    try:
        msg = data
        window.append(msg)
    except Exception as e:
        print(e)


def main():
    '''основная функция - для .whl'''
    reciever = GuiReciever(client)
    reciever.gotData.connect(update_chat)
    th = QThread()
    reciever.moveToThread(th)
    th.started.connect(reciever.poll)
    th.start()
    userGUI.thread = th
    userGUI.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()