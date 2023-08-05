import pytest
import socket as s
from datetime import datetime

from protocol.jim import Responses


responses = Responses()

@pytest.fixture()
def time(request):
    time = datetime.now()


@pytest.fixture()
def resource_setup(request):
    time = str(datetime.now())
    resurs = '{{ "test": "test", "time":"{}" }}'.format(time)
    return resurs.encode('utf-8')


def test_get_response(time):
    data = responses.get_response(200, time,
                                  msg='Hello', contacts='contacts')
    assert data == {"response": 200,
                    "time": time,
                    "alert": 'Hello',
                    "contacts": 'contacts'
                    }

# Не видит time - надо разбираться
def test_get_data(resource_setup, time):
    data = responses.get_data(resource_setup)
    assert data == {"test": "test",
                    "time": time}


def test_msg(time):
    data = responses.msg({"message": "test"}, time)
    assert data == {"action": "msg",
                    "time": time,
                    "to": "#all",
                    "from": "Anonimus",
                    "message": "test",}
