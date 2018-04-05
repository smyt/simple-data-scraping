"""Yell spider module."""
import scrapy
from scrapy.http.request import Request

from app.company_list import CompanyList
from scrapy_parser.yellparser.items import CompanyItem
from scrapy_parser.yellparser.loaders import CompanyLoader


class YellSpider(scrapy.Spider):
    """YellSpider spider class."""

    name = "yell"

    bizcenter_xpaths = {
        'name': '//div[@class="bcenter__title"]/h1/text()',
        'rating': '//span[@itemprop="ratingValue"]/text()',
        'site_redirect_url': '//div[@class="bcenter__contacts"]/descendant::a/@href',
        'addr': '//div[@class="bcenter__location"]/div[1]/descendant::*/text()',
        'metro': '//div[@class="bcenter__location"]/div[2]'
                 '//div[@class="bcenter__contacts-popup-item"]/text()',
        'district': '//div[@class="bcenter__location"]/div[3]/'
                    'span[2]/text()',
        'phones': '//div[@class="bcenter__contacts"]/'
                  'div[@class="bcenter__contacts-item"][1]/descendant::*/text()',
        'coords': '//div[@class="bcenter__map-container"]/@ng-init',
    }

    company_xpaths = {
        'name': '//div[@class="company__title"]//*[@itemprop="name"]/text()',
        # 'rating': '//span[@itemprop="ratingValue"]/text()',
        'rating': '//span[@class="rating__value"]/text()',
        'site_redirect_url': '//div[@class="company__contacts"]'
                             '/div[1]//a/@href',
        'addr': '//div[@class="company__contacts"]'
                '//span[@itemprop="address"]',
        'metro': '//div[@class="company__contacts"]'
                 '//div[@id="contacts-metro"]/descendant::*/text()',
        'district': '//div[@class="company__contacts"]'
                    '/div[2]/div[3]'
                    '/span[@class="company__contacts-item-text"]',
        'phones': '//div[@class="company__contacts"]'
                  '//*[@itemprop="telephone"]/text()',
        'category': '//div[@class="breadcrumbs"]/*/a/span/text()',
        'services': '//div[@class="company__about"]'
                    '/div[contains(@class,"company__custom-fields")]'
                    '/descendant::*/text()',
        'avg_check': '//div[@class="company__about"]'
                     '/div[@class="company__avg-check"]'
                     '/descendant::*/text()',
        'coords': '//div[@class="company__map-container"]/@ng-click',
        'is_closed': '//div[@class="company__status alert alert_danger"]'
    }

    def __init__(self, name=None, **kwargs):
        """It's YellSpider parser constructor."""
        super().__init__(name, **kwargs)
        self.urls = kwargs.get('urls').split(',')
        self.type_parsing = kwargs.get('type_parsing')

    def start_requests(self):
        """Start parsing requests."""
        for url in self.urls:
            companies = CompanyList(self.type_parsing)(url, self.parse)
            yield Request(companies.url, callback=companies.proccess)

    def get_xpaths(self, response):
        """Get xpath's type of company page.

        There are two types of company page known.
        """
        if response.xpath('//div[@ng-controller="Bcenter"]').extract():
            xpaths = self.bizcenter_xpaths
        else:
            xpaths = self.company_xpaths
        return xpaths

    def parse(self, response):
        """Parse company item."""
        xpaths = self.get_xpaths(response)

        loader = CompanyLoader(item=CompanyItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', xpaths['name'])
        loader.add_xpath('category', xpaths['category'])
        loader.add_xpath('rating', xpaths['rating'])
        loader.add_xpath('site_url', xpaths['site_redirect_url'])
        loader.add_xpath('addr', xpaths['addr'])
        loader.add_xpath('phones', xpaths['phones'])
        loader.add_xpath('metro', xpaths['metro'])
        loader.add_xpath('district', xpaths['district'])
        loader.add_xpath('services', xpaths['services'])
        loader.add_xpath('avg_check', xpaths['avg_check'])
        loader.add_xpath('coords', xpaths['coords'])
        loader.add_xpath('is_closed', xpaths['is_closed'])
        return loader.load_item()
