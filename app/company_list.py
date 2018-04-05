"""Two methods of getting company list."""
from scrapy import Request

from app import app
from app.forms import DownloadForm


class CompanyBaseList:
    """Base class for list company."""

    def __init__(self, url, callback):
        """Override normal behavior."""
        self.url = url
        self.callback = callback
        self.host = app.config['HOST_PARSING']


class CompanySitemapList(CompanyBaseList):
    """Company list is getting by sitemap."""

    def __init__(self, url, callback):
        """Override base behavior."""
        super().__init__(url, callback)
        self.url = self.url_to_sitemap()

    def url_to_sitemap(self):
        """Get sitemap url for companies."""
        from app.utils import get_city_category_from_url
        city, category = get_city_category_from_url(self.url)
        return '{}/sitemap/{}/{}/companies.xml'.format(self.host, city, category)

    def proccess(self, response):
        """Parse companies."""
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        links = response.xpath('//sitemap:loc/text()', namespaces=ns).extract()

        for link in links:
            request = Request(link, callback=self.callback)
            yield request


class CompanyHtmlList(CompanyBaseList):
    """Company list is getting by html parse."""

    def proccess(self, response):
        """Parse companies."""
        for link in response.xpath('//div[@class="companies"]'
                                   '/div[@class="companies__item clearfix"]'
                                   '//h4/a/@href'):
            link = link.extract()
            if not link.startswith('/'):
                continue
            link = '{}{}'.format(self.host, link)
            request = Request(link, callback=self.callback)
            yield request

        goto_pages = response.xpath('//div[@class="category__companies-more"]/a[@rel="next"]/@href').extract()
        if goto_pages:
            next_page_link = self.host + goto_pages[-1] + '&rel=next'
            request = Request(next_page_link, callback=self.proccess)
            yield request


class CompanyList:
    """Class for choosing type of parsing."""

    def __init__(self, type_parsing):
        """Class constructor."""
        self.type_parsing = type_parsing

    def __call__(self, *args, **kwargs):
        """Behavior of calling object class."""
        if self.type_parsing == DownloadForm.CHOICES_TYPE_PARCING[0][0]:
            return CompanyHtmlList(*args, **kwargs)
        return CompanySitemapList(*args, **kwargs)
