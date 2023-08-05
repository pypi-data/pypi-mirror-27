# coding=utf-8

from scrapy_redis.spiders import RedisCrawlSpider
from easyspider.utils.tools import get_time
from scrapy.http import Response
from bs4 import UnicodeDammit
from scrapy import Request
import urlparse
import urllib
import time
import json
import copy
"""base spider of easyspider
have provied multi useful method to make crawler more easier
"""


class easyCrawlSpider(RedisCrawlSpider):

    name = u"easyCrawlSpider"

    start_key = u"start_urls"
    block_key = u"blocked_urls"
    successed_key = u"successed_urls"

    # redis's operation methods
    fetch_unit = 16
    fetch_from_redis_method = (lambda self, server: server.lpop)
    save_into_redis_method = (lambda self, server: server.rpush)
    
    def next_requests(self):
        """
        heartbeat of engine, called every 5s, to generate new request in crawler process
        
        next_requests will [l]pop the spider_name:start_key list queue from redis (attention, operation is lpop,
        so when you need to push into redis, you should use rpush instead)
        """
        print "\n\nin spider next_request~~~  to get new start tasks"
        count = 0
        while count < self.fetch_unit:
            # may lost connection with redis, and then make spider closed with finished reason....
            try:
                start_map = self.fetch_from_redis_method(self.server)(u"%s:%s" % (self.name, self.start_key))
            except:
                self.logger.exception("in easyCrawlSpider: next_requests,  start_map = self.fetch_from_redis_method(self.server)(u\"%s:%s\" % (self.name, self.start_key)) failed, return")
                time.sleep(3)
                continue
            req = self.convert_startmap_2_request(start_map)
            if isinstance(req, Request):
                # yield Request
                yield req
            else:
                break
            count += 1

        self.logger.debug(u"Read %s requests from '%s:%s'" % (count, self.name, self.start_key))

    def convert_startmap_2_request(self, start_map):
        """start map has carry multi request's info, it should be parsed before scheduled"""

        # if fetch from redis is None
        if not start_map:
            return
        try:
            start_map = json.loads(start_map)
        except:
            self.logger.exception(u"convert start url -> dict failed, start_map source is %s" % (start_map))

        try:
            # if this new request's info is added by retrymiddleware or other error solve middleware, you should close the filter on this request
            if not start_map.get(u"dont_filter"):
                close_filter = True if int(start_map.get(u"easyspider", {}).get(u"from_retry") or 0) > 0 else False
            else:
                # close_filter = dont_filter
                close_filter = True if (start_map.get(u"dont_filter") == "True" or start_map.get(u"dont_filter") == "true" or start_map.get(u"dont_filter")) else False

            # callback is not sure to be parse, it can be assign by user. but also default to be parse
            # print start_map.get(u"callback", u"self.parse")
            req_callback_method = eval(start_map.get(u"callback", u"self.parse") or u"self.parse")

            # if http's method is post, post body can provide as dict or str/unicode.(in scrapy, body is str or unicode)
            post_data = start_map.get(u"body", "")
            if isinstance(post_data, dict):
                req_body = urllib.urlencode(post_data)
            elif isinstance(post_data, unicode) or isinstance(post_data, str):
                req_body = post_data
            else:
                self.logger.warning(u"request body type is not supported, input type is %s, source is %s" % (type(post_data), post_data))
                req_body = None

            # other info
            req_url = start_map.get(u"url")
            # req_method = start_map.get(u"method", u"GET")
            req_method = start_map.get(u"method") or  u"GET"
            req_headers = start_map.get(u"headers") or {} # (in scrapy, headers is dict, not not !! str) 
            req_cookies = start_map.get(u"cookies") or ""
            # 针对json 格式的请求，增加支持
            if "application/json" in req_headers.get("Content-Type", ""):
                req_body = json.loads(req_body)
            # meta message 
            req_meta = start_map.get(u"meta") or {}
            easyspider_info = {
                u"from_retry": start_map.get(u"easyspider", {}).get(u"from_retry", 0), # if from error back
                u"source_start_url": start_map.get(u"easyspider", {}).get(u"source_start_url", req_url) or req_url,  # the original request url
                u"remark": start_map.get(u"easyspider", {}).get(u"remark")   # some remark on this request
            }
            req_meta.update({"easyspider": easyspider_info}) # update meta
            print req_body
            return Request(url = req_url,
                callback = req_callback_method,
                method = req_method,
                meta = req_meta,
                body = req_body,
                headers = req_headers,
                cookies = req_cookies,
                dont_filter = close_filter
                )
        except:
            self.logger.exception(u"parse start url error, source start url is %s" % start_map)

    def is_blocked_spider(self, response):
        """method is called every time to check if blocked the spider, default to be False or None"""
        pass

    def blocked_call_back(self, response, reason=u"spider was blocked", exc_info=None, extra=None):
        """method called when spider is blocked, also can be used to record other error situation"""
        self.report_this_crawl_2_log(response, reason)
        self.put_back_2_start_url(response)

    def report_this_crawl_2_log(self, response, reason):
        """log this response"""
        report_template = u"""
            response body -> %(response_body)s
            %(response)s is recorded, because %(reason)s happended, following are detail info:
            response url -> %(response_url)s,
            status code -> %(status_code)s,
            request url -> %(request_url)s,
            original request url -> %(original_request_url)s

            request headers -> %(request_headers)s,
            request body -> %(request_body)s,

            request callback -> %(request_callback)s,

            """

        report_info = {
            u"response": response.url,
            u"reason": reason,
            u"response_url": response.url,
            u"status_code": response.status,
            u"request_url": response.request.url,
            u"original_request_url": self.get_source_url(response),
            u"request_headers": response.request.headers,
            u"request_body": self.get_request_body(response), # dict type
            # u"request_callback": response.request.callback.__name__,
            u"request_callback": self.get_last_request_callback(response),
            u"response_body": self.get_unicode_response_body(response) # unciode body
        }

        self.logger.info(report_template % report_info)

    def get_source_url(self, r):
        """to get the original url, because 302 will modified the request url"""
        if isinstance(r, Response):
            # Request object can't use copy 
            # r_copy = copy.deepcopy(r.request)
            r_copy = r.request.copy()
        else:
            # r_copy = copy.deepcopy(r)
            r_copy = r.copy()
        source_url = r_copy.meta.get(u"easyspider", {}).get(u"source_start_url")
        return source_url or r_copy.meta.get("redirect_urls", [None])[0] or r_copy.url

    def get_request_body(self, r):
        """return str/unicode request body -> dict"""
        if isinstance(r, Response):
            # r_copy = copy.deep_copy(r.request)
            r_copy = r.request.copy()
        else:
            # r_copy = copy.deepcopy(r)
            r_copy = r.copy()
        dict_body = self.parse_query_2_dict(r_copy.body)
        if not dict_body:
            try:
                dict_body = json.dumps(r_copy.body, ensure_ascii=False)
            except:
                self.logger.exception("convert request body failed... source body is %s" % r_copy.body)
        return dict_body

    def parse_query_2_dict(self, query):
        """parse url query to dict format"""
        try:
            return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
        except:
            self.logger.exception(u"can't parse url -> dict, source url data is %s" % query)

    def detect_encoding(self, body):
        dammit = UnicodeDammit(body)
        return dammit.original_encoding

    def get_unicode_response_body(self, response):
        # TypeError: decode() argument 1 must be string, not None
        # return response.body.decode(self.detect_encoding(response.body))
        if self.detect_encoding(response.body):
            return response.body.decode(self.detect_encoding(response.body))
        return response.body

    def put_back_2_start_url(self, r):
        """return error request to start step"""
        if isinstance(r, Response):
            # r_copy = copy.deepcopy(r.request)
            r_copy = r.request.copy()
        else:
            # r_copy = copy.deepcopy(r)
            r_copy = r.copy()

        if hasattr(r_copy, "priority"):
            priority = r_copy.priority or 0
        else:
            priority = 0

        reput_request = {
            u"url": self.get_source_url(r_copy),
            # u"callback": r_copy.callback.__name__,
            u"callback": self.get_last_request_callback(r_copy),
            u"method": r_copy.method,
            u"body": r_copy.method!="GET" and self.get_request_body(r_copy) or None,
            u"headers": r_copy.headers,
            u"dont_filter": True,
            "priority": priority
        }
        if reput_request.get("method") == "GET":
            reput_request.pop("body")

        meta = copy.deepcopy(r.meta)
        # direct launch Requst from start_requests won't have start_url template
        meta.get(u"easyspider", {}).update({
                u"from_retry": int(meta.get(u"easyspider", {}).get(u"from_retry", 0) or 0) + 1,
                u"source_start_url": self.get_source_url(r_copy),
                u"remark": meta.get(u"easyspider", {}).get(u"remark"),
            })
        reput_request["meta"] = meta
        # TODO: check if need to save cookies
        if self.settings.get(u"COOKIES_ENABLED"):
            reput_request["cookies"] = r_copy.cookies
        else:
            reput_request["cookies"] = None

        # put back to start key
        while True:
            try:
                self.save_into_redis_method(self.server)("%s:%s"%(self.name, self.start_key), json.dumps(reput_request))
                break
            except:
                self.logger.exception("in easyCrawlSpider: put_back_2_start_url,  self.save_into_redis_method failed, loop until it successed..")
        # logginig
        put_back_logging_template = """reput crawl task into start url, detail info are %s"""
        self.logger.info(put_back_logging_template % reput_request)

    def get_last_request_callback(self, r):
        if isinstance(r, Response):
            inline_r = r.request
        elif isinstance(r, Request):
            inline_r = r
        if not inline_r.callback:
            # default callback
            return "self.parse"
        return "self.%s" % inline_r.callback.__name__

    def parse_request_to_dict(self, r):
        """return error request to start step"""
        if isinstance(r, Response):
            # r_copy = copy.deepcopy(r.request)
            r_copy = r.request.copy()
        else:
            # r_copy = copy.deepcopy(r)
            r_copy = r.copy()

        reput_request = {
            u"url": self.get_source_url(r_copy),
            # u"callback": r_copy.callback.__name__,
            u"callback": self.get_last_request_callback(r_copy),
            u"method": r_copy.method,
            u"body": self.get_request_body(r_copy),
            u"headers": r_copy.headers,
            u"dont_filter": True
        }

        meta = copy.deepcopy(r.meta)
        # direct launch Requst from start_requests won't have start_url template
        meta.get(u"easyspider", {}).update({
                u"from_retry": int(meta.get(u"easyspider", {}).get(u"from_retry", 0) or 0) + 1,
                u"source_start_url": self.get_source_url(r_copy),
                u"remark": meta.get(u"easyspider", {}).get(u"remark"),
            })
        reput_request["meta"] = meta
        # TODO: check if need to save cookies
        if self.settings.get(u"COOKIES_ENABLED"):
            reput_request["cookies"] = r_copy.cookies
        else:
            reput_request["cookies"] = None
        return reput_request
