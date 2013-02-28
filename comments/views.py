from django.core.exceptions import PermissionDenied
from django import forms #newforms as forms
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
import datetime
import re
from resources import captcha
from django.conf import settings
from django.utils.functional import Promise
from django.utils.encoding import force_unicode

class LazyEncoder(simplejson.JSONEncoder):
    # simplejson needs this encoder to frobble lazy objects
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

class CommentForm(forms.Form):
    text =     forms.CharField(max_length=3000, required=True, widget=forms.Textarea)
    username = forms.CharField(max_length=50, required = True)
    email    = forms.EmailField(required=True)

    def get_comment(self, new_data):
        "Helper function"
        return Comment(None, None, new_data["username"], new_data["content_type_id"],
                new_data["object_id"], new_data["text"].strip(),
                datetime.datetime.now(), new_data["ip_address"])

def post_comment(request):
    if not request.POST:
        raise PermissionDenied, "Only POSTs are allowed"
    try:
        target=request.POST.get('target')
        recaptcha_challenge_field = request.POST.get('recaptcha_challenge_field')
        recaptcha_response_field = request.POST.get('recaptcha_response_field')
    except KeyError:
        raise PermissionDenied, "One or more of the required fields wasn't submitted"
    content_type_id, object_id = target.split(':') # target is something like '52:5157'
    try:
        ctype = ContentType.objects.get(pk=content_type_id)
        obj = ctype.get_object_for_this_type(pk=object_id)
    except ObjectDoesNotExist:
        raise Http404, "The comment form had an invalid 'target' parameter -- the object ID was invalid"
    new_data = request.POST.copy()
    new_data['content_type_id'] = content_type_id
    new_data['object_id'] = object_id
    new_data['ip_address'] = request.META.get('REMOTE_ADDR')
    check_captcha = captcha.submit(recaptcha_challenge_field, recaptcha_response_field, settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])

    form = CommentForm(new_data)
    if form.is_valid() and check_captcha.is_valid:
        today = datetime.date.today()
        c = form.get_comment(new_data)
        c.save()
    else:
        if request.GET.has_key('xhr'):
            return HttpResponse(simplejson.dumps({'errors':form.errors.items(), 'valid_captcha':check_captcha.is_valid}, cls=LazyEncoder))
        else:
            return HttpResponse('<p>Sorry, there was an error with the information you entered. Please go back and try again.</p>')
    if request.GET.has_key('xhr'):
        comments = [{'username':c.get_username(), 'text':c.text} for c in obj.comments.all()]
        return HttpResponse(simplejson.dumps(comments), mimetype="application/json")
    else:
        return HttpResponseRedirect("../posted/?c=%s:%s" % (content_type_id, object_id))


def comment_was_posted(request):
    """
    Display "comment was posted" success page

    Templates: `comment_posted`
    Context:
        object
            The object the comment was posted on
    """
    obj = None
    if 'c' in request.GET:
        content_type_id, object_id = request.GET['c'].split(':')
        try:
            content_type = ContentType.objects.get(pk=content_type_id)
            obj = content_type.get_object_for_this_type(pk=object_id)
        except (ObjectDoesNotExist, ValueError):
            pass
    return render_to_response('comments/posted.html', {'object': obj}, context_instance=RequestContext(request))

