import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DEBUG = False

db_name = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)), 'db_server.sqlite')

db_engine = 'sqlite:///{}?check_same_thread=False'.format(db_name)

engine = create_engine(db_engine, echo=DEBUG)

Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
