from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^post/$', 'comments.views.post_comment'),
    url(r'^posted/$', 'comments.views.comment_was_posted'),
)
