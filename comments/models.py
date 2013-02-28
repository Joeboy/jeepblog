from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.contrib import admin
import datetime

#class SimpleQuestion(models.Model):
#    """ A simple question and answer for defeating spambots """
#    question=models.CharField(max_length=250)
#    answer=models.CharField(max_length=250)
#
#    def __unicode__(self):
#        return self.question


class Comment(models.Model):
    """ model for a comment """
    user = models.ForeignKey(User, null=True, blank=True)
    name_of_poster = models.CharField(max_length=60, null=True, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
#    title = models.CharField(max_length=255)
    text = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_address = models.IPAddressField(blank=True, null=True)
    content_object = generic.GenericForeignKey()

    class Meta:
        ordering = ('date',)
    class Admin:
        fields = (
            (None, {'fields': ('content_type', 'object_id')}),
            ('Content', {'fields': ('user', 'name_of_poster', 'text')}),
            ('Meta', {'fields': ('ip_address',)}),
        )
        list_display = ('user', 'date', 'content_type')
        list_filter = ('date',)
        date_hierarchy = 'date'
        search_fields = ('comment', 'user__username')

    def __str__(self):
        return "%s: %s..." % (self.get_username(), self.text[:100].encode('ascii', 'replace'))

    def get_absolute_url(self):
        return self.get_content_object().get_absolute_url() + "#c" + str(self.id)

    def get_username(self):
        return self.user and self.user.username or self.name_of_poster

    def get_as_text(self):
        return 'Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s' % \
            {'user': self.user.username, 'date': self.submit_date,
            'comment': self.comment, 'domain': self.site.domain, 'url': self.get_absolute_url()}

