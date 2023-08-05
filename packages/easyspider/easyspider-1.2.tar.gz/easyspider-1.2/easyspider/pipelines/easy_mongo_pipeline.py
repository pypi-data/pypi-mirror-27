# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2017-07-25 17:48:09
# @Last Modified by:   hang.zhang
# @Last Modified time: 2017-08-07 14:14:31
from easyspider.utils.DBService import MongoService
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

default_mongo_url = "mongodb://localhost:27017"
default_mongo_db_name = "spider"

mongo_url_key = "MONGO_URL"
mongo_db_name = "MONGO_DB_NAME"

# 存入mongo的collection的key名
item_result_table_key = "result_table"
# 存入的操作是update还是直接insert
item_update_key = "update_record"
item_update_query_key = "update_query_key"
# 存入的时候是否需要新建一个collections来保存历史记录
item_keep_history = "keep_history"
# 存入库的名字，如果没有指定库，那么就以spider名字来命名
item_save_db = "save_db"

class easyMongoPipeline(object):

    def __init__(self, mongoUrl, mongoDbName):
        self.server = MongoService(mongoUrl)
        self.server.select_db(mongoDbName)

    @classmethod
    def from_settings(cls, settings):
        mongoUrl = settings.get(mongo_url_key, default_mongo_url)
        mongoDbName = settings.get(mongo_db_name, default_mongo_db_name)
        return cls(mongoUrl, mongoDbName)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        result_table = item.get(item_result_table_key, spider.name)
        # 每个爬虫结果享有一个独立的库，如果没有在item中指定
        self.server.select_db(item.get(item_save_db, spider.name))
        # 检查是新增还是update
        if item.get(item_update_key):
            # update 的话，需要先按照条件查询
            history_record = {}
            for key in item.get(item_update_query_key):
                history_record[key] = item.get(key)
            # 相当于查询出来了再替换
            # self.server.update(result_table, item, history_record)
            self.server.replace_one(result_table, item, history_record)
        else:
            self.server.insert(result_table, item)
        # 检查是否需要保留历史记录
        if item.get(item_keep_history):
            self.server.insert("%s_history" % result_table, item)
        return item
