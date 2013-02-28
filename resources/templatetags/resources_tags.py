import re
from django import template
from django.template import resolve_variable
register = template.Library()

class ActiveClassNode(template.Node):

    def __init__(self, urlarea_regexp):
        self.urlarea_regexp = urlarea_regexp

    def render(self, context):
        # Skanky hack to stop syndication templates erroring
        try:
            url = template.resolve_variable("request.path", context)
        except:
            return ''
        if re.match(self.urlarea_regexp, url):
            return ' class="active"'
        else:
            return ''

@register.tag(name="activeclass")
def do_activeclass(parser, token):
    """
    Return ' class="active"' if the current url matches the regexp
    Requires the url context processor to be enabled
    """
    try:
        tag_name, urlarea_regexp = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single, quoted argument" % token.contents.split()[0]
    return ActiveClassNode(urlarea_regexp[1:-1])

class PyImportNode(template.Node):
    """ Import a python variable """
    def __init__(self, import_spec):
        self.import_spec = import_spec

    def render(self, context):
        bits=self.import_spec.split('.')
        m = __import__('.'.join(bits[:-1]))
        m = __import__(bits[0])
        for i in bits[1:]:
            m = getattr(m, i)
        context[bits[-1]] = m
        return ''

@register.tag(name="py_import")
def do_py_import(parser, token):
    """
    Capture content and set a context variable to the captured string
    """
    try:
        tag_name, import_spec = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires an argument" % token.contents[0]
    return PyImportNode(import_spec)

class PaginationBarNode(template.Node):

    def render(self, context):
        has_previous=resolve_variable('has_previous', context)
        has_next=resolve_variable('has_next', context)
        previous=resolve_variable('previous', context)
        next=resolve_variable('next', context)
        page=resolve_variable('page', context)
        pages=resolve_variable('pages', context)

        html = ''
        if has_previous:
            html+='<li><a href="./?page=%s">&laquo;</a></li>\n' % previous
        if pages > 10:
            for l in range(1,5):
                html+='<li><a href="./?page=%d">%d</a></li>\n' % (l, l)
            html+='<li><span>...</span></li>'
            for l in range(pages-3,pages+1):
                html+='<li><a href="./?page=%d">%d</a></li>\n' % (l, l)
        else:
            for l in range(1,pages+1):
                html+='<li><a href="./?page=%d">%d</a></li>\n' % (l, l)
        if has_next:
            html+='<li><a href="./?page=%s">&raquo;</a></li>\n' % next

        return html

@register.tag
def pagination_bar(parser, token):
    """
    Make a formatted html pagination bar out of the pagination info set for generic views
    """
    return PaginationBarNode()

