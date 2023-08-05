from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import func as sql_func

from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    UserId = Column(Integer, primary_key=True)
    Login = Column(String, unique=True)

    def __init__(self, login):
        self.Login = login

    def __repr__(self):
        return "<Contact ('%s')>" % self.Login

    def __eq__(self, other):
        return self.Login == other.Login


class Message(Base):
    __tablename__ = 'Message'
    MessageId = Column(Integer, primary_key=True)
    # Сюда будем писать кому было отправлено сообщение
    RelationId = Column(Integer, nullable=False)
    Text = Column(String)
    CreateData = Column(DateTime, server_default=sql_func.now())
    UserId = Column(Integer, ForeignKey('User.UserId'))

    User = relationship("User", back_populates="Messages")

    def __init__(self, text, user_id, created=None):
        self.Text = text
        self.UserId = user_id
        if created:
            self.CreateData = created

    def __repr__(self):
        return "<Message ('%s', %d)>" % (self.Text, self.UserId)

    def __eq__(self, other):
        return self.Text == other.Text and self.CreateData == other.CreateData and self.UserId == other.UserId


User.Messages = relationship("Message", order_by=Message.CreateData, back_populates="User")


class ClientAvatar(Base):
    __tablename__ = 'ClientAvatar'
    AvatarId = Column(Integer, primary_key=True)
    AvatarByte = Column(BLOB, nullable=False)

    def __init__(self, avatar_file):
        self.AvatarByte = avatar_file
