# coding=utf-8

from datetime import datetime
from easyspider.utils.tools import get_time
import socket

flat = (lambda L: sum(map(flat, L), []) if isinstance(L, list) or isinstance(L, tuple) else [L])


class ExamplePipeline(object):

    def process_item(self, item, spider):
        item["crawled_time"] = get_time()
        item["spider"] = spider.name
        # 多机器抓取用来标志是来源于哪台机器
        item["crawled_server"] = ";".join(flat(socket.gethostbyname_ex(socket.gethostname())))
        # item["crawled_url"] = response.url
        return item
