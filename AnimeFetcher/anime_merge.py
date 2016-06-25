# -*- coding: utf-8 -*-

import sys
import BaseHTTPServer
import cgi
import json
import threading
import urllib2
import time
import itertools
import numpy as np
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
from tools import *
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz


reload(sys)
sys.setdefaultencoding('utf-8')

num_retry = 1
period = int(3600*12)

con = MongoClient('178.62.38.12')
db = con.animedb
animesDB = db.animes

# data format
# {
#     title
#     [titles]
#     timestamp
#     [videos]
#         [nums]
#             link
#             size
#     [batchdownloads]
# }
def mergeAnimes():
    entries = animesDB.find({},{'title':1})
    idtitles = [[entry['_id'],entry['title']] for entry in entries]
    removelist = []

    for j,(id1, t1) in enumerate(idtitles):
        for id2,t2 in idtitles[j+1:]:
            ratio = fuzz.ratio(t1, t2)
            if ratio > 80:
                removelist.append(id1)

                source = animesDB.find_one({'_id':id1})
                target = animesDB.find_one({'_id':id2})

                if ratio < 100:
                    target['titles'].append(t1)
                    if len(t1) < len(t2):
                        target['title'] = t1

                target['titles'] += [t for t in source['titles'] if not t in target['titles']]


                target['timestamp'] = np.max([source['timestamp'],target['timestamp']])

                for num in source['videos'].keys():
                    if not target['videos'].has_key(num):
                        target['videos'][num] = []
                    target['videos'][num] += [s for s in source['videos'][num] if not s in target['videos'][num]]


                if not source.has_key('bunk'):
                    source['bunk'] = []
                if not target.has_key('bunk'):
                    target['bunk'] = []
                target['bunk'] += [b for b in source['bunk'] if not b in target['bunk']]

                animesDB.update({'_id':id2},target)

                print 'Merged: {} and {}'.format(t1,t2)
                break

    for id in removelist:
        animesDB.remove({'_id':id})

if __name__ == '__main__':
    mergeAnimes()
