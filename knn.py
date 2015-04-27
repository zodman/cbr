from model import Data, Distance, Category
import math
from decimal import Decimal
from datetime import datetime

def euclidean_distance(test_data, data_obj):
    distance = 0
    data_list = [data_obj.price,
                 data_obj.weekday(),
                 Data.is_light(data_obj.timestamp)
                 ]
    test_data = [test_data[1], 
                datetime.fromtimestamp(test_data[2]).weekday(),
                Data.is_light(test_data[2])
                ]
    for i, elem in enumerate(data_list):
        distance += pow((Decimal(test_data[i]) - elem), 2)
    return math.sqrt(distance)


def get_neighbors(test_data, k=1):
    Distance.delete().execute()
    cat = test_data[0]
    datas = Data.select().where(Data.category == cat)
    for d in datas:
        dist = euclidean_distance(test_data, d)
        Distance.create(distance=dist, data=d)
    distances = Distance.select().order_by(Distance.distance.desc()).limit(k)
    return distances

import operator


def get_response(neighbors):
    SUCCESS = 1
    FAIL = 0
    k = {SUCCESS: 0, FAIL: 0}
    for i in neighbors:
        k[i.data.success] += 1
    sortedVotes = sorted(k.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]
