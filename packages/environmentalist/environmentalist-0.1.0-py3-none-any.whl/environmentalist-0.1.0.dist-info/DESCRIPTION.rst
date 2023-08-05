# Environmentalist - use API secrets easily

Environmentalist helps API users to retrive API secrets from the environment
easily.

## The problem

I'm tired of rewriting the following code over and over again to get my app key
from the environment variables.

```python
import os
from requests_oauthlib import OAuth1Session
api = OAuth1Session(client_key=os.environ.get('TWITTER_CLIENT_KEY'),
                    client_secret=os.environ.get('TWITTER_CLIENT_SECRET'),
                    resource_owner_token=os.environ.get('TWITTER_RESOURCE_OWNER_TOKEN'),
                    resource_owner_secret=os.environ.get('TWITTER_RESOURCE_OWNER_SECRET'))
```

## Project dependencies

1. N/A

## Usage

Use an instance to easily create your API instance, for example:

```bash
# Create environment variables with the same prefix
set TWITTER_CLIENT_KEY=xxx
set TWITTER_CLIENT_SECRET=xxx
set TWITTER_RESOURCE_OWNER_TOKEN=xxx
set TWITTER_RESOURCE_OWNER_SECRET=xxx
```

```python
from environmentalist import E

api = OAuth1Session(**E(prefix='TWITTER'))

api.get('https://api.twitter.com/1.1/statuses/home_timeline.json')
```

When you create the `E` instance, it filter and strips the prefix out of the
environment variables.

Or you can dump all the environment variables for no reason:

```python
print(E())
# {'HOME': '...', ...}
```


