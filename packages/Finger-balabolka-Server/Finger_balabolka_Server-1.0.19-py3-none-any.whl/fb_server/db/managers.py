import logging

from .settings import session, Base, engine
from .models import Client, ClientHistory, ClientContacts


logger = logging.getLogger("server_log")
# Создаю таблицы - думаю есть место получше куда вставить
Base.metadata.create_all(engine)


class ClientManager():
    '''Менежер пользователей'''
    client = Client

    def create_client(self, username, info=None):
        client = self.client()
        client.username = username.strip()
        client.info = info
        client.save()

    def get_client_id(self, username):
        client = session.query(self.client)
        client = client.filter(self.client.username==username).first()
        client_id = client.client_id if client else None
        return client_id


class ClientHistoryManager():
    '''Манеджер истории клиента'''
    history = ClientHistory

    def create_history(self, client_id, time, addr):
        history = self.history()
        history.time_connect = time
        history.ipaddr = addr
        history.client_id = client_id
        history.save()

    def get_history(self, client_id):
        '''получить экземпляр истории'''
        query = session.query(self.history)
        history = query.filter(self.history.client_id==client_id).first()
        return history


class ClientContactsManager():
    '''Менеджер контактов'''
    client = ClientManager()

    def get_contact(self, name, contact_name):
        contact = None
        client_id = self.client.get_client_id(name)
        contact_id = self.client.get_client_id(contact_name)
        query = session.query(ClientContacts)
        contact = query.filter((ClientContacts.client_id==client_id) &
                               (ClientContacts.contact_id==contact_id)).first()
        return contact

    def get_contacts(self, name):
        contacts_list = []
        client_id = self.client.get_client_id(name)
        query = session.query(ClientContacts)
        contacts = query.filter(ClientContacts.client_id==client_id).all()
        for contact in contacts:
            if contact.contact_id:
                query_name = session.query(Client)
                username = query_name.filter(
                                Client.client_id == contact.contact_id).first()
                contacts_list.append(username.username)
        return contacts_list


    def add_contact(self, name, contact):
        contacts = ClientContacts()
        client_id = self.client.get_client_id(name)
        contact_id = self.client.get_client_id(contact)
        contacts.client_id = client_id
        contacts.contact_id = contact_id
        contacts.save()

    def del_contact(self, name, contact):
        contact_del = self.get_contact(name, contact)
        try:
            contact_del.delete()
        except Exception as error:
            logger.warning('Ошибка удаления контакта: {}'.format(error))
