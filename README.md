# gp_scraper

Google Play scraper.

## Example usage.

```python
from gp_scraper import GPScraper
from gp_scraper import Sort

gp = GPScraper('es')

# Scraping app details
details = gp.app_details('com.github.android')

# Scraping reviews example 1.
reviews = [r for r in gp.reviews('com.github.android')]

#Scraping reviews example 2 (Optional args).
optional = {	
	'review_size': 100,
	'sort_type': Sort.RATING,
	'sort_score': 5
}
reviews = [r for r in gp.reviews('com.github.android', **optional)]
```

## TODO
- App searching scraper.
