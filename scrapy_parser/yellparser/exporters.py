"""Scrapy results exporters."""
from scrapy.exporters import CsvItemExporter


class CsvItemExporterExtended(CsvItemExporter):
    """Exporter into csv."""

    def __init__(self, file, include_headers_line=True, join_multivalued=',', **kwargs):
        """Class constructor.

        Override for change delimeter in our csv result.
        """
        kwargs['delimiter'] = ';'
        super().__init__(file, include_headers_line, join_multivalued, **kwargs)
