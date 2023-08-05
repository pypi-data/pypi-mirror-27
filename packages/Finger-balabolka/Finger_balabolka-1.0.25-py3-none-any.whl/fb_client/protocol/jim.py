# Класссы реализации сообщений:
#    Message > JIM Сообщение​
#    Responce > JIM Ответ​

import json

from datetime import datetime


class Messages:
    '''Формирование сообщений по протоколу JIM'''
    time = datetime.now()

    def presence_msg(self, **kwargs):
        presence = {
            "action": "presence",
            "time":str(self.time),
            "type": "status",
            "user":{
                "account_name": kwargs.get('account_name',
                                           'Anonymous'),
                "status": "Yep, I am​ here!",
            }
        }
        return presence

    def get_user_msg(self, action, msg, **kwargs):
        ''' Получения сообщения от пользователя'''
        message = {
            "action": action,
            "time": str(self.time),
            "to": kwargs.get('to', '#all'),
            "from": kwargs.get('name', 'Anonymous'),
            "message": msg,
        }
        return message

    def action(self, **kwargs):
        '''Отправка простых действий:
           Покинуть комнату, по умолчанию выход'''
        action = {
            "action": kwargs.get("action", "quit"),
            "time": str(self.time),
            "from": kwargs.get("username", None),
            "room": kwargs.get("action", "main"),
        }
        return action

    def edit_contact(self, action, user, contact):
        ''' Получения сообщения от пользователя'''
        message = {
            "action": action,
            "time": str(self.time),
            "from": user,
            "contact": contact,
        }
        print('MESSAGE_LEVEL >> edit_msg >>', message)
        return message
