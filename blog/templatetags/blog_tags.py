from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter
@stringfilter
def introparafy(text, url):
    c = text.find('<!--END_INTRO_PARA-->')
    if c != -1:
        return '%s\n<p class="readmorelink"><a href="%s">Read more &raquo;</a></p>' % (text[:c],url)
    else:
        return text

@register.inclusion_tag('blog/includes/category_listing.html', takes_context=True)
def blog_category_listing(context, *args, **kwargs):
    return {
        'category': context['category'],
        'frontpage': kwargs.get('frontpage'),
    }
