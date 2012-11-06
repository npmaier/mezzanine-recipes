
from mezzanine.twitter.templatetags.twitter_tags import tweets_for
from mezzanine.conf import settings
from mezzanine import template

register = template.Library()

@register.as_tag
def tweets_default(*args):
    """
    Tweets for the default settings.
    """
    settings.use_editable()
    query_type = settings.TWITTER_DEFAULT_QUERY_TYPE
    args = (settings.TWITTER_DEFAULT_QUERY,
            settings.TWITTER_DEFAULT_NUM_TWEETS)
    return tweets_for(query_type, args)
