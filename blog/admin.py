from django.contrib import admin
from blog.models import Post, Tag, Category

class PostOptions(admin.ModelAdmin):
    list_display = ('slug', 'title', 'date')
    search_fields = ('title',)
    date_hierarchy = 'date'
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category',)

admin.site.register(Post, PostOptions)
admin.site.register(Tag)
admin.site.register(Category)

