# -*- coding: utf-8 -*-
# @Author: home-pc
# @Date:   2017-09-10 15:25:52
# @Last Modified by:   MOLBASE\hang.zhang
# @Last Modified time: 2017-09-19 11:08:29


from scrapy_redis.queue import PriorityQueue


class easyPriorityQueue(PriorityQueue):

    # no use...
    # def pop(self, timeout=0):
    #     """
    #     Pop a request
    #     timeout not support in this queue class
    #     """
    #     # use atomic range/remove using multi/exec
    #     pipe = self.server.pipeline()
    #     pipe.multi()
    #     # pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
    #     pipe.zrange(self.key, 0, 0)
    #     results = pipe.execute()[0]
    #     if results:
    #         return self._decode_request(results[0])
    # pass
    def pop(self, timeout=0):
        """
        modified by yiTian.zhang

        maybe...the rem command have received by redis, but when redis response the command,
        spider has lost connection, then...the request has lost
        """
        """
        Pop a request
        timeout not support in this queue class
        """
        # use atomic range/remove using multi/exec
        
        pipe = self.server.pipeline()
        pipe.multi()

        pipe.zrange(self.key, 0, 0)
        results = pipe.execute()[0]

        pipe.zremrangebyrank(self.key, 0, 0)
        count = pipe.execute()
        
        if results:
            return self._decode_request(results[0])

