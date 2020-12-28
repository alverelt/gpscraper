# gp_scraper

Google Play scraper.

## Example usage.

```python
from gp_scraper import GPScraper

gp = GPScraper('es')

# Example 1.
reviews = [r for r in gp.reviews('com.github.android')]

#Example 2 (Optional args).
optional = {
	'pagination_delay': 0,
	'review_size': 100
}
reviews = [r for r in gp.reviews('com.github.android', **optional)]
```

## TODO
- App details scraper.

- App searching scraper.

- Scrape by sorting type.
