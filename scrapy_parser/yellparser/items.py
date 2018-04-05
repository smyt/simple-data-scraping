"""Scrapy items."""
import scrapy


class CompanyItem(scrapy.Item):
    """Company item.

    Describe all parsing fields.
    """

    link = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    site_url = scrapy.Field()
    addr = scrapy.Field()
    phones = scrapy.Field()
    metro = scrapy.Field()
    district = scrapy.Field()
    services = scrapy.Field()
    avg_check = scrapy.Field()
    coords = scrapy.Field()
    is_closed = scrapy.Field()
