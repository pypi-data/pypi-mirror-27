# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2017-09-05 16:20:40
# @Last Modified by:   home-pc
# @Last Modified time: 2017-09-10 15:48:18

from scrapy_redis.dupefilter import RFPDupeFilter
import logging


logger = logging.getLogger(__name__)


class easyRFPDupeFilter(RFPDupeFilter):

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        # added = self.server.sadd(self.key, fp)
        try:
            added = self.server.sismember(self.key, fp)
        # print "\n\n sismember ", self.server.sismember(self.key, fp)
            return added
        except:
            # return false to schedler this request
            logger.exception("in easyRFPDupeFilter: check is in dupefilter failed, return false")
            return False
        # return added == 0
