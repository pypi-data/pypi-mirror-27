import logging

from hashlib import md5

from PIL import Image

from fb_client.utils import log_config
from fb_client.utils.utils import get_path
from .db.settings import session, Base, engine
from .db.models import User, ContactList


logger = logging.getLogger("client_log")
# Создаю таблицы - думаю есть место получше куда вставить
Base.metadata.create_all(engine)


class UserManager():
    '''Менежер пользователей'''

    def create_user(self, username):
        user = User(username.strip())
        user.save()
        return user

    def create_avatar(self, fname, user):
        '''создание аватарки из ранее загруженного файла
            TODO - "мусорные файлы!!! Остается мусор в виде старых аватарок"
        '''
        size = 200, 180
        avatar = Image.open(fname)
        avatar.thumbnail(size)
        filename = md5(fname.encode()).hexdigest()[-7:]
        avatar_path = get_path(filename + ".png")
        # Сохраняю файл на диск
        avatar.save(avatar_path, "PNG")
        # сохраняю путь в БД
        user.avatar = avatar_path
        user.save()

    def get_user(self, username):
        user = session.query(User).filter(User.username==username).first()
        return user

    def get_users(self):
        users = session.query(User).all()
        return users

class ContactManager():
    '''Менеджер контактов пользователя'''
    def add_contact(self, user_id, contact):
        contact = ContactList()
        contact.user_id = user_id
        contact.username = contact
        contact.save()

    def get_contact_list(self, contacts):
        ''' Получить контакт лист с сервера и сохранить в локальну БД
            За чем? Оверхед?
        '''
        pass