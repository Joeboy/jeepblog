from django.conf.urls import *
from django.views.decorators.cache import cache_page

from jeepblog.blog.models import Post

urlpatterns = patterns('',
    url(r'^$', 'blog.views.index', name="index"),
    url(r'^(?P<blog_path>[a-zA-Z0-9/-]+)/$', 'blog.views.blog_entry', name="blog_path"),
)

