from peewee import *
import datetime

DB = SqliteDatabase("DataBase.db")


class Stoke(Model):
    Pr_code = IntegerField()
    Pr_Name = CharField()
    Pr_Quantity = IntegerField()
    Pr_Sold_Quantity = IntegerField()
    Pr_Prise = FloatField()

    class Meta:
        database = DB


class History(Model):
    Pr_Name = CharField()
    Pr_Prise = FloatField()
    Pr_Sold_Quantity = IntegerField()
    Pr_code = IntegerField()
    pr_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DB


class Settings(Model):
    Ui_Theme_color = CharField()

    class Meta:
        database = DB


def Create_dataBase():
    DB.connect()
    DB.create_tables([Stoke, History, Settings])
    DB.close()
if __name__ == '__main__':
    Create_dataBase()