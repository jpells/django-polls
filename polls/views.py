from django.shortcuts import get_object_or_404, render_to_response, HttpResponse
from django.http import HttpResponseRedirect
from django.utils import simplejson 
from django import oldforms
from django import newforms as forms
from django.template import RequestContext
from django.template.defaultfilters import slugify
from polls.models import Poll, Vote, Choice
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import simplejson
from django.core import serializers
from polls.templatetags.polls_lib import get_latest_poll 

"""def poll_form(request):
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
            for i in range(int(request.POST['choice_count'])):
                choice_form = ChoiceFormClass(request.POST, prefix='choice'+str(i))
                if choice_form.is_valid():
                    choice = choice_form.save(commit=False)
                    choice.poll = poll
                    choice.save()
                choice_forms.append(choice_form)
            return HttpResponseRedirect(poll.get_absolute_url())
    else:
        poll_form = PollFormClass()
        for i in range(settings.POLL_DEFAULT_CHOICE_COUNT):
            choice_form = ChoiceFormClass(prefix='choice'+str(i))
            choice_forms.append(choice_form)
    return render_to_response('polls/poll_form.html', {'poll_form': poll_form, 'choice_forms': choice_forms}, context_instance=RequestContext(request))
poll_form = login_required(poll_form)"""

def ajax_refresh(request):
    return render_to_response('polls/poll_form_ajax.html', get_latest_poll(request.user, request.META['REMOTE_ADDR']), context_instance=RequestContext(request))

def vote_form(request, poll_id=None, slug=None):
    for key in request.POST.keys():
        print key
    return render_to_response('polls/vote_form.html', context_instance=RequestContext(request))
"""    xhr = request.GET.has_key('xhr')
    response_dict = {}
    response_dict_xhr = {}
    if poll_id != None:
        poll = get_object_or_404(Poll, pk=poll_id)
    elif slug != None:
        poll = get_object_or_404(Poll, slug=slug)
    if poll == None:
        raise Http404
    if int(poll.state) != settings.STATE_PUBLISHED:
        raise Http404
    response_dict.update({'poll': poll})
    poll_dict = {'id': poll.id}
    response_dict_xhr.update({'poll': poll_dict})
    if request.user.is_authenticated() and Vote.objects.filter(poll=poll).filter(user=request.user):
        choices_with_counts = Choice.objects.with_counts(poll.id, True)
        response_dict.update({'already_voted': True})
        response_dict.update({'choices': choices_with_counts})
        response_dict_xhr.update({'already_voted': True})
        response_dict_xhr.update({'choices': choices_with_counts})
        if xhr:
            return  HttpResponse(simplejson.dumps(response_dict_xhr), mimetype='application/javascript')
#            return HttpResponse(serializers.serialize("xml", response_dict), mimetype='application/xml')
        return render_to_response('polls/vote_form.html', response_dict, context_instance=RequestContext(request))
    VoteFormClass = forms.models.form_for_model(Vote)
    VoteFormClass.base_fields['choice'].widget = forms.widgets.RadioSelect(choices=poll.get_choices_tuple())
    VoteFormClass.base_fields['choice'].required = True
    VoteFormClass.base_fields['user'].widget = forms.widgets.HiddenInput()
    VoteFormClass.base_fields['user'].initial = request.user.id
    VoteFormClass.base_fields['ip_address'].widget = forms.widgets.HiddenInput()
    VoteFormClass.base_fields['ip_address'].initial = request.META['REMOTE_ADDR'] 
    VoteFormClass.base_fields['ip_address'].required = False
    VoteFormClass.base_fields['poll'].widget = forms.widgets.HiddenInput()
    VoteFormClass.base_fields['poll'].required = False
    if request.POST:
        vote_form = VoteFormClass(request.POST)
        if vote_form.is_valid():
            vote = vote_form.save(commit=False)
            vote.poll = poll 
            vote.save()
            if xhr:
                choices_with_counts = Choice.objects.with_counts(poll.id)
                response_dict.update({'already_voted': True})
                response_dict.update({'choices': choices_with_counts})
                return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
#                return HttpResponse(serializers.serialize("xml", response_dict), mimetype='application/xml')
            return HttpResponseRedirect(poll.get_absolute_url())
    else:
        vote_form = VoteFormClass()
    response_dict.update({'vote_form': vote_form})
    if xhr:
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
#        return HttpResponse(serializers.serialize("xml", response_dict), mimetype='application/xml')
    return render_to_response('polls/vote_form.html', {'poll': poll, 'vote_form': vote_form}, context_instance=RequestContext(request))"""
