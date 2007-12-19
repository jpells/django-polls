from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from tagging.fields import TagField
from published_manager.managers import PublishedManager
from django.utils.translation import ugettext as _

class Poll(models.Model):
    """
    A poll 
    """
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True, help_text=_("Not Required"))
    slug = models.SlugField(prepopulate_from=('title',), unique=True, verbose_name=_("Slug Field"))
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Published"))
    user = models.ForeignKey(User, verbose_name=_("User"))
    state = models.CharField(max_length=1, choices=settings.STATE_CHOICES, default=settings.STATE_DEFAULT, verbose_name=_("State of object"))
    ip_address = models.IPAddressField(verbose_name=_("Author's IP Address"))
    tags = TagField(help_text=_("Enter key terms seperated with a space that you want to associate with this Poll"), verbose_name=_("Tags"))
    objects = models.Manager()
    published_objects = PublishedManager()

    def get_choices_tuple(self):
        choices = Choice.objects.with_counts(poll_id=self.id, as_dict=False)
        choice_tuple = ((choice.id, choice.choice, choice.vote_count) for choice in choices)
        return choice_tuple

    def get_absolute_url(self):
        return "/polls/%s/" % self.slug

    def __unicode__(self):
        return _(self.title)

    class Meta:
        ordering = ['pub_date']
        get_latest_by = "pub_date"
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")

    class Admin:
        date_hierarchy = 'pub_date'
        list_display = ('title', 'user')
        ordering = ['pub_date']
        search_fields = ['title']
        fields = (
            (None, {
                'fields': ('title', 'description', 'user', 'ip_address')
            }),
            (_('Advanced settings'), {
                'classes': 'collapse',
                'fields' : ('state', 'slug', 'pub_date')
            }),
        )

class ChoiceManager(models.Manager):
    def with_counts(self, poll_id, as_dict):
        from django.db import connection
        cursor = connection.cursor()
        #TODO fix for postgres
        cursor.execute("SELECT a.poll_id, a.id, a.choice, ifnull(i.num_votes, 0) vote_count from polls_choice a left outer join (select c.poll_id, c.choice, count(*) num_votes from polls_choice c, polls_vote v where c.poll_id = v.poll_id and c.id = v.choice_id group by c.choice) i on a.choice = i.choice where a.poll_id = %s;", [poll_id])
        result_list = []
        for row in cursor.fetchall():
            c = self.model(id=row[1], choice=row[2], poll_id=row[0])
            c.vote_count = row[3]
            result_list.append(c)
        result_dict = {}
        if as_dict:
            counter = 0
            for choice in result_list:
                choice_dict = {'choice': choice.choice, 'vote_count': choice.vote_count}
                result_dict.update({counter: choice_dict})
                counter += 1
            return result_dict
        return result_list

class Choice(models.Model):
    """
    A choice 
    """
    poll = models.ForeignKey(Poll, null=False, blank=False, verbose_name=_("Poll"), edit_inline=models.TABULAR, num_in_admin=5)
    choice = models.CharField(max_length=200, verbose_name=_("Choice"), core=True)
    objects = ChoiceManager()

    def __unicode__(self):
        return _(self.choice)

    def get_vote_count(self):
        return Vote.objects.filter(choice=self).count()

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

class Vote(models.Model):
    """
    A vote
    """
    poll = models.ForeignKey(Poll, verbose_name=_("Poll"))
    choice = models.ForeignKey(Choice, radio_admin=True, verbose_name=_("Choice"))
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Published"))
    user = models.ForeignKey(User, verbose_name=_("User"), related_name='polls_vote')
    ip_address = models.IPAddressField(verbose_name=_("Author's IP Address"))

    def __unicode__(self):
        return _(self.choice.choice)

    class Meta:
        unique_together = (("user", "poll"),)
        ordering = ['pub_date']
        get_latest_by = "pub_date"
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

    class Admin:
        date_hierarchy = 'pub_date'
        list_display = ('poll', 'choice', 'user')
        ordering = ['pub_date']
        search_fields = ['poll']
        fields = (
            (None, {
                'fields': ('poll', 'choice', 'user', 'ip_address')
            }),
            (_('Advanced settings'), {
                'classes': 'collapse',
                'fields' : ('pub_date', )
            }),
        )
