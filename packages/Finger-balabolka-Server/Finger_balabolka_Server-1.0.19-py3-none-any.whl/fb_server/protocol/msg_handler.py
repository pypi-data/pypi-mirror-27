from datetime import datetime

from .jim import *


class MessageHandler:
    '''Формирование ответов по протоколу JIM'''
    def response(self, code, **kwargs):
        RESPONSE["response"] = code
        RESPONSE["alert"] = kwargs.get('msg', None)
        RESPONSE["contacts"] = kwargs.get('contacts', None)
        return RESPONSE

    def presence(self, contacts):
        '''Присутсвие, ответ при конекте клиента'''
        msg = "Welcome to 'Finger Balabolka'!"
        presence = self.response(200, msg=msg, contacts=contacts)
        return presence

    def msg(self, data):
        MESSAGE["time"] = str(datetime.now())
        MESSAGE["to"] = data.get("to", "#all")
        MESSAGE["from"] = data.get("from", "SERVER")
        MESSAGE["message"] = data.get("message", None)
        return MESSAGE
