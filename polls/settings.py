"""
Convenience module for access of custom poll application settings,
which enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

_ = lambda s: s

# The choices for state of a Poll
STATE_CHOICES = getattr(settings, 'STATE_CHOICES', (
    ('1', _('Draft')),
    ('2', _('Published')),
    ('3', _('Inactive')),
))

# The default state when a Poll is created
STATE_DEFAULT = getattr(settings, 'STATE_DEFAULT', 3)

# The state of a Published Poll
STATE_PUBLISHED = getattr(settings, 'STATE_PUBLISHED', 2)

# The default number of Choices given when a Poll is created
POLL_DEFAULT_CHOICE_COUNT = getattr(settings, 'POLL_DEFAULT_CHOICE_COUNT', 3)