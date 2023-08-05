# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2017-07-28 14:07:10
# @Last Modified by:   hang.zhang
# @Last Modified time: 2017-10-26 11:28:37

import json
import logging
from scrapy import signals
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy_redis import picklecompat
from scrapy.exceptions import DropItem
from scrapy.core.scraper import Scraper
from twisted.python.failure import Failure
from scrapy.utils.request import referer_str
from scrapy.utils.reqser import request_to_dict
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.log import logformatter_adapter
from scrapy.utils.request import request_fingerprint


logger = logging.getLogger(__name__)

import traceback

class easyScraper(Scraper):

    # 核心希望替换的东西
    def handle_spider_error(self, _failure, request, response, spider):
        # 之前的套路
        super(easyScraper, self).handle_spider_error(_failure, request, response, spider)
        """
            目的就是要在出错的时候，能够打印出出错的body请求。同时把出错的请求，重新放回队列中去
            预防这样一种情况：当出现正则或者xpath规则提取不到的时候，能够马上反映出，是为什么规则出错
            是否是发现了不同格式的body内容，需要增加规则的数量
            而常规的scraper 只是记录报错写error log和reason，并不会告诉你此时的response body
            由于blocked之后的操作和此次目的是一样的，所以直接就用这个
        """
        spider.blocked_call_back(response, reason="Spider error processing %(request)s (referer: %(referer)s): info %(info)s" % {'request': request, 'referer': referer_str(request), 'info': "%s, %s" % (failure_to_exc_info(_failure), repr(traceback.format_exc())) }, exc_info=failure_to_exc_info(_failure), extra=self.__class__.__name__)

    # Error downloading 就不需要记录，因为Error downloading根本没有body
    # def _log_download_errors(self, spider_failure, download_failure, request, spider):
    #     pass

    def _process_spidermw_output(self, output, request, response, spider):
        """add response argument in item pipeline
        """
        if isinstance(output, Request):
            meta_easyspider = output.meta.get("easyspider") or {}
            meta_easyspider.update({
                "crawled_urls_path": meta_easyspider.get("crawled_urls_path", []) + [request.url]
            })
            output.meta.update({"easyspider": meta_easyspider})
            self.crawler.engine.crawl(request=output, spider=spider)
        elif isinstance(output, (BaseItem, dict)):
            self.slot.itemproc_size += 1
            # this if will never be false, because the only time to be false, is request from put_back_2_start_urls, and history request has meta..and has
            # crawled_urls_path...but, ! put_back_2_start_urls will not record crawled_urls_path
            # -----------------------------------------------
            if not output.get("crawled_url"):
                output["crawled_url"] = response.url

                meta_easyspider = response.meta.get("easyspider") or {}
                # crawled_urls_path = meta_easyspider.get("crawled_urls_path") or [] + [response.url] + [response.meta.get("redirect_urls")] or [response.url]
                # the best way to get crawled_urls_path is get result from redirect_urls
                crawled_urls_path = meta_easyspider.get("crawled_urls_path") or []
                if not response.meta.get("redirect_urls"):
                    crawled_urls_path = crawled_urls_path + [response.url]
                else:
                    crawled_urls_path = crawled_urls_path + response.meta.get("redirect_urls")
                output["crawled_urls_path"] = crawled_urls_path
            else:
                # if has add crawled_urls_path before, just need to add current request request
                output["crawled_urls_path"] += [response.url]
            # -----------------------------------------------
            dfd = self.itemproc.process_item(output, spider)
            dfd.addBoth(self._itemproc_finished, output, response, spider)
            return dfd
        elif output is None:
            # pass
            # 2017-9-26 16:12:34 if output is None, it should also add fingerprint to dupefilter, beacuse if not add to dupefilter...it will 
            # be use in another spider, recrawler the same task...(a bug: if UA headers if difference, the same requests will look difference...)
            # 就算输出为空，也要添加到dupefilter 里面去，因为不然这样的话，就会被其他爬虫重复消费了。
            # ----Add fingerprint--------
            rq = response.request
            fp = request_fingerprint(rq)
            print "\n\n\n add request_fingerprint before !..."
            try:
                spider.server.sadd("%s:dupefilter" % spider.name, fp)
            except:
                logger.exception("when _itemproc_finished, add into request fingerprint failed....")
            # ----------------
        else:
            typename = type(output).__name__
            logger.error('Spider must return Request, BaseItem, dict or None, '
                         'got %(typename)r in %(request)s',
                         {'request': request, 'typename': typename},
                         extra={'spider': spider})

    def _itemproc_finished(self, output, item, response, spider):
        """
        # Add request fingerprint
        """
        """ItemProcessor finished for the given ``item`` and returned ``output``
        """
        self.slot.itemproc_size -= 1
        # -------------------------
        rq = response.request
        # --------------------------
        if isinstance(output, Failure) or not rq:
            ex = output.value
            if isinstance(ex, DropItem):
                logkws = self.logformatter.dropped(item, ex, response, spider)
                logger.log(*logformatter_adapter(logkws), extra={'spider': spider})
                return self.signals.send_catch_log_deferred(
                    signal=signals.item_dropped, item=item, response=response,
                    spider=spider, exception=output.value)
            else:
                logger.error('Error processing %(item)s', {'item': item},
                             exc_info=failure_to_exc_info(output),
                             extra={'spider': spider})
        else:
            logkws = self.logformatter.scraped(output, response, spider)
            logger.log(*logformatter_adapter(logkws), extra={'spider': spider})
            # ----Add fingerprint--------
            fp = request_fingerprint(rq)
            try:
                spider.server.sadd("%s:dupefilter" % spider.name, fp)
            except:
                logger.exception("when _itemproc_finished, add into request fingerprint failed....")
            # ----------------
            # ------remove request record beacuse successed-----

            # data = self._encode_request_for_remove_successed_request(response.request, spider)
            # spider.server.execute_command("ZREM", '%(spider)s:requests' % {"spider": spider.name}, data)
            # print "\n\nremove .... remove \n\n"
            # print "\n\n request is data %s" % repr(data)
            # --------------------------------------------------

            # ------add start urls-----
            successed_request = spider.parse_request_to_dict(response)
            try:
                spider.server.sadd("%s:successed_urls" % spider.name, json.dumps(successed_request))
            except:
                logger.exception("in _itemproc_finished, add successed request failed....")
            # --------------------------------------------------
            return self.signals.send_catch_log_deferred(
                signal=signals.item_scraped, item=output, response=response,
                spider=spider)

    def _encode_request_for_remove_successed_request(self, request, spider):
        """Encode a request object"""
        obj = request_to_dict(request, spider)
        return picklecompat.dumps(obj)
