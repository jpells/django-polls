from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import newforms as forms
from django.template import RequestContext
from django.template.defaultfilters import slugify
from polls.models import Poll, Vote, Choice
from django.conf import settings
from django.contrib.auth.decorators import login_required
from polls.utils import get_poll_dict 

def poll_form(request):
    PollFormClass = forms.models.form_for_model(Poll) 
    PollFormClass.base_fields['slug'].widget = forms.widgets.HiddenInput()
    PollFormClass.base_fields['slug'].required = False
    PollFormClass.base_fields['user'].widget = forms.widgets.HiddenInput()
    PollFormClass.base_fields['user'].initial = request.user.id
    PollFormClass.base_fields['ip_address'].widget = forms.widgets.HiddenInput()
    PollFormClass.base_fields['ip_address'].initial = request.META['REMOTE_ADDR'] 
    PollFormClass.base_fields['state'].widget = forms.widgets.HiddenInput()
    PollFormClass.base_fields['state'].initial = settings.STATE_DEFAULT
    PollFormClass.base_fields['choice_count'] = forms.CharField(widget=forms.widgets.HiddenInput(), initial=settings.POLL_DEFAULT_CHOICE_COUNT)
    ChoiceFormClass = forms.models.form_for_model(Choice)
    ChoiceFormClass.base_fields['poll'].widget = forms.widgets.HiddenInput()
    ChoiceFormClass.base_fields['poll'].required = False
    choice_forms = []
    if request.POST:
        poll_form = PollFormClass(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.slug = slugify(poll.title)
            poll.save()
            for i in range(int(request.POST['choice_count'])+1):
                choice_form = ChoiceFormClass(request.POST, prefix='choice'+str(i))
                if choice_form.is_valid():
                    choice = choice_form.save(commit=False)
                    choice.poll = poll
                    choice.save()
                choice_forms.append(choice_form)
            if settings.STATE_DEFAULT != settings.STATE_PUBLISHED:
                return HttpResponseRedirect('/polls/posted/')
            else:
                return HttpResponseRedirect(poll.get_absolute_url())
    else:
        poll_form = PollFormClass()
        for i in range(settings.POLL_DEFAULT_CHOICE_COUNT):
            choice_form = ChoiceFormClass(prefix='choice'+str(i))
            choice_forms.append(choice_form)
    return render_to_response('polls/poll_form.html', {'poll_form': poll_form, 'choice_forms': choice_forms}, context_instance=RequestContext(request))
poll_form = login_required(poll_form)

def ajax_refresh(request):
    return render_to_response('polls/vote_form_ajax.html', get_poll_dict(RequestContext(request)), context_instance=RequestContext(request))

def vote_form(request, slug):
    if request.POST:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/?next='+request.META['PATH_INFO'])
        VoteFormClass = forms.models.form_for_model(Vote)
        vote_form = VoteFormClass(request.POST)
        if vote_form.is_valid():
            vote = vote_form.save(commit=False)
            vote.poll = Poll.objects.get(slug=slug)
            vote.save()
    return render_to_response('polls/vote_form.html', get_poll_dict(RequestContext(request), slug), context_instance=RequestContext(request))
