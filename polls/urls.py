from django.conf.urls.defaults import *
from polls.feeds import RssFeed, AtomFeed
from polls.models import Poll, Vote
from django.conf import settings

feeds = { 
    'rss': RssFeed,
    'atom': AtomFeed,
}

poll_dict = {
    'model': Poll,
    'base_url': '/polls/',
}

vote_dict = {
    'model': Vote,
    'base_url': '/polls/votes/',
}

urlpatterns = patterns('',
    (r'^rss/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds, 'url': 'rss'}),
    (r'^atom/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds, 'url': 'atom'}),
)

urlpatterns += patterns('sorted_paginated_authored_archived_list_view.views',
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'sorted_paginated_authored_archived_list', poll_dict),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'sorted_paginated_authored_archived_list', poll_dict),
    (r'^(?P<year>\d{4})/$', 'sorted_paginated_authored_archived_list', poll_dict),
    (r'^$', 'sorted_paginated_authored_archived_list', poll_dict),
    (r'^votes/$', 'sorted_paginated_authored_archived_list', vote_dict),
    # if votes were really archived there would be more urls here
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^posted/$', 'direct_to_template', dict(template='polls/posted.html')),
)

urlpatterns += patterns('polls.views',
    (r'^create/$', 'poll_form'),
    (r'^ajaxrefresh/$', 'ajax_refresh'),
    (r'^(?P<slug>[-\w]+)/$', 'vote_form'),
)

