# gpscraper

Google Play scraper.

## Example usage.

```python
from gpscraper import GPScraper, Sort

gp = GPScraper('es')

# Scraping app details
details = gp.app_details('com.github.android')

# Scraping reviews example 1.
reviews = [r for r in gp.reviews('com.github.android')]

#Scraping reviews example 2 (Optional args).
optional = {
        'count_pages': 10,
	'review_size': 100,
	'sort_type': Sort.RATING,
	'sort_score': 5
}
reviews = [r for r in gp.reviews('com.github.android', **optional)]
```

## TODO
- App searching scraper.
