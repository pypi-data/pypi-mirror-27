import json
import logging

from datetime import datetime

from fb_server.utils import log_config
from fb_server.protocol.msg_handler import MessageHandler
from fb_server.db.managers import (ClientManager, ClientHistoryManager,
                         ClientContactsManager)

logger = logging.getLogger("server_log")


class JimHandler:
    ''' Формирование ответов по протоколу JIM
        Сохранение в БД данных
    '''
    message = MessageHandler()
    db_client = ClientManager()
    db_history = ClientHistoryManager()
    db_contacts = ClientContactsManager()

    def create_msg(self, msg):
        msg = json.dumps(msg)
        return msg.encode('utf-8')

    def presence(self, msg, addr):
        '''Ответ на присутсиве'''
        username = msg['user']['account_name']
        client_id = self.db_client.get_client_id(username)
        if client_id is None:
            client_id = self.db_client.create_client(username, 'JUST TEST')
        # Контакты клиента
        contacts_list = self.db_contacts.get_contacts(username)
        # История клиента
        self.db_history.create_history(client_id, msg['time'], addr[0])
        history = self.db_history.get_history(client_id)
        message = self.message.presence(contacts_list)
        return username, message

    def msg(self, msg):
        return self.create_msg(self.message.msg(msg))

    def get_contacts(self, message):
        contacts_list = self.db_contacts.get_contacts(message['from'])
        message = self.message.response(200, msg=message['message'],
                                        contacts=contacts_list)
        return message

    def add_contact(self, msg):
        '''Добавление контакта
            TODO > Уведомление!
        '''
        self.db_contacts.add_contact(msg['from'], msg['contact'])
        message = self.message.response(200, msg="Добавлен")
        return message

    def del_contact(self, msg):
        '''Добавление контакта
            TODO > Уведомление!
        '''
        self.db_contacts.del_contact(msg['from'], msg['contact'])
        message = self.message.response(200, msg="Удален")
        return message


def load_msg(data):
    data = data.decode("utf-8")
    if data == '':
        return
    try:
        data = json.loads(data)
        data['time'] = datetime.strptime(data['time'],
                                         "%Y-%m-%d %H:%M:%S.%f")
    except json.decoder.JSONDecodeError as error:
        logger.warning('Ошибка данных: {}'.format(error))
        data = None
    return data


jim_handler = JimHandler()

def presence(connection, message, addr):
    '''Ответ на присутсиве'''
    presence = jim_handler.presence(message, addr)
    msg = jim_handler.create_msg(presence[1])
    connection.send(msg)
    return presence[0]

def send_contacts(*args):
    message = args[0]
    connection = args[2]
    contacts = jim_handler.get_contacts(message)
    msg = jim_handler.create_msg(contacts)
    connection.send(msg)

def add_contact(*args):
    ''' Добавление контакта
        TODO: Отправка уведомления
    '''
    message = args[0]
    connection = args[2]
    msg = jim_handler.add_contact(message)
    msg = jim_handler.create_msg(msg)
    connection.send(msg)

def del_contact(*args):
    ''' Удаление контакта
        TODO: Отправка уведомления
    '''
    message = args[0]
    connection = args[2]
    print("del_contact >> ", message)
    msg = jim_handler.del_contact(message)
    msg = jim_handler.create_msg(msg)
    connection.send(msg)

def to_contact(*args):
    message = args[0]
    connection = args[2]
    accounts = args[3]
    msg = jim_handler.msg(message)
    try:
        accounts[message['to']].send(msg)
    except Exception as e:
        logger.warning('Не возможна Отправка: {}'.format(e))
        msg = jim_handler.msg({'message':'Ошибка!'})
        connection.send(msg)

def broadcast(*args):
    '''Общий чат'''
    to_del = []
    message = args[0]
    clients = args[1]
    connection = args[2]
    for client in clients:
        if client != connection:
            msg = jim_handler.msg(message)
            try:
                client.send(msg)
            except:
                to_del.append(client)
                client.close()
    return to_del

def server_broadcast(*args):
    '''SERVER ответ на выход клиента'''
    to_del = []
    message = args[0]
    clients = args[1]
    connection = args[2]
    for client in clients:
        if client != connection:
            msg = jim_handler.message.response(200, msg=message)
            msg = jim_handler.create_msg(msg)
            try:
                client.send(msg)
            except:
                '''Если не вышло закрываю соед и в список на удал-е'''
                to_del.append(client)
                client.close()
    return to_del

ACTIONS = {
    "presence": presence,
    "contacts": send_contacts,
    "add": add_contact,
    "del": del_contact,
    "server_broadcast": server_broadcast,
    "broadcast": broadcast,
    "msg": to_contact,
}


# TODO:
    #def probe(self, client):
    #    проверка онлайн клиента

    #def del_contact(message, clients, connection):
    #    удаление контакта
