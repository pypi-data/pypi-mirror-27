import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from fb_server.utils import log_config
from .settings import session, Base


logger = logging.getLogger("server_log")


class Client(Base):
    '''Пользователь'''
    __tablename__ = "Client"
    client_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    info = Column(String)

    def save(self):
        session.add(self)
        try:
            session.commit()
            logger.info('''новый клиент: {}
                        '''.format(self.username))
        except:
            session.rollback()
            logger.info('''Клиент: {}
                        '''.format(self.username))


class ClientHistory(Base):
    '''История пользолвателя'''
    __tablename__ = "ClientHistory"
    history_id = Column(Integer, primary_key=True)
    time_connect = Column(DateTime, default=datetime.utcnow)
    ipaddr = Column(String)
    client_id = Column(Integer, ForeignKey('Client.client_id'))

    def save(self):
        session.add(self)
        try:
            session.commit()
            logger.info('''Создана история: client_id:{}
                        '''.format(self.client_id))
        except Exception as err:
            session.rollback()
            logger.warning('Ошибка создания/изменения истории! {}'.format(err))


class ClientContacts(Base):
    '''Контакты пользователя'''
    __tablename__ = "ClientContacts"
    contacts_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('Client.client_id'))
    contact_id = Column(Integer, ForeignKey('Client.client_id'))

    def save(self):
        session.add(self)
        try:
            session.commit()
            logger.info('''Изменен контакт лист: client_id:{}
                        '''.format(self.client_id))
        except:
            session.rollback()
            logger.warning('Ошибка создания/изменения контакта!')

    def delete(self):
        session.delete(self)
        try:
            session.commit()
            logger.info('''Изменен контакт лист: client_id:{}
                        '''.format(self.client_id))
        except:
            session.rollback()
            logger.warning('Ошибка создания/изменения контакта!')
