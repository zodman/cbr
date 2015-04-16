import csv
import datetime
import time
from decimal import Decimal
from model import create_tables, insert_training, Data, replace_category
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
            if success == '1':
                success = True
            else:
                success = False
            trainingdataset.append([cat, Decimal(precio), timestamp, success])
    return trainingdataset


def init():
    trainingdataset = process_dataset("out.csv")
    create_tables()
    insert_training(trainingdataset)
    print "data %s" % Data.select().count()
    testdataset = process_dataset("test.csv")
    for data in testdataset:
        cat = replace_category(data)
        neighbors = get_neighbors(data, k=1)
        for i in neighbors:
            print i.data.pprint()
        result = get_response(neighbors)
        print "%s %s >>>>>>>>>>>>> prediction: %s" % (cat,data[:-1], result)



if __name__ == "__main__":
    init()
