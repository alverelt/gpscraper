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
[{'search': [{'icon': 'https://play-lh.googleusercontent.com/PCpXdqvUWfCW1mXhH1Y...',
    'title': 'GitHub',
    'offered_by': 'GitHub',
    'developer': {'more_apps': '/store/apps/developer?id=GitHub'},
    'description': 'Triage notifications, review, comment, and merge, right from your mobile device',
    'rating': ['4.7', 4.650081],
    'app_id': 'com.github.android'},
   {'icon': 'https://play-lh.googleusercontent.com/XP-tvaGf-as9XMQ3kcUjohSZlSD7...',
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

- With the `details` method you will gather lots of information from an specific application.

**Example**
```python
import gpscraper as gp

details = gp.details('com.github.android')
```

And get something like this
```python
{'title': 'GitHub',
 'description': 'There’s a lot you can do on GitHub that doesn’t require a complex ...',
 'screenshots': ['https://play-lh.googleusercontent.com/_x8EKTsswQFtmxc3p_zkfY3b2qgTZkCduy...',
  'https://play-lh.googleusercontent.com/oJIO3RRu9DWOnf-BMGcgiJDU7h9EQD0Z5SOEzaHF4sRhdr9UQ...',
  'https://play-lh.googleusercontent.com/UY_55o3qfR7C-5_795DeEQBM_kpbWOOOjYVzljSXSRy2Qfza_z...',
  'https://play-lh.googleusercontent.com/BP7LyjN7Zp9EBQn0wuosZZgAF7n73pBL5Isww_Zzg8YNgY0iaw...'],
 'icon': 'https://play-lh.googleusercontent.com/PCpXdqvUWfCW1mXhH1Y_98yBpgsWxuTSTofy3NGMo9y...',
 'additional_info': {'offered_by': 'GitHub',
  'installs': ['1,000,000+', 1000000, 1452118, '1M+'],
  'interactive_elements': 'Users Interact',
  'in_app_products': None,
  'content_rating': ['Everyone'],
  'updated': 'February 17, 2021',
  'app_size': '9.7M',
  'current_version': '1.4.9',
  'requires_android': '6.0 and up',
  'developer': {'site': 'https://github.com/mobile',
   'mailto': 'mobilefeedback+android@github.com',
   'more_apps': '/store/apps/developer?id=GitHub',
   'privacy_policy': 'https://help.github.com/en/articles/github-privacy-statement',
   'address': None}},
 'editors_choice': False,
 'whats_new': 'Introducing Sponsors! A new button in the profile section now reveals...',
 'category': 'PRODUCTIVITY',
 'released': 'Feb 15, 2020',
 'esrb': {'description': 'Everyone',
  'icon': 'https://play-lh.googleusercontent.com/OBVqgRK7eerY0GPfK8AOzitu5oE9ecC6kG4kU...'},
 'prices': {'normal': {'raw': 0, 'currency': 'USD', 'formatted': ''},
  'offer': None},
 'rating_value': ['4.7', 4.650081],
 'histogram': {'1': 344, '2': 285, '3': 767, '4': 2596, '5': 14193},
 'rating_count': 18187}
```
