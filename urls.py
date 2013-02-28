from django.conf.urls import *
from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotFound
from settings import MEDIA_ROOT
from blog.feeds import AllFeed

admin.autodiscover()


urlpatterns = patterns('',
#    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes':True}),

    url(r'^$', 'jeepblog.views.home'),
    url(r'^about/$', 'jeepblog.views.about', name='about'),
    url(r'^articles/', include('blog.urls', namespace='blog')),
    url(r'^comments/', include('jeepblog.comments.urls', namespace='comments')),
    url(r'^contact/', include('jeepblog.contactform.urls', namespace='contact')),
    url(r'^rss/all/$', AllFeed(), name="rss_all"),
    url('^admin/', admin.site.urls),
)
