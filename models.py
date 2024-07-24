from peewee import PostgresqlDatabase, Model, CharField, ForeignKeyField
import os

DB = {
    'database': os.getenv('POSTGRES_DB', 'iot'),
    'user': os.getenv('POSTGRES_USER', 'user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'host': os.getenv('DB_HOST', 'db'),
    'port': int(os.getenv('DB_PORT', 5432)),
} 

db = PostgresqlDatabase(**DB)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db 


class Apiuser(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()


class Location(BaseModel):
    name = CharField(unique=True)


class Device(BaseModel):
    name = CharField()
    type = CharField()
    login = CharField()
    password = CharField()
    location_id = ForeignKeyField(Location)
    api_user_id = ForeignKeyField(Apiuser)


db.connect()
db.create_tables([Apiuser, Location, Device], safe=True)