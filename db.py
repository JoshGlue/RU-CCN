
from peewee import  *
import datetime


instance = SqliteDatabase("stock.db")


class Symbol(Model):
    name = CharField()
    symbol = CharField(unique=True)
    class Meta:
        database = instance
class Portfolio(Model):
    symbol = ForeignKeyField(Symbol, related_name='portfolios')
    price = FloatField()
    invest = FloatField()

    class Meta:
        database = instance
class StockValue(Model):
    value = FloatField()
    symbol = ForeignKeyField(Symbol, related_name='values')
    date = DateTimeField()

    class Meta:
        database = instance



class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = instance # This model uses the "people.db" database.


class Pet(Model):
    owner = ForeignKeyField(Person, related_name='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = instance # this model uses the "people.db" database
instance.connect()
instance.create_tables([Symbol, Portfolio, StockValue],safe=True)
