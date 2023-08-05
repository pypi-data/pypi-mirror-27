import sys
import json
import logging
import socket

from fb_client.utils import log_config


logger = logging.getLogger("client_log")


class Client():
    '''Клиент Finger Balabolka'''
    def __init__(self, **params):
        self.ip = params.get('ip', '127.0.0.1')
        self.port = params.get('port', 7777)
        self.conection = self.connect()

    def connect(self):
        '''Подключение к серверу'''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.ip, self.port))
        except ConnectionRefusedError:
            print("Сервер недоступен!")
            sys.exit(0)
        return sock

    def send_msg(self, msg):
        '''Отправка сообщения серверу'''
        msg_str = json.dumps(msg)
        self.conection.sendall(msg_str.encode('utf-8'))

    def get_msg(self):
        '''Ответ сервера и преобразоание в словарь'''
        msg = self.conection.recv(1024)
        msg = msg.decode("utf-8")
        try:
            msg = json.loads(msg)
        except json.decoder.JSONDecodeError as error:
            logger.warning('Ошибка данных: {}'.format(error))
            msg = {'alert': 'Ошибка'}
        return msg

    def get_msg_server(self, msg):
        '''Ответ сервера и преобразоание в словарь'''
        try:
            msg = json.loads(msg)
        except json.decoder.JSONDecodeError as error:
            logger.warning('Ошибка данных: {}'.format(error))
            msg = {'alert': 'Ошибка'}
        return msg
