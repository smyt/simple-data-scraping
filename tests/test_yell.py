"""test's module."""
import unittest
import urllib.request

from lxml import etree

from scrapy_parser.yellparser.spiders.yell_spider import YellSpider


class YellSiteTest(unittest.TestCase):
    """Public Yell Site class test for checking source html site."""

    BASE_URL = 'https://www.yell.ru/'

    def _check_assert(self, condition, key):
        try:
            self.assertTrue(condition)
        except AssertionError:
            print('Error in structure source html site. Error in key: {}'.format(key))
            raise

    def test_source_html_structure(self):
        """Check html structure of source site."""
        # get first company in company list
        url_category = '{}moscow/top/fitnes-kluby/'.format(self.BASE_URL)
        category_page_content = urllib.request.urlopen(url_category).read()
        tree = etree.HTML(category_page_content)
        category_urls = tree.xpath('//div[@class="companies"]'
                                   '/div[@class="companies__item clearfix"]'
                                   '//h4/a/@href')
        self.assertTrue(len(category_urls) > 1)
        url_page = "{}{}".format(self.BASE_URL, category_urls[0])
        # parse page of first company
        page_content = urllib.request.urlopen(url_page).read().decode('utf-8')
        tree = etree.HTML(page_content)
        is_b_center = True if tree.xpath('//div[@ng-controller="Bcenter"]') else False
        xpaths = YellSpider.company_xpaths if not is_b_center else YellSpider.bizcenter_xpaths
        for key, value in xpaths.items():
            # not required fields
            if key not in ('site_redirect_url', 'metro', 'avg_check', 'is_closed'):
                param = tree.xpath(value)
                self._check_assert(len(param) > 0, key)
