import pytest
import sys
import socket


def get_user_msg(msg):
    ''' Получения сообщения от пользователя'''
    MESSAGE = {
        "action": "msg",
        "time": "timestamp",
        "to": "#all",
        "from": 'user',
        "message": msg,
    }
    return MESSAGE


def test_get_user_msg():
    msg = "test message"
    assert get_user_msg(msg) == {"action": "msg",
                                     "time": "timestamp",
                                     "to": "#all",
                                     "from": 'user',
                                     "message": msg,
                                     }
