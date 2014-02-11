# -*- coding: utf-8 -*-
from spiders import *
from whooshHelper import *



whooshGuardian = WhooshHelper("indexGuardian")
whooshHuffington = WhooshHelper("indexHuffington")
whooshReuters = WhooshHelper("indexReuters")

spiderGuardian = GuardianSpider(whoosh=whooshGuardian)
spiderHuffington = HuffingtonSpider(whoosh=whooshHuffington)
spiderReuters = ReutersSpider(whoosh=whooshReuters)

while True:
    spiderGuardian.crawl(cached=False)
    spiderHuffington.crawl(cached=False)
    spiderReuters.crawl(cached=False)