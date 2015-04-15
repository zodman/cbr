import peewee
from datetime import datetime

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
    timestamp = peewee.DecimalField()
    success = peewee.BooleanField()

    class Meta:
        database = db

    def convert_timestamp(self):
        return self.convert_datetime().strftime("%Y-%m-%d %H:%M:%S")

    def convert_datetime(self):
        return datetime.fromtimestamp(self.timestamp)

    def pprint(self):
        price = self.price
        cat = self.category.name
        d = self.convert_timestamp()
        return u"$%s %s %s [%s]" % (price, cat, d, self.success)


class Distance(peewee.Model):
    distance = peewee.DecimalField()
    data = peewee.ForeignKeyField(Data)

    def pprint(self):
        d = self.data.pprint()
        return u"dist: %s data:%s" % (self.distance, d)
    class Meta:
        database = db


def create_tables():
    db.create_tables([Category, Data, Distance])


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
    return Data.create(category=cat,
            price=price, timestamp=timestamp, success=success)

def replace_category(test_datasets):
    for i, dataset in enumerate(test_datasets):
        cat = dataset[0]
        id = insert_categories(cat).id
        test_datasets[i][0] = id

        
