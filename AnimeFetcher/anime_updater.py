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


reload(sys)
sys.setdefaultencoding('utf-8')

num_retry = 1
period = int(3600*12)

con = MongoClient('178.62.38.12')
db = con.animedb
animesDB = db.animes


anime_base_url = 'http://share.dmhy.org/topics/list/sort_id/2/page/{}'
# anime_base_url = 'http://share.dmhy.org/topics/list/page/{}?keyword=%E5%9C%A8%E4%B8%8B%E5%9D%82%E6%9C%AC&sort_id=2&team_id=0&order=date-desc'



def parseTimestamp(ts):
    return datetime.datetime.strptime(ts.find('span').text, '%Y/%m/%d %H:%M')


def parseCategory(cat):
    if cat.find('a').attrs["class"][0] == 'sort-2':
        nCat = 0
    elif cat.find('a').attrs["class"][0] == 'sort-31':
        nCat = 1
    else:
        nCat = -1

    return nCat


def parseMagnet(link):
    return link.find('a').attrs['href']


def parseTitle(title):
    title_str = title.find_all('a')[-1].text.strip()


    spliter = [u'\u3010', u'\u3011', '[',']']

    data = []
    index = 0
    for j,c in enumerate(title_str):
        if c in spliter:
            temp = title_str[index:j]
            if len(temp) > 0:
                data.append(temp)

            index = j+1

    index = -1
    num = -1
    for j,d in enumerate(data):
        try:
            num = int(d)
            index = j
            break
        except:
            pass

    if num > -1:
        title_str = reduce(lambda x,y:x+' '+y, data[1:index], '')
        title_str = Converter('zh-hans').convert(title_str.decode('utf-8'))
        title_str = title_str.encode('utf-8')
        title_str = title_str.split('\xe6\x96\xb0\xe7\x95\xaa')[-1].strip()

    return [title_str, num]

def parseSize(size):
    return size.text

# data format
# {
#     title
#     [titles]
#     timestamp
#     [videos]
#         [nums]
#             [downloads]
#                 link
#                 size
#     [batchdownloads]
# }
def upsertVideo(title, num, link, size, timestamp):
    print num,title
    num = str(num)
    entries = animesDB.find({},{'title':1, 'titles': 1, 'timestamp': 1})

    isFound = False
    video = None
    for entry in entries:
        for t in entry['titles']:
            ratio = SequenceMatcher(None, title, t.encode('utf8')).ratio()
            if ratio > 0.4:
                isFound = True
                video = entry
                break

        if isFound:
            break

    if isFound:
        anime = animesDB.find_one({'_id':video['_id']})
        # update timestamp
        if anime['timestamp'] < timestamp:
            anime['timestamp'] = timestamp

        # update video list
        if not anime['videos'].has_key(num):
            anime['videos'][num] = []

        if not link in [v['link'] for v in anime['videos'][num]]:
            anime['videos'][num].append({'link':link, 'size': size})
        else:
            return False

        # update title
        titles = [t.encode('utf8') for t in anime['titles']]
        ratios = map(lambda x: SequenceMatcher(None, title, x).ratio(), titles)
        lengthes = [len(t) for t in titles]
        if not np.max(ratios) == 1:
            anime['titles'].append(title)
            if len(title) < np.min(lengthes):
                anime['title'] = title

        animesDB.update({'_id':video['_id']},anime)
    else:
        result = animesDB.insert_one({
            'title': title,
            'titles': [title],
            'timestamp': timestamp,
            'videos': {
                num: [{'link':link, 'size': size}]
            }
        });

    return True




def run_task():
    for page in itertools.count(1):
        page_url = anime_base_url.format(page)
        page_html = BeautifulSoup(safe_request(page_url), "html.parser")
        table_html = page_html.find("table", {"id": "topic_list"})

        if not table_html:
            break

        entrys_html = table_html.find('tbody').find_all("tr")

        for entry in entrys_html:
            timestamp, category, title, magnet, size, _, _, _, _ = entry.find_all('td')
            print page
            timestamp = parseTimestamp(timestamp)
            category = parseCategory(category)
            title, num = parseTitle(title)
            magnet = parseMagnet(magnet)
            size = parseSize(size)

            if num > -1 and len(title) > 0:
                upsertVideo(title, num, magnet, size, timestamp)



if __name__ == '__main__':
    while(True):
        # DBManager.connect(dbconfig['username'], dbconfig['password'], dbconfig['dbname'])

        print("Updating Anime List")
        run_task()
        print("Update Done")

        # DBManager.disconnect()
        time.sleep(period)
