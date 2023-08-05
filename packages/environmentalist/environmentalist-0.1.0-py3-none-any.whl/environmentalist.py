"""Environmentalist helps devs to retrive API secrets from the environment."""
import collections
import os


class E(collections.UserDict):
    """Use an instance to easily create your API instance, for example:

        # bash
        set TWITTER_CLIENT_KEY = xxx
        set TWITTER_CLIENT_SECRET = xxx
        set TWITTER_RESOURCE_OWNER_TOKEN = xxx
        set TWITTER_RESOURCE_OWNER_SECRET = xxx

        # python
        from environmentalist import E
        from requests_oauthlib import OAuth1Session
        api = OAuth1Session(**E(prefix='TWITTER'))
        api.get('https://api.twitter.com/1.1/statuses/home_timeline.json')

    Or you can dump all the environment variables. This will not change the environment
    variables to lower case:

        print(E())
        # {'HOME': '...', ...}

    :param prefix: This is used to filter the environment variables. If not set,
                   this class is simply a copy of the current os.environ.
    """

    def __init__(self, prefix=None):
        self._prefix = prefix
        if prefix:
            self.data = {key.lstrip(prefix + '_').lower(): val
                         for key, val
                         in os.environ.items()
                         if key.startswith(prefix)}
        else:
            self.data = {key: val for key, val in os.environ.items()}
