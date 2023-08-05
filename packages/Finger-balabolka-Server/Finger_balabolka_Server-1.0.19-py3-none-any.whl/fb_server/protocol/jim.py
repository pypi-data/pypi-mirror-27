# сообщения JIM Ответ​

from datetime import datetime


TIME = datetime.now()

RESPONSE ={
    "response": None,
    "time": str(TIME),
    "alert": None,
    "contacts": None
}

MESSAGE = {
    "action": "msg",
    "time": str(TIME),
    "to": "#all",
    "from": None,
    "message": None,
}
