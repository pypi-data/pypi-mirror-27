"""Константы для работы JIM протокола"""


# Возможные ключи клиента
class MyJimActions:
    def __init__(self):
        # TODO дополнить. Возможные варианты - join, leave, probe (server)
        # Не уверен что стоит тут определять константы, в этом есть смысл?
        self.PRESENCE = 'presence'
        self.AUTH = 'authenticate'
        self.MSG = 'msg'
        self.QUIT = 'quit'
        self.RESPONSE = 'response'
        self.AVATAR = 'avatar'

    @property
    def actions(self):
        # Кортеж возможных действий
        # TODO дополнить. Возможные варианты - join, leave, probe (server)
        actions = (self.PRESENCE, self.MSG, self.AUTH, self.QUIT)
        return actions


# Обязательные поля клиента/севера
class MyJimField:
    def __init__(self):
        # TODO - user (account_name, status), type, to, from, encoding, message, room
        # Для клиента
        self.ACTION = 'action'

        # Для сервера
        self.RESPONSE = 'response'

        # Общие
        self.TIME = 'time'

        self.MESSAGE = 'message'

    # Обязательные поля для клиента
    @property
    def client_fields(self):
        return self.ACTION, self.TIME

    # Обязательные поля для сервера
    @property
    def server_fields(self):
        return self.RESPONSE,


# Возможные ключи/коды ответа сервера
class MyJimResponseCode:
    def __init__(self):
        # TODO есть ещё варианты кодов, но не ясно на сколько они вооще нужны
        # '100': 'Basic Notification', '101': 'Important Notification',
        # '200': 'OK', '201': 'Object Created', '202': 'Accepted',
        # '400': 'Malformed JSON', '401': 'Not Authorised', '402': 'Wrong Login/Password',
        # '403': 'Forbidden', '404': 'Not Found', '409': 'Connection Conflict',
        # '410': 'User Gone', '500': 'Server Error',
        self.BASIC_NOTICE = 100
        self.OK = 200
        self.ACCEPTED = 202
        self.WRONG_REQUEST = 400
        self.SERVER_ERROR = 500

    # Варианты ответа сервера
    @property
    def codes(self):
        return self.BASIC_NOTICE, self.OK, self.ACCEPTED, self.WRONG_REQUEST, self.SERVER_ERROR


class MyJimOtherValue:
    def __init__(self):
        self.USER = 'user'
        self.ACCOUNT_NAME = 'account_name'
        self.ADD_CONTACT = 'add_contact'
        self.DEL_CONTACT = 'del_contact'
        self.GET_CONTACTS = 'get_contacts'
        self.QUANTITY = 'quantity'
        self.TO = 'to'
        self.FROM = 'from'
        self.AVATAR_NAME = 'avatar_name'
        self.ADD = 'add'
        self.DEL = 'del'
        self.FILE_ACTION = 'file_action'
        self.CONTACT_NAME = 'contact_name'
