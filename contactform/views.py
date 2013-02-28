from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail('Message sent using jeepblog web form', form.cleaned_data['message'],
                      '%s <%s>' % (form.cleaned_data['name'],form.cleaned_data['email']), settings.ADMINS, fail_silently=False)
            return HttpResponseRedirect('/contact-me/done/')
    else:
        form = ContactForm()

    return render_to_response( 'contactform/contact_me.html',
                               {'form' : form,},
                               context_instance=RequestContext(request) )

def done(request):
    return render_to_response( 'contactform/done.html',
                               context_instance=RequestContext(request) )
