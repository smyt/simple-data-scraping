"""Useful utils for project."""
import os
import uuid
import zipfile
from io import BytesIO

from flask_mail import Message
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from app import app, mail, logger
from app.forms import DownloadForm


def get_city_category_from_url(url):
    """Get city and category from url."""
    from urllib.parse import urlparse
    url_ob = urlparse(url)
    assert url_ob.query == ''
    url_parts = [part for part in url_ob.path.split('/') if part]
    assert len(url_parts) == 3
    city, category = url_parts[0], url_parts[-1]
    return city, category


def generate_email_filename(city, category):
    """Generate pretty filename of email attachment."""
    from datetime import datetime
    return "parsing-{}-{}-{}.csv".format(city, category, datetime.now().strftime("%Y%m%d-%H%M%S"))


def start_task(url, type_parsing=DownloadForm.CHOICES_TYPE_PARCING[1][0], email=None):
    """Start Main method of processing, start parsing and send results on email after parse."""
    is_need_compress = app.config.get('COMPRESS_FILE', False)
    result_filename = start_parser(url, type_parsing)
    if is_need_compress:
        result_filename = archive_file(result_filename)
    email_filename = generate_email_filename(*get_city_category_from_url(url))
    send_email(is_need_compress, result_filename, email, email_filename)
    os.remove(result_filename)


def start_parser(url, type_parsing=DownloadForm.CHOICES_TYPE_PARCING[1][0]):
    """Start parsing."""
    from scrapy_parser.yellparser.spiders.yell_spider import YellSpider
    from scrapy_parser.yellparser.settings import FEED_EXPORT_FIELDS
    url = str(url)
    logger.info('Start parsing with url: {}'.format(url))
    settings = get_project_settings()
    filename = '/tmp/{}.csv'.format(uuid.uuid4())
    # without this settings csv dump works wrong
    settings.set('FEED_URI', filename)
    settings.set('FEED_FORMAT', 'csv')
    settings.set('FEED_EXPORT_FIELDS', FEED_EXPORT_FIELDS)
    process = CrawlerProcess(settings)
    process.crawl(YellSpider, urls=url, type_parsing=type_parsing)
    process.start()
    return filename


def send_email(attachment_is_arch=False, filename=None, email=None, email_filename='results'):
    """Send results of parsing on email."""
    msg = Message("Parsing results", sender=app.config['EMAIL_FROM'], recipients=[email])
    logger.info('Send e-mail to: {}'.format(email))
    if filename:
        if attachment_is_arch:
            email_filename = '{}.zip'.format(email_filename)
            msg.attach(email_filename, "application/zip", filename)
        else:
            with app.open_resource(filename) as fp:
                msg.attach(email_filename, "text/csv", fp.read())

    with app.app_context():
        mail.send(msg)


def archive_file(filename):
    """Archive csv results into zip archive."""
    logger.info('Archive file: {}'.format(filename))
    buff = BytesIO()
    with zipfile.ZipFile(buff, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_archive:
        zip_archive.write(filename, os.path.relpath(filename, '/tmp'))
    return buff.getbuffer()
