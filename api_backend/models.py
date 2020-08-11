import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('TripStatistics.sqlite')

class User(UserMixin, Model):
    username = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Map(Model):
    name = CharField()
    user = CharField()
    data = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Map], safe=True)
    print("TABLES Created")
    DATABASE.close()