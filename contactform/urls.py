from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 'contactform.views.contact_form', name='index'),
    url(r'^done/$', 'contactform.views.done', name='done'),
)
