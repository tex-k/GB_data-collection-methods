# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyparsePipeline:
    def process_item(self, item, spider):
        client = MongoClient("localhost", 27017)
        db = client.adv
        collection = db["leroy"]
        collection.insert_one(item)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["photos"]:
            for photo in item["photos"]:
                try:
                    yield scrapy.Request(photo)
                except:
                    pass

    def item_completed(self, results, item, info):
        item["photos"] = [itm[1] for itm in results if itm[0]]
        return item
