# gpscraper

Welcome to this Google Play scraper.

- With the `search` generator method you will be able to gather information from all results according to your input query.

**Example**
```python
import gpscraper as gp

searches = [s for s in gp.search('github')]

```

And get something like this

```python
[{'search': [{'icon': 'https://play-lh.googleusercontent.com/PCpXdqvUWfCW1mXhH1Y_98yBpgsWxuTSTofy3NGMo9yBTATDyzVkqU580bfSln50bFU',
    'title': 'GitHub',
    'offered_by': 'GitHub',
    'developer': {'more_apps': '/store/apps/developer?id=GitHub'},
    'description': 'Triage notifications, review, comment, and merge, right from your mobile device',
    'rating': ['4.7', 4.650081],
    'app_id': 'com.github.android'},
   {'icon': 'https://play-lh.googleusercontent.com/XP-tvaGf-as9XMQ3kcUjohSZlSD7uyf_AcHsjq6jTI0chXWK1yQrnJJs2Y_Pvbe1FRQ',
    'title': 'OpenHub for GitHub',
    'offered_by': 'ThirtyDegreesRay',
    'developer': {'more_apps': '/store/apps/developer?id=ThirtyDegreesRay'},
    'description': 'An open source GitHub client app, faster and concise.',
    'rating': ['4.1', 4.142857],
    'app_id': 'com.thirtydegreesray.openhub'},
   {...}],
  'next': {'query': 'github',
   'token': 'Cgj6noGdAwIIChAKGguCAQgKBmdpdGh1YjoOCggKBmdpdGh1YhAAGAc',
   'unknown_1': '[10,[10,50]],true,...',
   'pagination_delay': 1,
   'lang': 'us'}}]
```

You may have noticed the `next` field, that is because each pagination contains a token for the next results, also `search` retrieves all results it finds, so if you break in a loop and want to continue from the last results found, you can do something like this:

```python
for s in gp.search(**searches[-1]['next']):
    searches.append(s)
```
