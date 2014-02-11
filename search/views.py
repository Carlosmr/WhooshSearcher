# -*- coding: utf-8 -*-
from whoosh.index import create_in,open_dir
from whoosh.fields import *
import os.path
from whoosh.qparser import QueryParser
from whoosh.query import *
from whoosh import index
import sys,traceback
from django.template import Context, RequestContext
from django.shortcuts import render_to_response


class Result():

    def __init__(self, title, url, date, highlights, keywords):
        self.title = title
        self.url = url
        self.date = date
        self.highlights = highlights
        self.keywords = keywords

def search(request):
    hits = []
    results = []
    query = request.GET.get('q', None)
    newspaper = request.GET.get('newspaper', None)
    if newspaper is not None:
        index_dir = "C:/Django Projects/searcher/modules/index" + newspaper
        ix = index.open_dir(index_dir)
        searcher = ix.searcher()
        if query is not None and query != u"":
            query = query.replace('+', ' AND ').replace(' -', ' NOT ')
            parser = QueryParser("content", schema=ix.schema)
            try:
                qry = parser.parse(query)
            except:
                qry = None
            if qry is not None:
                hits = searcher.search(qry)

        for hit in hits:
            title = hit['title']
            url = hit['url']
            date = hit['date']
            highlights = hit.highlights("content")
            keywords_list = [keyword for keyword, score in searcher.key_terms_from_text("content", hit['content'])]
            keywords = ", ".join(keywords_list)
            results.append(Result(title,url,date,highlights,keywords))
            


    variables = RequestContext(request, {
        'query': query,
        'hits': results
    })
    return render_to_response('search.html', variables)