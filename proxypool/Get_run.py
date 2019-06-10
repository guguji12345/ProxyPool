from 代理池.Redis_db import RedisClient
from 代理池.Get_proxy import Crawler
import sys

POOL_UPPER_THRESHOLD = 10000
class Get_proxies():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):#判断数据库中代理数是否达到最大值
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("开始获取代理:")
        if not self.is_over_threshold():#当数据库中代理数较少时
            for callback_func in range(self.crawler.crawl_count):#遍历代理网站数量,为callback赋值
                callback = self.crawler.crawl_name[callback_func]#按索引给callback赋值不同的函数,即不同的网站
                proxies = self.crawler.get_proxies(callback)#获取网站中的代理
                # sys.stdout.flush()#强制刷新缓冲区,可达到立刻打印的目的
                for proxy in proxies:
                    self.redis.add(proxy)#添加代理
                    print(proxy,"添加成功")
