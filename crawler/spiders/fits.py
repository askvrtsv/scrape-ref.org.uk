# -*- coding: utf-8 -*-

import re

import scrapy
from scrapy.utils.response import open_in_browser

from crawler.items import FitLoader


URL = 'https://www.ref.org.uk/fits/search.php?order=fitid&dir=asc&fitid=FIT{fitid:0>5}&start={start}'

# Колонки таблицы с результатами поиска
COLS = ['fit_id', 'no', 'post_code', 'technology', 'installation', 'kw',
        'commission', 'export', 'tariff', 'country', 'go_region',
        'local_authority', 'related_id', 'generator_name']


class FitsSpider(scrapy.Spider):
    name = 'fits'
    allowed_domains = ['www.ref.org.uk']

    def start_requests(self):
        yield scrapy.Request(URL.format(fitid=1, start=''), self.parse_total)

    def parse_total(self, response):
        try:
            total = re.findall(r'returned (\w+) generators',
                               response.body.decode('utf8'))
            total = int(total[0])
        except (KeyError):
            self.logger.critical("Can't parse total fits")
            return

        self.logger.info(f'Will scrape {total} items')

        for fitid in range(0, total // 1000 + 1):
            for start in range(0, 1000, 200):
                yield scrapy.Request(URL.format(fitid=fitid, start=start),
                                     callback=self.parse_table)

    def parse_table(self, response):
        for row in response.css('.fits tbody tr'):
            l = FitLoader(response=response, selector=row)

            for colnum, colname in enumerate(COLS, 1):
                l.add_xpath(colname, f'./td[{colnum}]')

            l.add_xpath('fit_link', './td[1]/a/@href')
            l.add_xpath('related_link', './td[13]/a/@href')

            yield l.load_item()
