import csv
import datetime
import time
from decimal import Decimal
from model import create_tables, insert_training, Data
from knn import get_neighbors, get_response

def process_dataset(file_):
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
    trainingdataset = process_dataset("out.csv")
    create_tables()
    insert_training(trainingdataset)
    print "data %s" % Data.select().count()
    testdataset = process_dataset("test.csv")
    for data in testdataset:
        neighbors = get_neighbors(data)
        result = get_response(neighbors)

if __name__ == "__main__":
    init()
