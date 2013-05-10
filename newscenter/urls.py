from datetime import datetime
from django.conf.urls.defaults import *
from newscenter.feeds import NewsroomFeed
from django.views.generic.list import ListView

from newscenter import models 

##Object List
urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=models.Newsroom.objects.all()), name='newscenter_index'),
    url(r'^categories/$',  ListView.as_view(queryset=models.Newsroom.objects.all()), name='category_index')
)

##Custom 
urlpatterns += patterns('newscenter.views',
    (r'^(?P<slug>[\-\d\w]+)/$',
        'newsroom_detail', None, 'news_newsroom_detail'),
    (r'^categories/(?P<slug>[\-\d\w]+)/$',
        'category_detail', None, 'news_category_detail'),
    (r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<slug>[\-\d\w]+)/$',
        'article_detail', None, 'news_article_detail'),
    (r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        'archive_month', None, 'news_archive_month',),
    (r'^(?P<newsroom>[\-\d\w]+)/(?P<year>\d{4})/$', 
        'archive_year', None, 'news_archive_year',)
)

##Feeds
urlpatterns += patterns('',
    (r'^(?P<newsroom>[\-\d\w]+)/rss/$', NewsroomFeed(), None, 'newsroom_feed'),
)
