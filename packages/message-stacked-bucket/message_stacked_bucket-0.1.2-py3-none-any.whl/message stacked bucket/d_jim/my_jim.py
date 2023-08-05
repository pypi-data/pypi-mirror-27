import json
from .my_jim_conf import *
from .my_jim_errors import MandatoryKeyError, ResponseCodeError


class MyJim:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            # Формируем свойства нашего объекта динамически
            setattr(self, k, v)

    def __bytes__(self):
        # Преобразуем в json
        message_json = json.dumps(self.__dict__)
        # Преобразуем в байты
        message_bytes = message_json.encode(encoding='utf-8')
        # Возвращаем рузльтат
        return message_bytes

    @classmethod
    def create_from_bytes(cls, message_bytes):
        # Байты в json
        message_json = message_bytes.decode(encoding='utf-8')
        # json в словарь
        message_dict = json.loads(message_json)
        # создаем экземпляр нужного класса
        return cls(**message_dict)

    def __str__(self):
        return str(self.__dict__)


class MyJimMessage(MyJim):
    def __init__(self, **kwargs):
        fields = MyJimField().client_fields
        for rule in fields:
            if rule not in kwargs:
                raise MandatoryKeyError(rule)
        super().__init__(**kwargs)


class MyJimResponse(MyJim):
    def __init__(self, **kwargs):
        """Реализуем проверки для отевта сервера"""
        # Обязательные поля
        fields = MyJimField().server_fields
        # Возможные коды ответа
        codes = MyJimResponseCode().codes

        # Проверим наличие обязательных полей
        for rule in fields:
            if rule not in kwargs:
                raise MandatoryKeyError(rule)

        # Мы же точно знаем, что там будет response, если его там нет, то отработает первая ошибка
        code = int(kwargs['response'])
        # Проверим есть ли значение респонса в допустимых кодах
        if code not in codes:
            raise ResponseCodeError(code)

        super().__init__(**kwargs)


# Просто без всяких проверок, навсякий чтобы отсылать, если где-то глючит
class MyJimOther(MyJim):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



# message = b'{"response": "200", "alert": "Well done!"}'
# bjm = MyJimResponse.create_from_bytes(message)
# print(bjm)
