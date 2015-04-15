import csv
import datetime
import time
from decimal import Decimal

def process_trainingdataset(file_):
    trainingdataset = []
    with open(file_, "rb") as f:
        rows = csv.reader(f)
        for row in rows:
            product, cat, precio, fecha, hora, success = row
            date_str = "%s-%s" % (fecha, hora)
            DF = "%m/%d/%y-%H:%M:%S"
            fechahora = datetime.datetime.strptime(date_str, DF)
            timestamp = time.mktime(fechahora.timetuple())
            trainingdataset.append([cat, Decimal(precio), timestamp, success])
    return trainingdataset

def init():
    trainingdataset = process_trainingdataset("out.csv")
    from model import create_tables, insert_training, Data
    create_tables()
    insert_training(trainingdataset)
    print "data %s" % Data.select().count()

if __name__ == "__main__":
    init()
