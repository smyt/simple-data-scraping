# -*- coding: utf-8 -*-

"""Scrapy module of item pipelines.

Don't forget to add your pipeline to the ITEM_PIPELINES setting
See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""


class YellparserPipeline(object):
    """YellparserPipeline item."""

    def process_item(self, item, spider):
        """Without additional processing."""
        return item
