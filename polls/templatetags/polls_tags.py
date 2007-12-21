from django.template import Library, Node, loader, Context
from polls.utils import get_poll_dict

register = Library()

class LatestPollNode(Node):
    def __init__(self):
        pass
    def render(self, context):
        t = loader.get_template('polls/vote_form_ajax.html')
        c = Context(get_poll_dict(context))
        return t.render(c)

def latest_poll(parser, token):
    return LatestPollNode()

register.tag('latest_poll', latest_poll)

