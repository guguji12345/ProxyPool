import aiohttp
from 代理池.Redis_db import RedisClient
import asyncio
import time
import sys
from aiohttp import ClientError
from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from concurrent.futures._base import TimeoutError
from selenium.common.exceptions import TimeoutException


TRUE_STAUS_CODE = [200,302]
BASE_URL = 'https://www.jd.com/'
BATCH_MOTH_COUNT = 10

class Moth(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_singal_proxy(self,proxy):#异步测试单个代理的可用度,可在某个代理响应时间里进行下一次代理的请求
        connection = aiohttp.TCPConnector(verify_ssl=False)#不响应ssl要求,不知道该用什么连接器传输数据时使用TCP处理HTTP和HTTPS的连接器
        async with aiohttp.ClientSession(connector=connection)as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode("utf-8")
                real_proxy = 'http://'+proxy
                print("正在测试代理",proxy)
                async with session.get(BASE_URL,proxy=real_proxy,timeout=15,allow_redirects=False)as response:
                    if response.status in TRUE_STAUS_CODE:
                        self.redis.max(proxy)
                        print("可用代理为",proxy)
                    else:
                        self.redis.decrease(proxy)
                        print("请求响应码不合法",response.status,"IP为",proxy)
            except (TimeoutError,ProxyConnectionError,ClientError,AttributeError,asyncio.TimeoutError,TimeoutException):
                self.redis.decrease(proxy)
                print(proxy,"代理请求失败")

    def run(self):#测试器,批量测试代理
        print("开始测试")
        try:
            count = self.redis.count()
            print("当前剩余",count,"个代理")
            for i in range(0,count,BATCH_MOTH_COUNT):
                start = i
                stop = min(i + BATCH_MOTH_COUNT,count)
                print("正在测试第",start+1,"-",stop,"中的代理")
                test_proxies = self.redis.batch(start,stop)
                loop = asyncio.get_event_loop()#批量测试,创建事件循环,协程需借助该事件来触发循环
                tasks = [self.test_singal_proxy(proxy) for proxy in test_proxies]#将批量测试的每个代理进行单独测试,创建协程
                loop.run_until_complete(asyncio.wait(tasks))#将协程加入到循环事件并开始启动
                sys.stdout.flush()#强制刷新缓冲区,可达到立刻打印的目的
                time.sleep(5)
        except Exception as e:
            print("测试期发生错误",e.args)
