# -*- coding: utf-8 -*-
import os, re, sqlite3, sys; sys.path.insert(0, os.path.join("..", ".."))
import string
from datetime import datetime
from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO, URL,plaintext,DOM, Element
from django.utils.encoding import smart_str, smart_unicode
from whooshHelper import *
from spiders import encode

link = "http://in.reuters.com/article/2013/08/16/iran-nuclear-salehi-idINDEE97F05Q20130816"

html = URL(link).download()
result = ''
body = DOM(html).body.by_class('column2 gridPanel grid8')[0]
title = body('h1')[0].content

splitted_url = link.split('/')

article_date = datetime.datetime(int(splitted_url[4]), int(splitted_url[5]), int(splitted_url[6]))

print article_date