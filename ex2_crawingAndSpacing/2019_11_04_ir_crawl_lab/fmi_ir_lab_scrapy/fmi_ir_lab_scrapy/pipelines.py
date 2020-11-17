# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

import json


class AvatarImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename', '')

    def get_media_requests(self, item, info):

        pass

        yield Request(url=img_url, meta=meta)

    def item_completed(self, results, item, info):
        pass


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        # Open your export files here (for teachers in FMI and those in other buildings)

    def close_spider(self, spider):
        # Don't forget to close them

    def process_item(self, item, spider):
        # Remove unsed attributes from item
        # Write each row into it's proper file
