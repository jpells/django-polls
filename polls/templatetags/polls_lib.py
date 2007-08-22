from django import template
from django import newforms as forms
from polls.models import Poll, Vote
from django.conf import settings

register = template.Library()

def get_latest_poll(user, ip_address):
    template_dict = {}
    template_dict.update({'poll_exists': True, 'already_voted': False, 'user': user, 'MEDIA_URL': settings.MEDIA_URL, 'not_auth': False})
    try:
        poll = Poll.published_objects.all().latest('pub_date')
        template_dict.update({'poll': poll})
        template_dict.update({'choice_tuple': poll.get_choices_tuple()})
        VoteForm = forms.form_for_model(Vote)
        VoteForm = forms.models.form_for_model(Vote)
        VoteForm.base_fields['choice'].widget = forms.widgets.RadioSelect(choices=poll.get_choices_tuple())
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
        if not user.is_authenticated():
            template_dict.update({'not_auth': True})
    except Poll.DoesNotExist:
        template_dict.update({'poll_exists': False})
    return template_dict

register.inclusion_tag('polls/poll_form_ajax.html')(get_latest_poll)
