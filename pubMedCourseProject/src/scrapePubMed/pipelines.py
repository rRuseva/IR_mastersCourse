# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import json


class MedImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename', '')

    def get_media_requests(self, item, info):
        img_urls = item['image_url']
        filenames = item['image_path']

        for img_url, name in zip(img_urls, filenames):
            yield Request(url=img_url, meta={'filename': name})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def item_completed(self, results, item, info):

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['images'] = image_paths
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.pubMedImages_json = open('../../assets/medImages.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.pubMedImages_json.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"

        self.pubMedImages_json.write(line)

        return item
