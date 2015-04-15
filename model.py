import peewee

db = peewee.SqliteDatabase(':memory:')
"""
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
"""

class Category(peewee.Model):
    name = peewee.CharField(max_length=50, unique=True)
    class Meta:
        database = db

class Data(peewee.Model):
    category = peewee.ForeignKeyField(Category)
    price = peewee.DecimalField()
    timestamp = peewee.CharField(max_length=100)
    success = peewee.BooleanField()
    class Meta:
        database = db


def create_tables():
    db.create_tables([Category,Data])

def insert_categories(category_name):
    try:
        cat_exist = Category.get(name=category_name)
    except Category.DoesNotExist:
        cat_exist = None

    if not cat_exist:
        cat = Category.create(name=category_name)
        return Category.get(id=cat)
    return cat_exist

def insert_training(data):
    for i in data:
        insert_data(*i)

def insert_data(category, price, timestamp, success):
    cat = insert_categories(category)
    return Data.create(category = cat,
            price=price, timestamp = timestamp, success=success)

