from sqlalchemy import Column, Integer, String, ForeignKey

from .settings import session, Base


class User(Base):
    '''Пользователи чата'''
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    avatar = Column(String)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User ('%s')>" % self.username

    def save(self):
        session.add(self)
        try:
            session.commit()
        except:
            session.rollback()


class ContactList(Base):
    '''Контакт лист'''
    __tablename__ = 'ContactList'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('User.id'))
    contact_id = Column(String)

    def save(self):
        session.add(self)
        try:
            session.commit()
        except:
            session.rollback()


class MessageHistory(Base):
    '''История'''
    __tablename__ = 'MessageHistory'
    history_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    message_to = Column(String)
    message_from = Column(String)
