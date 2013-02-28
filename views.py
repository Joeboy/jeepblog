from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.conf import settings

from jeepblog.blog.models import Post, Category
import itertools

@cache_page(5*60)
def home(request, xhtml=False):
    """ Homepage view """

    frontpage_categories = Category.objects.filter(frontpage=True)

    return render_to_response('home.html', {'frontpage_categories':frontpage_categories}, context_instance=RequestContext(request))


@cache_page(5*60)
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request) )
