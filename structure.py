import csv
import datetime
import time
from decimal import Decimal
from model import create_tables, insert_training, Data, replace_category,insert_data
from knn import get_neighbors, get_response
import os

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
    #print "data %s" % Data.select().count()
    testdataset = process_dataset("test.csv")
    try:
        os.unlink("graphoutput.tx")
    except OSError:
        pass
    for data in testdataset:
        cat = replace_category(data)
        neighbors = get_neighbors(data, k=10)
        with open("graphoutput.txt", "a") as f:
            for i in neighbors:
                d = i.distance
                print i.data.pprint()
                f.write("%s\n" % d)
        result = get_response(neighbors)
        print "%s %s >>>>>>>>>>>>> prediction: %s" % (cat,data[:-1], result)
        yes_no = raw_input("Desea validar el valor (y/[n])? ")
        if yes_no is 'y':
            result = raw_input("nuevo valor 1 or 0: ")
            

        data[-1] = result
        insert_data(*data)




if __name__ == "__main__":
    init()
