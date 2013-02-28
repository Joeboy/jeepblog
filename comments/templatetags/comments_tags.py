from jeepblog.comments.models import Comment
from django import template
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from resources import captcha
from django.conf import settings
import re

register = template.Library()

#def contact(request):
#    if request.method == 'POST':
#        # Check the captcha
#        check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
#        if check_captcha.is_valid is False:
#            # Captcha is wrong show a error ...
#            return HttpResponseRedirect('/url/error/')
#        form = ContactForm(request.POST)
#        if form.is_valid():
#            # Do form processing here...
#            return HttpResponseRedirect('/url/on_success/')
#    else:
#        form = ContactForm()
#        html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
#    return render_to_response('contact.html', {'form': form, 'html_captcha': html_captcha})

class CommentFormNode(template.Node):
    def __init__(self, object_name):
        self.object_name = object_name

    def render(self, context):
        object = template.resolve_variable(self.object_name, context)
        obj_type = ContentType.objects.get_for_model(object.__class__)
        context['target'] = '%s:%s' % (obj_type.id, object.id)
        context['html_captcha'] = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)

        default_form = loader.get_template('comments/form.html')
        output = default_form.render(context)
        return output

@register.tag
def comment_form(parser, token):
    """
    Displays a comment form for the given params.
    """

    tokens = token.contents.split()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least 1 argument" % tokens[0]
    return CommentFormNode(tokens[1])

class CommentCountNode(template.Node):
    def __init__(self, object_name):
        self.object_name = object_name

    def render(self, context):
        try:
            object = template.resolve_variable(self.object_name, context)
        except template.VariableDoesNotExist:
            return ''
        comment_count = object.comments.all().count()
        return str(comment_count)

@register.tag
def get_comment_count(parser, token):
    """
    Returns the comment count for the given object
    Example usage:
    {% get_comment_count blog_post %}
    """

    tokens = token.contents.split()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError, "%r tag requires 1 argument" % tokens[0]

    return CommentCountNode(tokens[1])

class GetCommentsNode(template.Node):
    def __init__(self, object_name):
        self.object_name = object_name

    def render(self, context):
        try:
            object = template.resolve_variable(self.object_name, context)
        except template.VariableDoesNotExist:
            return ''
        context['comments'] = object.comments.all()
        return ''

@register.tag
def get_comments(parser, token):
    """
    Gets comments for the given object, putting them in the
    'comments' context var
    Example usage:
    {% get_comments blog_post %}
    """

    tokens = token.contents.split()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError, "%r tag requires 1 argument" % tokens[0]

    return GetCommentsNode(tokens[1])

