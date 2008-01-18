from django.template import resolve_variable
from django import newforms as forms
from polls.models import Poll, Vote
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings

def get_poll_dict(context, slug=None):
    user = resolve_variable('user', context)
    ip_address = resolve_variable('request.META.REMOTE_ADDR', context)
    template_dict = context 
    template_dict.update({'poll_exists': True, 'already_voted': False, 'user': user, 'MEDIA_URL': settings.MEDIA_URL, 'not_auth': False})
    try:
        if slug != None:
            poll = get_object_or_404(Poll, slug=slug)
        else:
            poll = Poll.published_objects.all().latest('pub_date')
        if poll == None:
            raise Http404
        if int(poll.state) != settings.STATE_PUBLISHED:
            raise Http404
        template_dict.update({'poll': poll})
        VoteForm = forms.models.form_for_model(Vote)
        VoteForm.base_fields['choice'].widget = forms.widgets.RadioSelect(choices=((choice.id, choice.choice) for choice in poll.choice_set.all()))
        VoteForm.base_fields['choice'].required = True
        VoteForm.base_fields['user'].widget = forms.widgets.HiddenInput()
        VoteForm.base_fields['user'].initial = user.id
        VoteForm.base_fields['ip_address'].widget = forms.widgets.HiddenInput()
        VoteForm.base_fields['ip_address'].initial = ip_address 
        VoteForm.base_fields['poll'].widget = forms.widgets.HiddenInput()
        VoteForm.base_fields['poll'].initial = poll.id
        VoteForm.base_fields.update({'slug': forms.CharField()})
        VoteForm.base_fields['slug'].widget = forms.widgets.HiddenInput()
        VoteForm.base_fields['slug'].initial = poll.slug
        form = VoteForm()
        template_dict.update({'form': form})
        if user.is_authenticated() and Vote.objects.filter(poll=poll).filter(user=user):
            template_dict.update({'already_voted': True})
    except Poll.DoesNotExist:
        template_dict.update({'poll_exists': False})
    return template_dict

