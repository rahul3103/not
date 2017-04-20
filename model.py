import os
from peewee import Model, CharField, PostgresqlDatabase, ForeignKeyField
from werkzeug.security import generate_password_hash, check_password_hash
from playhouse.db_url import connect
import settings

local_url = 'postgresql://{}:{}@localhost:5432/{}'.format(settings.DB_USER, settings.DB_PASS, settings.DB_NAME)

database = connect(os.environ.get('DATABASE_URL') or local_url)


class BaseModel(Model):
    class Meta:
        database = database


class Users(BaseModel):
    name = CharField()
    email = CharField(null=False, unique=True)
    password_hash = CharField()

    @property
    def password(self):
        raise AttributeError('Cannot access password.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Notepad(BaseModel):
    area = CharField()
    user_id = ForeignKeyField(Users, null=False, db_column='user_id')
