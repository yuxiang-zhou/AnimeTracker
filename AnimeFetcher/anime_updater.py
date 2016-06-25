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
from anime_merge import mergeAnimes


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
    title_str = Converter('zh-hans').convert(title_str.decode('utf-8'))

    spliter = ['[',']','\\', '/','(',')']

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
        except:
            try:
                num = int(d.partition(u'第')[-1].rpartition(u'话')[0])
                index = j
            except:
                pass

        if num == 720 or num == 1080:
            num = -1

        if num > -1:
            break



    if num > -1:
        title_str = reduce(lambda x,y:x+' - '+y, [d for d in data[1:index] if len(d.strip()) > 0], '')
    else:
        title_str = reduce(lambda x,y:x+' - '+y, [d for d in data if len(d.strip()) > 0], '')

    title_str = title_str.encode('utf-8').split('\xe6\x96\xb0\xe7\x95\xaa')[-1].strip()

    if title_str[:2] == '- ':
        title_str = title_str[2:]

    return [title_str, num]

def parseSize(size):
    return size.text



def getSimilarAnime(title):
    isFound = False
    video = None
    entries = animesDB.find({},{'title':1, 'titles': 1, 'timestamp': 1})
    for entry in entries:
        for t in entry['titles']:
            ratio = fuzz.partial_ratio(title,t.encode('utf8'))
            lsum = float(len(title) + len(t.encode('utf8')))
            ldiff = np.abs(len(title) - len(t.encode('utf8')))
            if ratio > 90 and ldiff / lsum < 0.4:
                isFound = True
                video = entry
                break

        if isFound:
            break

    return isFound,video
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

    isFound,video = getSimilarAnime(title)

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
        ratios = map(lambda x: fuzz.ratio(title, x), titles)
        lengthes = [len(t) for t in titles]
        if not np.max(ratios) == 100:
            anime['titles'].append(title)
            if len(title) < np.min(lengthes):
                anime['title'] = title

        animesDB.update({'_id':video['_id']},anime)
    else:
        # create new entry if collection not found
        result = animesDB.insert_one({
            'title': title,
            'titles': [title],
            'timestamp': timestamp,
            'videos': {
                num: [{'link':link, 'size': size}]
            }
        });

    return True


def upsertBunk(title, magnet, size, timestamp):
    print title

    entries = animesDB.find({},{'title':1, 'titles': 1, 'timestamp': 1})

    isFound, video = getSimilarAnime(title)

    if isFound:
        anime = animesDB.find_one({'_id':video['_id']})
        # update timestamp
        if anime['timestamp'] < timestamp:
            anime['timestamp'] = timestamp

        # update title
        titles = [t.encode('utf8') for t in anime['titles']]
        ratios = map(lambda x: fuzz.ratio(title, x), titles)
        lengthes = [len(t) for t in titles]
        if not np.max(ratios) == 100:
            anime['titles'].append(title)
            if len(title) < np.min(lengthes):
                anime['title'] = title

        # update bunk
        if not anime.has_key('bunk'):
            anime['bunk'] = []
        if not magnet in [v['link'] for v in anime['bunk']]:
            anime['bunk'].append({'link': magnet, 'size': size})
        else:
            return False

        animesDB.update({'_id':video['_id']}, anime)
    else:
        # create new entry if collection not found
        result = animesDB.insert_one({
            'title': title,
            'titles': [title],
            'timestamp': timestamp,
            'videos': {},
            'bunk': [{'link':magnet, 'size': size}]
        });

    return True




def run_task(update_all=False):
    # Loop through all pages
    for page in itertools.count(1):
        page_url = anime_base_url.format(page)
        page_html = BeautifulSoup(safe_request(page_url), "html.parser")
        table_html = page_html.find("table", {"id": "topic_list"})

        # Stop when empty table are found
        if not table_html:
            break

        entrys_html = table_html.find('tbody').find_all("tr")

        # Loop page entries
        for entry in entrys_html:
            try:
                timestamp, category, title, magnet, size, _, _, _, _ = entry.find_all('td')
            except:
                continue

            print page

            # Parse infomation
            timestamp = parseTimestamp(timestamp)
            category = parseCategory(category)
            title, num = parseTitle(title)
            magnet = parseMagnet(magnet)
            size = parseSize(size)

            # update valid video
            if num > -1 and len(title) > 0:
                success = upsertVideo(title, num, magnet, size, timestamp)
            elif category == 1:
                success = upsertBunk(title, magnet, size, timestamp)
            else:
                continue

            if not success and not update_all:
                return

if __name__ == '__main__':
    import argparse

    # parse arguments

    parser = argparse.ArgumentParser(description='Anime Fetching')
    parser.add_argument('-a', dest='update_all', default=False, help='Anime List Update ALL', action="store_true")
    args = parser.parse_args()

    run_task(update_all=args.update_all)
    mergeAnimes()

    while(True):
        # DBManager.connect(dbconfig['username'], dbconfig['password'], dbconfig['dbname'])

        print("Updating Anime List")
        run_task()
        print("Update Done")

        # DBManager.disconnect()
        time.sleep(period)
