# -*- coding: utf-8 -*-
# @Author: zhangTian
# @Email:  hhczy1003@163.com
# @Date:   2017-07-08 13:48:45
# @Last Modified by:   MOLBASE\hang.zhang
# @Last Modified time: 2017-09-14 10:24:03


# TODO: 队列监控反馈
import logging
from scrapy_redis.scheduler import Scheduler
logger = logging.getLogger(__name__)


class easyScheduler(Scheduler):

    def has_pending_requests(self):
        # in this method, you should only return True regardless what len(self) is
        # because in a extreme case, spider machine may lost connection with the redis
        # (ADSK dailing interval or even worse case: the ADSL interface had crush down and must reboot to resume),
        # if can not connect to redis, len(self) will casuse Exception, because of the Exception, crawler can not
        # run into next_request, and run into a useless loop, never require more request from redis anymore(because next_requsts not called)
        try:
            # print "in easyScheduler len(queue) are %s" %len(self)
            return len(self) > 0
        except:
            logger.exception("in easyScheduler: check has_pending_requests,  len(self) failed, return false")
            return False

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        # loop until connected to redis
        while True:
            try:
                self.queue.push(request)
                return True
            except:
                logger.exception("in easyScheduler: enqueue_request,  self.queue.push(request) failed, return True")
