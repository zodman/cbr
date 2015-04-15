import csv
import datetime
import time
from decimal import Decimal

def process_trainingdataset(file_):
    categories = set()
    trainingdataset = []
    with open(file_, "rb") as f:
        rows = csv.reader(f)
        for row in rows:
            product, cat, precio, fecha, hora, success = row
            date_str = "%s-%s" % (fecha, hora)
            DF = "%m/%d/%y-%H:%M:%S"
            fechahora = datetime.datetime.strptime(date_str, DF)
            timestamp = time.mktime(fechahora.timetuple())
            categories.add(cat)
            index = len(categories)
            trainingdataset.append([index, Decimal(precio), timestamp, success])

    categories = list(categories)
    return trainingdataset, categories

if __name__ == "__main__":
    trainingdataset, categories = process_trainingdataset("out.csv")

