from PyQt5.QtCore import QObject, pyqtSignal

from e_temeplate_func.MyMessage import MyMessMessage
from d_jim.my_jim_conf import MyJimOtherValue, MyJimActions, MyJimResponseCode, MyJimField


class MyMessReceiver:
    # Получает сокет, получает очередь
    def __init__(self, sock, sock_in_queue):
        self.sock = sock
        self.sock_in_queue = sock_in_queue

        self.jim_other = MyJimOtherValue()
        self.actions = MyJimActions()
        self.codes = MyJimResponseCode()
        self.fields = MyJimField()
        self.is_alive = False

    def process_message(self, message):
        pass

    def poll(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            # Принимает сообщение от сервера по протоколу
            # data = self.sock.recv(1024)
            # print(data)
            listen_sct = MyMessMessage()
            response = listen_sct.mess_get(self.sock)
            if self.fields.RESPONSE in response:
                if response[self.fields.RESPONSE] == self.codes.OK:
                    print('Грит {} ---- Полный {}'.format(response[self.fields.RESPONSE], response))
                elif response[self.fields.RESPONSE] == self.codes.ACCEPTED:
                    print('Запрос успешен {}'.format(response))
                else:
                    print('Неверный код ответа от сервера')
            elif self.fields.ACTION in response:
                if response[self.fields.ACTION] == self.actions.MSG:
                        print('{} говорит --> {}'.format(
                            response[self.jim_other.USER][self.jim_other.FROM],
                            response[self.fields.MESSAGE])
                        )
                        self.process_message(response)
                elif response[self.fields.ACTION] == self.actions.RESPONSE:
                    self.sock_in_queue.put(response)


class MyGuiReceiver(MyMessReceiver, QObject):
    gotData = pyqtSignal(dict)

    def __init__(self, sock, request_queue):
        MyMessReceiver.__init__(self, sock, request_queue)
        QObject.__init__(self)

    def process_message(self, message):
        to_all = False
        text = message[self.fields.MESSAGE]
        user_from = message[self.jim_other.USER][self.jim_other.FROM]
        message = dict(text=text, user=user_from)
        self.gotData.emit(message)

    def poll(self):
        super().poll()

