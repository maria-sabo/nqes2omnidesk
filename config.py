ssh_host_url = ""
ssh_path_to_key = ""
ssh_username = ""
ssh_port =

postgres_port = 5432


def foreign_db_params(db_name):
    """
    Функция возвращает параметры для подключения к БД.

    :param db_name: Название БД, к которой будет выполняться подключение
    :return: Словарь, содержащий параметры для подключения к БД
    """
    foreign_db_params_ = {
        'dbname': db_name,
        'user': "",
        'password': "",
        'host': 'localhost',
        'port':
    }
    return foreign_db_params_


# Настройки для Омнидеск
user_email_omni = "help@hr-link.ru"
user_full_name_omni = ""
