from model import Data, Distance
import math
from decimal import Decimal


def euclidean_distance(test_data, data_obj):
    distance = 0
    data_list = [data_obj.category.id, data_obj.price,
                 data_obj.timestamp]
    test_data = test_data[:-1]
    for i, elem in enumerate(data_list):
        distance += pow((Decimal(test_data[i]) - elem), 2)
    return math.sqrt(distance)


def get_neighbors(test_data, k=1):
    Distance.delete().execute()
    for d in Data.select():
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
