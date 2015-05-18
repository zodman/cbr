import sys
import os
import unicodecsv as csv
import radar
import datetime
import random
try:
    from local_settings import client_id, client_secret
except ImportError:
    print "no local_setings"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, "python-sdk", "lib"))

from meli import Meli
URL = "http://waifu.ca/"
TOKEN = os.environ.get("TOKEN")
auth_params = dict(client_id=client_id, client_secret=client_secret)
SITE = "MLM"
TIMES  = random.randint(1,2)
NUM_PAGE = random.randint(1,10)
LIMIT = 30 # random.randint(1,10)
FROM_DATE = datetime.datetime(year=2000, month=5, day=24)
TO_DATE = datetime.datetime.now()

def write_cvs(data):
    f_ = open(sys.argv[1], "w")
    wr = csv.writer(f_, encoding="utf-8", quoting=csv.QUOTE_ALL)
    for d in data:
        items = d["items"]
        for i in [dict(t) for t in set([tuple(f.items()) for f in items])]:
            random_date = radar.random_datetime(start=FROM_DATE, stop=TO_DATE)
            date_ = random_date.strftime("%x")
            time_ = random_date.strftime("%X")
            tran = random.randint(0,1)
            wr.writerow((i["item_name"], d['cat_name'], i['item_price'], date_, time_, tran))
    f_.close()

def main():
    if not  TOKEN:
        CODE = os.environ.get("CODE")
        if not CODE:
            ml_api = Meli(**auth_params)
            print ml_api.auth_url(redirect_URI=URL)
            print "login and run CODE=foobar main.py"
        else:
            ml_api = Meli(**auth_params)
            ml_api.authorize(CODE,URL)
            print "export set TOKEN='%s'" % ml_api.access_token
        sys.exit(0)

    auth_params.update({'access_token':TOKEN})

    ml_api = Meli(**auth_params)

    resp = ml_api.get("/sites/%s/categories" % SITE )
    cat_list = resp.json()
    data = []
    cat_count = 0
    item_count = 0
    for cat in cat_list:
        cat_id = cat.get("id")
        cat_name = cat.get("name")
        d = {'cat_id':cat_id, 'cat_name':cat_name, 'items':[]}
        cat_count +=1
        print d
        for page in range(0,TIMES):
            url = "/sites/{}/hot_items/search?limit={}&category={}&page={}".format(SITE,LIMIT,cat_id, page)
            resp = ml_api.get(url)
            item_list = resp.json()["results"]
            for item in item_list:
                item_count +=1
                item_name = item.get("title")
                item_id = item.get("id")
                item_price = item.get("price")
                if item_name:
                    d["items"].append({'item_id': item_id,
                        'item_price':item_price, 'item_name': item_name})
                    #print d
        data.append(d)
    print "fetch"
    print "cats: {} items: {}".format(cat_count, item_count)
    return data

if __name__ == "__main__":
    write_cvs(main())
