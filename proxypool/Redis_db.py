MAX_SCORE = 100#设置可用代理分数为100
MIN_SCORE = 0#设置不可用代理分数为0
INITIAL_SCORE = 10#新获取到的代理分数设置为10
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_POSSWORD = None
REDIS_KEY = 'proxies'


import redis
from random import choice
from 代理池.PoolEmptyError import PoolEmptyError
import re
import random

class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_POSSWORD):
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)

    def add(self,proxy,score=INITIAL_SCORE):
        if not re.match(r'\d+\.\d+\.\d+\.\d+:\d+',proxy):
            print("代码",proxy,"不符合规范,已舍弃")
            return
        if not self.db.zscore(REDIS_KEY,proxy):#如果键名为REDIS_KEY的zset中proxy没有分数
            return self.db.zadd(REDIS_KEY,{proxy:score})#向键名为REDIS_KEY的zset中添加分数为score的proxy(代理)

    def random_100(self):#随机方法
        result = self.db.zrevrange(REDIS_KEY,0,100)#返回键名为REDIS_KEY的zset中从大到小第0个到第100个元素
        if len(result):
            return "，".join(result)
        else:
            raise PoolEmptyError

    def all_100(self):
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)  # 返回键名为REDIS_KEY的zset中所有最大元素
        if len(result):
            return "，".join(result)
        else:
            raise PoolEmptyError

    def random(self):#随机方法
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)#返回键名为REDIS_KEY的zset中score在为最大值时的proxy元素,列表形式
        if len(result):#存在result为最高分数时进行随机抽选
            return choice(result)
        else:
            raise PoolEmptyError

    def decrease(self,proxy):#减分方法
        score = self.db.zscore(REDIS_KEY,proxy)#返回键名为REDIS_KEY的zset中proxy对应的分数
        if score and score > MIN_SCORE:#当存在分数并且分数大于0时
            print("代理",proxy,"当前分数",score,"减二")
            return self.db.zincrby(REDIS_KEY,-2,proxy)#将键名为REDIS_KEY的zset中proxy对应的score-2
        else:#当分数为0时
            print("代理",proxy,"当前分数",score,"移除")
            return self.db.zrem(REDIS_KEY,proxy)#从键名为REDIS_KEY的zset中移除proxy

    def exists(self,proxy):#判断代理是否存在
        return not self.db.zscore(REDIS_KEY,proxy) == None

    def max(self,proxy):#将可用代理设置为100分
        print("代理",proxy,'可用,分数设置为',MAX_SCORE)
        return self.db.zadd(REDIS_KEY,{proxy:MAX_SCORE})

    def count(self,):#统计代理数量
        return self.db.zcard(REDIS_KEY)#获取键名为REDIS_KEY的zset中元素的个数

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)#获取键名为REDIS_KEY的zset中元素proxy分数在0-100范围内的所有元素,列表形式

    def batch(self,start,stop):
        return self.db.zrevrange(REDIS_KEY,start,stop-1)






