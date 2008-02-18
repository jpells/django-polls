from polls.models import Poll
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _

class RssFeed(Feed):
    title = _("Polls")
    link = "/polls/" 
    description = _("Polls")
    def items(self):
        return Poll.published_objects.all().order_by('-pub_date')[:5]

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
