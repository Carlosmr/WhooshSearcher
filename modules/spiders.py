# -*- coding: utf-8 -*-
import os, re, sqlite3, sys; sys.path.insert(0, os.path.join("..", ".."))
import string
from datetime import datetime
from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO, URL,plaintext,DOM
from django.utils.encoding import smart_str, smart_unicode
from whooshHelper import *

def encode(s):
    #Removes non-ascii characters.
    return "".join(filter(lambda x: 32 <= ord(x) <= 126, s))

class HuffingtonSpider(Spider):
    
    def __init__(self, whoosh):
        Spider.__init__(self, links=["http://www.huffingtonpost.co.uk/"], domains=["huffingtonpost.co.uk"], delay=0.0)
        self.whoosh=whoosh
    
    def htmlParser(self,link):
        html = URL(link).download()
        result = ''
        
        body = DOM(html).body
        for e in body.by_tag('p'):
            a = e.by_tag('a')
            img = e.by_tag('img')
            span = e.by_tag('span') 
    
            if a == [] and img == [] and span == []:
                plainText = plaintext(encode(e.content),linebreaks=2, indentation = True)
                content = encode(plainText)
                filterContent = content.strip().lower()
                if filterContent != 'share your comment:':
                    result = result + plainText + '\n '

        pretty = unicode(result.strip())            
        return pretty
        
    def getTitle(self, link):
        html = URL(link).download()
        body = DOM(html).body
        title = body.by_class("title-news")[0].content.strip()
        return title

    def visit(self, link, source=None):
        match = re.search("huffingtonpost.co.uk/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            splitted_url = link.url.split('/')
            article_date = datetime.datetime(int(splitted_url[3]), int(splitted_url[4]), int(splitted_url[5]))
            title = self.getTitle(link.url)
            encodedContent = self.htmlParser(link.url)
            self.whoosh.addDocument(title, link.url, article_date, encodedContent)
            print "Date:", article_date, "\nTitle:", str(encode(title)), "\nUrl:", link.url, "\n\n"
            print "----------------------------------------------------------------------------------------------"

    def fail(self, link):
        print "failed:", encode(link.url),"\n"

    def priority(self, link, method=DEPTH):
        match = re.search("huffingtonpost.co.uk/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            return Spider.priority(self, link, method)
        else:
            return 0.0

class GuardianSpider(Spider):
    dic = {'jan':1,'feb':2,'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
    
    def __init__(self, whoosh):
        Spider.__init__(self, links=["http://www.theguardian.com/"], domains=["www.theguardian.com"], delay=0.0)
        self.whoosh=whoosh
    
    def htmlParser(self,link):
        html = URL(link).download()
        body = DOM(html).body
        content = body.by_id("content")
        if content:
            plaincontent = plaintext(content.content, linebreaks=2, indentation = True)
            pretty = unicode(plaincontent.strip())
        else:
            pretty=''            
        return pretty
        
    def getTitle(self, link):
        html = URL(link).download()
        body = DOM(html).body
        node = body.by_id("main-article-info")
        if node:
            title = node.children[1].content.strip()
        else:
            title = ''
        return title
    
    def visit(self, link, source=None):
        match = re.search("/\d{4}/\w{3}/\d{2}/", link.url)
        if match:
            is_video = re.search("video", link.url)
            if not is_video:
                splitted_url = link.url.split('/')
                splitted_date = match.group(0).split('/')
                article_date = datetime.datetime(int(splitted_date[1]), self.dic[splitted_date[2]], int(splitted_date[3]))
                encodedContent = self.htmlParser(link.url)
                if encodedContent:
                    title = self.getTitle(link.url)
                    if title:
                        self.whoosh.addDocument(title, link.url, article_date, encodedContent)
                        print "Date:", article_date, "\nTitle:", str(encode(title)), "\nUrl:", link.url, "\n\n"
                        print "-----------------------------------------------------"
                else:
                    print "Not a news article."
                    print link.url
                    print "-----------------------------------------------------"
            else:
                print "Its a video."
                print "-----------------------------------------------------"


    def fail(self, link):
        print "failed:", encode(link.url),"\n"

    def priority(self, link, method=DEPTH):
        match = re.search("/\d{4}/\w{3}/\d{2}/", link.url)
        if match:
            if re.search("media", link.url):
                res = 0.0
            else:
                res =  Spider.priority(self, link, method)
        else:
            res= 0.0
        return res


class ReutersSpider(Spider):
    
    def __init__(self, whoosh):
        Spider.__init__(self, links=["http://in.reuters.com/"], domains=["in.reuters.com"], delay=0.0)
        self.whoosh=whoosh
    
    def htmlParser(self,link):
        html = URL(link).download()
        result = ''
        body = DOM(html).body.by_class('column2 gridPanel grid8')[0]
        paragraphs = body('p')
        article = ''
        for p in paragraphs:
            article+=str(p)
        plainText = plaintext(encode(article),linebreaks=2, indentation = True)
        content = encode(plainText)
        pretty = unicode(content.strip())            
        return pretty
        
    def getTitle(self, link):
        html = URL(link).download()
        body = DOM(html).body.by_class('column2 gridPanel grid8')[0]
        title = body('h1')[0].content
        return title

    def visit(self, link, source=None):
        match = re.search("in.reuters.com/article/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            splitted_url = link.url.split('/')
            article_date = datetime.datetime(int(splitted_url[4]), int(splitted_url[5]), int(splitted_url[6]))
            title = self.getTitle(link.url)
            encodedContent = self.htmlParser(link.url)
            self.whoosh.addDocument(title, link.url, article_date, encodedContent)
            print "Date:", article_date, "\nTitle:", str(encode(title)), "\nUrl:", link.url, "\n\n"
            print "----------------------------------------------------------------------------------------------"

    def fail(self, link):
        print "failed:", encode(link.url),"\n"

    def priority(self, link, method=DEPTH):
        match = re.search("in.reuters.com/article/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            return Spider.priority(self, link, method)
        else:
            return 0.0