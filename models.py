import os
import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect

# determine database to use depending on if environment is local or heroku
if 'ON_HEROKU' in os.environ:
    print('\nheroku environment database')
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    print('\nlocal environment database')
    DATABASE = SqliteDatabase('TripStatistics.sqlite')


class User(UserMixin, Model):
    username = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class All_Map(Model):
    trip_name = CharField()
    filename = CharField()
    user = CharField()
    data = CharField(max_length=65535)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, All_Map], safe=True)
    print("TABLES Created")
    DATABASE.close()
