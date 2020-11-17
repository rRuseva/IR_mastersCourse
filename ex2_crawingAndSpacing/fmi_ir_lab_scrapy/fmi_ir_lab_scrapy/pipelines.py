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

        if 'image_url' not in item:
            return None

        img_url = item['image_url']
        meta = {'filename': item['image_path']}

        yield Request(url=img_url, meta=meta)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['images'] = image_paths
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.fmi_staff_json = open('./assets/fmi-offices.jl', 'w', encoding='utf-8')
        self.ban_staff_json = open('./assets/other-offices.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.fmi_staff_json.close()
        self.ban_staff_json.close()

    def process_item(self, item, spider):
        print(item)
        del item['image_url']
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"

        contains_fmi = item['office'] and 'фми' in item['office'].lower()
        file = self.fmi_staff_json if contains_fmi else self.ban_staff_json

        file.write(line)

        return item
