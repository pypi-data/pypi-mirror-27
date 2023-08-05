# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2017-10-30 11:00:02
# @Last Modified by:   hang.zhang
# @Last Modified time: 2017-11-28 16:30:20

import time
import logging
import hashlib
from DBService import MysqlService

logger = logging.getLogger(__name__)


def md5_from_dict(item):
    sort_list = sorted(item.iteritems(), key=lambda x: x[0])
    return hashlib.md5(str(sort_list)).hexdigest()


# insert_or_update 为了标志是否进行过操作，一定要加上一个时间的字段，必须要有时间
def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


class mysqlPipeline(object):

    def __init__(self, settings):
        self.mysql_host = settings.get("MYSQL_HOST")
        self.mysql_user = settings.get("MYSQL_USER")
        self.mysql_password = settings.get("MYSQL_PASSWORD")
        self.mysql_port = settings.get("MYSQL_PORT")
        self.mysql_db = settings.get("MYSQL_DB")
        self.mysql_table = settings.get("MYSQL_TABLE")

        self.server = MysqlService(
            self.mysql_host, self.mysql_user, self.mysql_password, self.mysql_port)
        self.server.select_db(self.mysql_db)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        print "\n\n\n\n\n%s\n" % item
        return item

    def insert_or_update(self, item, spider):
        hash_code = md5_from_dict(item)
        hashcode_list = self.server.query('select id from %s where hash_check="%s";' % (self.mysql_table, hash_code))
        if hashcode_list:
            record_id = hashcode_list[0].get("id")
            item["last_checktime"] = current_time()
            update_sql = self.server.update_sql_from_map(self.mysql_table, {"id": record_id}, item).replace("%", "%%")
            logger.debug("already have record, update last_checktime, running sql is %s" % update_sql)
            self.server.execute(update_sql)
        else:
            item["hash_check"] = hash_code
            item["last_checktime"] = current_time()
            sql = self.server.join_sql_from_map(self.mysql_table, item).replace("%", "%%")
            logger.debug("find a new record, insert sql is %s" % sql)
            self.server.execute(sql)

    # 如果是使用 sqlalchemy 的话，可以使用下面这个代码
    # def insert_or_update(self, item, spider):
    #     hash_code = md5_from_dict(item)
    #     hashcode_list = map(dict, self.server.execute('select id from %s where hash_check="%s";' % (self.mysql_table, hash_code)).fetchall())
    #     if hashcode_list:
    #         record_id = hashcode_list[0].get("id")
    #         item["last_checktime"] = current_time()
    #         update_sql = MysqlService.update_sql_from_map(self.mysql_table, {"id": record_id}, item).replace("%", "%%")
    #         logger.debug("already have record, update last_checktime, running sql is %s" % update_sql)
    #         self.server.execute(update_sql)
    #     else:
    #         item["hash_check"] = hash_code
    #         item["last_checktime"] = current_time()
    #         sql = MysqlService.join_sql_from_map(self.mysql_table, item).replace("%", "%%")
    #         logger.debug("find a new record, insert sql is %s" % sql)
    #         self.server.execute(sql)
