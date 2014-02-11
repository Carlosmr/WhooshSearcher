from django.conf.urls import patterns, include, url
from search.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

site_media = os.path.join(
	os.path.dirname(__file__), 'site_media'
)


urlpatterns = patterns('',
	(r'^$', search),    
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
   	{'document_root': site_media}),
)
