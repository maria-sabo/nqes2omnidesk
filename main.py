#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
import sshtunnel
import datetime as dt

import config
from prepare_send import prepare_and_send

ARGS_COUNT = 4


def main():
    """
    Если при запуске программы введены все требуемые аргумента,
        Происходит поделючение к серверу по SSH
        Вызывается основная функция подготовки и отправки полученных заявок prepare_and_send().

    sys.argv[0]: Аргумент командной строки, по умолчанию путь к скрипту main.py
    sys.argv[1]: Аргумент командной строки, строковое значение email-а админа
    sys.argv[2]: Аргумент командной строки, строковое значение api-токена админа
    sys.argv[3]: Аргумент командной строки, строковое значение поддомента в Омнидеск (например, hr-link)
    :return:
    """
    if sys.argv.__len__() == ARGS_COUNT:
        email = sys.argv[1]
        api_token = sys.argv[2]
        subdomain = sys.argv[3]

        with sshtunnel.SSHTunnelForwarder(
                (config.ssh_host_url, config.ssh_port),
                ssh_private_key=config.ssh_path_to_key,
                ssh_username=config.ssh_username,
                remote_bind_address=('localhost', config.postgres_port),
                local_bind_address=('localhost', config.ssh_port)) as server:
            server.start()
            logging.basicConfig(filename='app.log', level=logging.INFO,
                                format='INFO: ' + str(dt.datetime.now()) + '%(message)s')
            prepare_and_send(email, api_token, subdomain)
    else:
        print(
            'Введите четыре аргумента: \n - путь к запускаемому файлу (main.py) \n - email админа Омнидеск'
            '\n - api-токен админа \n - поддомен в Омнидеск')


if __name__ == '__main__':
    main()
