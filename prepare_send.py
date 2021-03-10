from data2omni import Data2Omni
from omni_request import send_request
from db_request import request_new_issues_from_db


def prepare_and_send(email, api_token, subdomain):
    """
    Функция берет данные о новый заявках из БД (читает последнюю записанную в файл дату,
    и берет заявки, пришедшие после этой даты).

    Происходит цикл по записям, полученным в результате запроса к БД:
        Из каждой записи берется имя сотрудника, которому выпускается УНЭП, дата заявки.
        Также вызываются запросы к базам данных и берутся данные о сотруднике и кадровике для отправк в Омнидеск.
        Данные хранятся в экземпляре класса Data2Omni.

        С этими данными вызывается функция send_request(), которая отправит сообщение в Омнидеск.
        Если сообщение успешно отправлено, то дата этой заявки перезаписывается в файл.

    :param email: email админа Омнидеск
    :param api_token: api-token админа Омнидеск
    :param subdomain: Поддомен в Омнидеск
    :return:
    """
    rows = request_new_issues_from_db()
    if rows:
        for row in rows:
            data2omni = Data2Omni()
            data2omni.issue_request_date = row[0].strftime("%d.%m.%Y в %H:%M:%S")
            data2omni.person_name = row[1]
            data2omni.person_phone = row[2]
            data2omni.person_email = row[3]
            data2omni.company = row[4]

            isSent = send_request(data2omni, email, api_token, subdomain)
            if isSent:
                with open('last_nqes_date.txt', 'w') as f:
                    f.write(str(row[0]))
            else:
                break
