# -*- coding: utf-8 -*-

from w3lib.html import remove_tags

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst


def absolute_url(url, loader_context):
    return loader_context['response'].urljoin(url)


class Fit(scrapy.Item):

    fit_id = scrapy.Field()
    no = scrapy.Field()
    post_code = scrapy.Field()
    technology = scrapy.Field()
    installation = scrapy.Field()
    kw = scrapy.Field()
    commission = scrapy.Field()
    export = scrapy.Field()
    tariff = scrapy.Field()
    country = scrapy.Field()
    go_region = scrapy.Field()
    local_authority = scrapy.Field()
    related_id = scrapy.Field()
    generator_name = scrapy.Field()
    fit_link = scrapy.Field()
    related_link = scrapy.Field()


class FitLoader(scrapy.loader.ItemLoader):

    default_item_class = Fit
    default_input_processor = MapCompose(remove_tags, str.strip)
    default_output_processor = TakeFirst()

    fit_link_in = MapCompose(absolute_url)
    related_link_in = MapCompose(absolute_url)
