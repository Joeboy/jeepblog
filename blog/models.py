from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from jeepblog.comments.models import Comment
from datetime import datetime

class Tag(models.Model):
    name = models.CharField('Name', max_length=25)
    slug = models.CharField(max_length=25, unique=True, db_index=True)
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    def save(self):
        super(Tag, self).save()
        # keep a tally of how many posts are tagged with this tag:
        self.count = self.post_set.count()
        super(Tag, self).save()

class Category(models.Model):
    title = models.CharField('Title', max_length=100)
    slug = models.CharField( 'Slug', max_length=30, unique=True, db_index=True,)
    parent = models.ForeignKey('Category', null=True, blank=True)
    frontpage = models.BooleanField()

    def __unicode__(self):
        return self.title

    def frontpage_post_set(self):
        return self.post_set.filter(frontpage=True)

    def get_entry_path(self):
        """ Return a list of categories between the root and this one """
        path = []
        c = self
        while c:
            path.append(c)
            c = c.parent
        return path[::-1]

    def get_absolute_url(self):
        blog_path = '/'.join([b.slug for b in self.get_entry_path()])
        return reverse('blog:blog_path', args=(), kwargs={'blog_path': blog_path})

    def save(self, *args, **kwargs):
        if self.parent == self:
            return
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

class Post(models.Model):
    """ Model for a blog post """
    title = models.CharField('Title', max_length=100)
    slug = models.CharField( 'Slug', max_length=30, unique=True, db_index=True,
    )
    date = models.DateTimeField(default=datetime.now, db_index=True)
    body = models.TextField('Body Text')
    comments = generic.GenericRelation(Comment)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    category = models.ForeignKey(Category)

    published = models.BooleanField()
    frontpage = models.BooleanField()

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        # Update tag tallies
        for t in self.tags.all():
            t.save()

    def get_entry_path(self):
        return self.category.get_entry_path() + [self]

    def get_absolute_url(self):
        blog_path = '/'.join([b.slug for b in self.get_entry_path()])
        return reverse('blog:blog_path', args=(), kwargs={'blog_path': blog_path})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-date',)

    class Admin:
        list_display=('title', 'date', 'published')

#from django.contrib import admin

#class PostOptions(admin.ModelAdmin):
#    list_display = ('slug', 'title', 'date')
#    search_fields = ('title',)
#    date_hierarchy = 'date'
#    prepopulated_fields = {'slug': ('title',)}
#
##site = admin.AdminSite()
#admin.site.register(Post, PostOptions)
#
