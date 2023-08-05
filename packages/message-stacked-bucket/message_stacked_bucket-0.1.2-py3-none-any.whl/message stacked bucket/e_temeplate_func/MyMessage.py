import json
import time

# JIM протокол
from d_jim.my_jim import MyJimMessage, MyJimResponse, MyJimOther


# Класс сообщение
class MyMessMessage:
    def __init__(self, **raw_message):
        # Не форматированное сообщение
        self.raw_message = raw_message

    # Умеет отправлять сообщения
    def mess_send(self, cur_socket):
        # Отправляем в класс JIM
        message = MyJimMessage(**self.raw_message, time=time.time())
        cur_socket.send(bytes(message))
        return message

    # Умеет отправлять респонсы
    def response_send(self, cur_socket):
        # Отправляем в класс JIM
        # TODO: тут проверки
        message = MyJimResponse(**self.raw_message, time='Time to kill!')
        cur_socket.send(bytes(message))
        return message

    def other_send(self, cur_socket):
        message = MyJimOther(**self.raw_message, time=time.time())
        cur_socket.send(bytes(message))
        return message

    # Умеет получать сообщения
    def mess_get(self, cur_socket):
        # Получает и сразу декодирует
        message = cur_socket.recv(1024)
        message = json.loads(message.decode('utf-8'))
        return message

    def __str__(self):
        return self.raw_message