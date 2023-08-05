import os
import sys
import argparse


def get_params():
    '''параметры запуска клиента'''
    params ={}

    parser = argparse.ArgumentParser(description="Параметры для чат клиента")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-ip", type=str, default="127.0.0.1",
                       help="Задать IP адресс сервера, по умолчанию 127.0.0.1")
    parser.add_argument("-port", type=int, default=7777,
                        help="Установить PORT сервера, по умолчанию 7777")
    args = parser.parse_args()
    params['ip'] = args.ip
    params['port'] = args.port
    return params


def get_path(icon):
    path = os.path.join(
                os.path.dirname(
                   os.path.dirname(
                        os.path.abspath(__file__))), 'ui/img')
    path_icon = "{}/{}".format(path, icon)
    return path_icon