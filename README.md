# gp_scraper

Google Play scraper.

## Example usage.

```python
from gp_scraper import GPReviews as gpr

# Example 1.
reviews = [r for r in gpr.scrape('com.github.android')]

#Example 2 (Optional args).
optional = {
	'pagination_delay': 0,
	'review_size': 100
}
reviews = [e for r in gpr.scrape('com.github.android', **optional)]
```

## TODO
- App scraper.

- Scrape by sorting type.
