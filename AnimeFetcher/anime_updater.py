#!/usr/bin/python3

import sys
import BaseHTTPServer
import cgi
import json
import threading
import urllib2
import time
from bs4 import BeautifulSoup
from pymongo import Connection
import datetime

import configparser

reload(sys)
sys.setdefaultencoding('utf-8')

num_retry = 12
period = int(3600*12)

con = Connection()
db = con.animedb
animelist = db.animelist
animes = db.animes


anime_base_url = 'http://wt.78land.com/ctlist/'
anime_base_download = 'http://wt.78land.com/ctdown/'
anime_list_url = anime_base_url + 'all.htm'

def get_url_content(url):
    anime_doc = ""
    retry = num_retry
    while(retry > 0):
        try:
            anime_req = urllib2.Request(url)
            anime_doc = urllib2.urlopen(anime_req).read()
            retry = 0
        except:
            retry = retry - 1
            pass

    return anime_doc

def parse_download_link(url):
    dl_doc = get_url_content(url)

    dlParse = BeautifulSoup(dl_doc)
    links = dlParse.find_all("a",href = True)
    linkList = []
    for link in links:
        dl_link = link.get("href")
        if dl_link[:7] == "thunder":
            linkList.append(dl_link)


    return linkList

def parse_anime(url, name, anime_id):
    anime_doc = get_url_content(url)
    animeParse = BeautifulSoup(anime_doc)
    animeVideos = animeParse.find_all("td", attrs={"width":"200", "height":"30"})
    for videoParse in animeVideos:
        a_tag = videoParse.a
        video_name = a_tag.string
        video_download_url = anime_base_download + a_tag.get('href').rpartition('/')[-1]
        video_download_link = parse_download_link(video_download_url)
        video = animes.find_one({"name":video_name})
        if video == None:
            animes.insert({"category":anime_id,"name":video_name,"dl_url":video_download_link,"update_at":datetime.datetime.now()})
        print 'Updating Video: {}'.format(video_name)

def run_task():
    # retrive anime list 
    html_doc = get_url_content(anime_list_url)
    # parse list
    htmlParser = BeautifulSoup(html_doc)
    animeListHtml = htmlParser.find_all("a",attrs={"target": "_blank"})
    for animeHtml in animeListHtml:
        animeName = animeHtml.string
        animeUrl = anime_base_url + animeHtml.get('href')
        anime = animelist.find_one({"name":animeName})
        animeID = 0
        if anime == None:
            animeID = animelist.insert({"name":animeName, "url":animeUrl})
        else:
            animeID = anime["_id"]
        print 'Updating {}'.format(animeName)
        parse_anime(animeUrl, animeName, animeID)



while(True):
    # DBManager.connect(dbconfig['username'], dbconfig['password'], dbconfig['dbname'])

    print("Updating Anime List")
    run_task()
    print("Update Done")

    # DBManager.disconnect()
    time.sleep(period)
