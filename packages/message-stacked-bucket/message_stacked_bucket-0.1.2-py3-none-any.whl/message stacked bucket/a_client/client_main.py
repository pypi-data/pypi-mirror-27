from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue

from e_temeplate_func.MyMessage import MyMessMessage
from a_client.db.client_db_def import ClientDbControl
from a_client.db.client_db_model import Base

from d_jim.my_jim_conf import MyJimOtherValue, MyJimActions, MyJimResponseCode


class MyMessClient:
    def __init__(self, name, addr='localhost', port=7777):
        self.name = name
        self.addr = addr
        self.port = port
        # JIM
        self.jim_other = MyJimOtherValue()
        self.actions = MyJimActions()
        self.codes = MyJimResponseCode()
        # Пресенс по дефолту
        self.presence = MyMessMessage(action=self.actions.PRESENCE, user={self.jim_other.ACCOUNT_NAME: self.name})
        # Подключиться
        self.socket = self.connect()

        # Создаём базу для клиента
        self.db = ClientDbControl('{}.db'.format(self.name), 'a_client/db', Base)
        # Сразу пишем туда подключившегося юзера
        self.add_to_client_db()

        # тут будет очередь
        self.request_queue = Queue()

        # Стартует GUI - пока не стартуем, только экземпяр хз для чего, но мб пригодится
        # self.gui = MyGui()
        '''
        self._gui_start() запустится после получения списка контактов - не запустится
        '''

    def connect(self):
        # Создать сокет TCP
        sct = socket(AF_INET, SOCK_STREAM)
        # Соединиться с сервером
        sct.connect((self.addr, self.port))
        # Отправляет пресенс
        # self.presence.mess_send(sock)
        self.presence.mess_send(sct)

        return sct

    def disconnect(self):
        # Отключаемся
        self.socket.close()

    # Запишет клиента в базу на клиенте?
    def add_to_client_db(self):
        self.db.add_user(self.name)
        self.db.commit()

    # Чтобы получать контакты
    def get_contacts(self):
        """Получить список контактов"""
        # формируем сообщение
        list_message = MyMessMessage(action=self.jim_other.GET_CONTACTS, user=self.name)
        # отправляем
        list_message.other_send(self.socket)
        # return {'user': 'MAX BLEAT', 'time': 'Time to kill!'}
        data = self.request_queue.get()
        return data

    def add_contact(self, new_name):
        add_contact = MyMessMessage(action=self.jim_other.ADD_CONTACT, user=self.name, contact_name=new_name)
        add_contact.other_send(self.socket)

    def del_contact(self, del_name):
        del_contact = MyMessMessage(action=self.jim_other.DEL_CONTACT, user=self.name, contact_name=del_name)
        del_contact.other_send(self.socket)

    def add_avatar(self, avatar_name, file):
        # Отправляем аватар на сервер, пока только имя
        add_avatar__to_server = MyMessMessage(action=self.actions.AVATAR, user=self.name,
                                              avatar={
                                                  self.jim_other.AVATAR_NAME: avatar_name,
                                                  self.jim_other.FILE_ACTION: self.jim_other.ADD
                                              })
        add_avatar__to_server.other_send(self.socket)

        # Пишем аватар в клиенте
        self.db.add_avatar(file)
        self.db.commit()

    def get_avatar(self):
        return self.db.get_avatar()

    def send_message(self, to_user_name, message_str):
        msg = MyMessMessage(action=self.actions.MSG, message=message_str, user={
            self.jim_other.FROM: self.name,
            self.jim_other.TO: to_user_name
        })
        # Отправляем на сервер
        msg.mess_send(self.socket)
