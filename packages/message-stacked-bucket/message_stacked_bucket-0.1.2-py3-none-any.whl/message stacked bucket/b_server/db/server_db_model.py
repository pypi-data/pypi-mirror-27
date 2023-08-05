# Базы данных
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import func as sql_func

# ORM
from sqlalchemy.orm import relationship

Base = declarative_base()

'''Клиент'''
'''Контакты клиента'''
'''История клиента'''


class Client(Base):
    __tablename__ = 'Client'
    ClientId = Column(Integer, primary_key=True)
    Login = Column(String(64), nullable=False, unique=True)
    Info = Column(String, nullable=True)
    CreateData = Column(DateTime, server_default=sql_func.now())

    def __init__(self, login, info=None):
        self.Login = login
        if info:
            self.Info = info

    def __repr__(self):
        return "<User ('%s')>" % self.Login

    def __eq__(self, other):
        return self.Login == other.Login


# Связанные юзеры, аля список контактов
class ClientContact(Base):
    __tablename__ = 'ClientContact'
    ClientContactId = Column(Integer, primary_key=True)
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    ContactId = Column(Integer, ForeignKey('Client.ClientId'))

    def __init__(self, client_id, contact_id):
        self.ClientId = client_id
        self.ContactId = contact_id


class ClientHistory(Base):
    __tablename__ = 'ClientHistory'
    ClientHistoryId = Column(Integer, primary_key=True)
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))  # внешний ключ ключ
    Ip = Column(String(10), nullable=True)
    TimeLogin = Column(DateTime, server_default=sql_func.now(), nullable=False)
    CreateData = Column(DateTime, server_default=sql_func.now())

    Client = relationship("Client", back_populates="ClientHistories")

    def __init__(self, client_id, ip, created=None):
        self.Ip = ip
        self.ClientId = client_id
        if created:
            self.CreateData = created

    def __repr__(self):
        return "<ClientHistory ('%s', %d)>" % (self.Ip, self.ClientId)

    def __eq__(self, other):
        return self.Ip == other.Ip and self.CreateData == other.CreateData and self.ClientId == other.ClientId


Client.ClientHistories = relationship("ClientHistory", order_by=ClientHistory.CreateData, back_populates="Client")


class ClientAvatar(Base):
    __tablename__ = 'ClientAvatar'
    AvatarId = Column(Integer, primary_key=True)
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    AvatarName = Column(String(255), nullable=False)

    def __init__(self, avatar_name, client_id):
        self.AvatarName = avatar_name
        self.ClientId = client_id

    def __repr__(self):
        return "<ClientAvatar ('%s', %d)>" % (self.ClientId, self.AvatarName)

class MessagesHistory(Base):
    __tablename__ = 'MessagesHistory'
    MessageId = Column(Integer, primary_key=True)
    # Сюда будем писать кому было отправлено сообщение
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    ContactId = Column(Integer, ForeignKey('Client.ClientId'))
    Text = Column(String)
    CreateData = Column(DateTime, server_default=sql_func.now())

    # Client = relationship("Client", back_populates="Messages")

    def __init__(self, client_id, contact_id, text):
        self.ClientId = client_id
        self.ContactId = contact_id
        self.Text = text


# Client.Messages = relationship("MessagesHistory", order_by=MessagesHistory.CreateData, back_populates="Client")

