import datetime as dt
from datetime import datetime

from db_connect import DbConnection


def get_last_nqes_date():
    """
    Функция возвращает дату, записанную в файл last_nqes_date.txt.

    :return:  Дата последней заявки, уведомление о которой, уже было отправлено в Омндеск
    """
    try:
        with open('last_nqes_date.txt') as f:
            first_line = f.readline()
            return first_line.rstrip()
    except FileNotFoundError:
        print('Файл не найден.')


def request_new_issues_from_db():
    """
    Функция подключается к БД zorro.
    Берет записанную в файл дату.
    Если дата является датой,
        то выполняется SQL-запрос, который выбирает записи о заявке УНЭП (заявка не в состоянии SUCCEEDED),
        которые имеют дату создания > записанной в файл.

    :return: Результат SQL-запроса
    Записи, имеющие столбцы:
    1. ФИО сотрудника, для которого создана заявка на выпуск УНЭП
    2. Телефон сотрудника, для которого создана заявка на выпуск УНЭП
    3. Email сотрудника, для которого создана заявка на выпуск УНЭП
    4. Компания сотрудника, для которого выпускается УНЭП
    """
    db_conn = DbConnection("zorro")
    curs = db_conn.curs
    last_nqes_date = get_last_nqes_date()
    try:
        tmp = datetime.strptime(last_nqes_date, "%Y-%m-%d %H:%M:%S.%f")
        db_conn.curs.execute(
            """
            SELECT
                concat(last_name, ' ', first_name, ' ', patronymic) as name, phone, email, a.name as company
            FROM nqes_issue_request JOIN person p ON nqes_issue_request.person_id = p.id
            JOIN arbitrator a ON nqes_issue_request.arbitrator_id = a.id
            WHERE state != 'SUCCEEDED' AND nqes_issue_request.created_date > %s
            ORDER BY nqes_issue_request.created_date
            """,
            (last_nqes_date,))
        db_response = curs.fetchall()
        if db_response:
            return db_response
        else:
            print(str(dt.datetime.now()) +
                  ' Все уведомления о новых заявках с текущей даты ' +
                  last_nqes_date +
                  ', записанной в файл last_nqes_date.txt, уже были отправлены в Омнидеск.')
    except ValueError:
        print('Введите корректную дату последней заявки в файл last_nqes_date.txt. '
              'Формат даты: YYYY-mm-dd HH:MM:SS.ffffff.')