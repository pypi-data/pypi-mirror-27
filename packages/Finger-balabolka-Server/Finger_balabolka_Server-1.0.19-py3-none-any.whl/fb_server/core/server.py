import sys
import socket
import json
import logging
import select

from fb_server.utils import log_config
from fb_server.db.managers import ClientManager, ClientHistoryManager
from .handler import load_msg, ACTIONS


logger = logging.getLogger("server_log")


class Server():
    """Основной класс сервера чата"""
    server = None
    def __init__(self, *params):
        self.ip_address = params[0]
        self.port = params[1]
        self._clients = []
        self.accounts = {}
        self._create_server()

    def _create_server(self):
        '''стартуем сервервер'''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip_address, self.port))
        self.server.listen(100)
        self.server.settimeout(0.2)

    def shutdown(self):
        self.server.close()

    def _connect(self):
        conn, addr = self.server.accept()
        logger.info("{}:{} connected".format(addr[0], addr[1]))
        return conn, addr

    def _remove(self, to_del):
        for client in to_del:
            if client in self._clients:
                self._clients.remove(client)

    def _read_requests(self, r_clients):
        """Чтение сообщений"""
        messages = []
        for sock in r_clients:
            msg = load_msg(sock.recv(1024))
            try:
                messages.append((msg, sock))
            except:
                logger.info('Клиент {} {} отключился'.format(sock.fileno(),
                                                            sock.getpeername()))
                self._clients.remove(sock)
        return messages

    def _write_responses(self, messages):
        clients = self._clients
        accounts = self.accounts
        result = None
        if messages is None:
            return
        for message, connection in messages:
            if message is None:
                continue
            elif message['action'] == 'quit':
                self._clients.remove(connection)
                msg = "Перестал флудить - {}".format(message['from'])
                result = ACTIONS["server_broadcast"](msg, self._clients,
                                            connection, accounts)
                continue
            else:
                result = ACTIONS[message['action']](message, clients,
                                                    connection, accounts)
            if result is not None:
                self._remove(result)

    def _client_connect(self):
        username = None
        try:
            conn, addr = self._connect()
            data = conn.recv(1024)
            message = load_msg(data)
            if message and message['action'] == 'presence':
                username = ACTIONS['presence'](conn, message, addr)
        except OSError as e:
            pass
        else:
            if username:
                self._clients.append(conn)
                self.accounts[username] = conn
        finally:
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(self._clients, self._clients, [], wait)
            except:
                pass
            requests = self._read_requests(r)
            self._write_responses(requests)

    def start_server(self):
        """"""
        while True:
            self._client_connect()
