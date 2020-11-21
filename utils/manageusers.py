from peewee import *
from system import get_config_file

db = SqliteDatabase('users.db')
config = get_config_file("../config.json")
id_super_admin = config["id_super_admin"].split(";")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id_user = IntegerField(unique = True)
    name = CharField()
    username = CharField()

class Admin(BaseModel):
    id_user = ForeignKeyField(User, backref='users')
    name = CharField()
    username = CharField()

class SuperAdmin(BaseModel):
    id_user = CharField()
    name = CharField()
    username = CharField()

db.connect()
db.create_tables([User,Admin,SuperAdmin])

overlord = SuperAdmin(id_user = id_super_admin[0], name = id_super_admin[1], username = id_super_admin[2])
overlord.save()
db.close()
