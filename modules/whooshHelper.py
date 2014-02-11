# -*- coding: utf-8 -*-
from whoosh.index import create_in,open_dir
from whoosh.fields import *
import os.path
from whoosh.qparser import QueryParser
from whoosh.query import *
import sys,traceback

class WhooshHelper:
    path = ""
    
    def __init__(self, path="index"):
        self.path=path
        if not os.path.exists(path):
            self.addSchema()
    
    
    
    def addSchema(self):
        schema = Schema(title=ID(stored=True, unique=True), url=ID(stored=True, unique=True), date = DATETIME(stored=True), content=TEXT(stored=True))
        os.mkdir(self.path)
        self.ix = create_in(self.path, schema)
    
    def addDocument(self, newsTitle, newsUrl, date, newsContent):
        ix = open_dir(self.path)
        writer = ix.writer()
        writer.update_document(title=newsTitle, url=newsUrl, date=date, content=newsContent)
        writer.commit()
        
    def search(self,queryString):
        try:
            ix = open_dir(self.path)
            with ix.searcher() as searcher:
                parser = QueryParser("content", ix.schema)
                myQuery = parser.parse(queryString)
                results = searcher.search(myQuery)
                if (len(results)==0):
                       print u"No matches found."
                else:
                    print "Numbers of matches: "+str(len(results))
                    for r in results:
                        print str(r) + "\n"
                    
        except:
            print "Problems with the result."
            print traceback.print_exc(file=sys.stdout)