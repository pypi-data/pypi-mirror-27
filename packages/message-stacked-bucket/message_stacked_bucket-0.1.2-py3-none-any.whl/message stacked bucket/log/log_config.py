# ○ Настройку логгера выполнить в отдельном модуле log_config.py: +
#   ● Создание именованного логгера. +
#   ● Сообщения лога должны иметь следующий формат: +
#   "<дата-время> <уровень_важности> <имя_модуля> <имя_функции> <сообщение>" +
#   ● Журналирование должно производиться в лог-файл. +
#   ● На стороне сервера необходимо настроить ежедневную ротацию лог-файлов +

import logging
from logging.handlers import TimedRotatingFileHandler


def set_logger(logger_name, log_level=logging.DEBUG):

    # ● Создание именованного логгера. +
    logger = logging.getLogger(logger_name)

    #   ● Сообщения лога должны иметь следующий формат: +
    #   "<дата-время> <уровень_важности> <имя_модуля> <имя_функции> <сообщение>" +
    log_format = logging.Formatter("%(asctime)s --- %(levelname)s --- %(module)s --- %(funcName)s --- %(message)s")

    #   ● Журналирование должно производиться в лог-файл. +
    if logger_name == 'server':
        #   ● На стороне сервера необходимо настроить ежедневную ротацию лог-файлов
        handler = TimedRotatingFileHandler('server.log', 'midnight', 1)
        handler.suffix = '%Y-%m-%d.log'
    else:
        handler = logging.FileHandler(logger_name + '.log')

    handler.setFormatter(log_format)
    logger.setLevel(log_level)
    logger.addHandler(handler)

