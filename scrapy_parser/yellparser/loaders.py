"""YellSpider loader and useful functions."""
import re
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose, MapCompose
from urllib.parse import urlparse, parse_qs
from w3lib.html import strip_html5_whitespace, replace_tags


def get_site_url(value):
    """Get url from string."""
    if value:
        site_redirect_url = urlparse(value[0].strip())
        qs_url = parse_qs(site_redirect_url.query).get('url')
        if qs_url:
            value = qs_url[0]
    return value


def get_coords(init_str):
    """Get coordinates from input string."""
    match = re.search(r'^[^(]+\((.+)\)$', init_str)
    json_str = match.group(1)
    map_dict = json.loads(json_str)
    point = map_dict.get('points')
    coords = ""
    if point:
        point = point[0]
        coords = "{},{}".format(point['lat'], point['lng'])
    return coords


def get_true_or_false(value):
    """Get true or false from input string."""
    return value is not None and len(value) > 0


class CompanyLoader(ItemLoader):
    """Scrapy CompanyLoader."""

    default_input_processor = MapCompose(strip_html5_whitespace)
    default_output_processor = TakeFirst()
    category_out = Join('|')
    site_url_out = Compose(TakeFirst(), get_site_url)
    phones_out = Compose(set, Join(','))
    metro_out = Join(',')
    district_in = MapCompose(replace_tags)
    addr_in = MapCompose(replace_tags)
    addr_out = Join(',')
    services_out = Join(',')
    coords_out = Compose(TakeFirst(), get_coords)
    is_closed_out = Compose(TakeFirst(), get_true_or_false)
