from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site


#from django.utils.text import truncate_html_words

from blog.models import Post, Tag
from datetime import datetime

class AllFeed(Feed):
    title="Look, it's Wayne's blog"
    link="/all/"
    description="Shit Wayne says"
    link = Site.objects.all()[0].domain

    def items(self):
        return Post.objects.filter(published=True, date__lte=datetime.now())[:10]

    def item_pubdate(self, obj):
        return obj.date

    def item_description(self, obj):
        return obj.body
