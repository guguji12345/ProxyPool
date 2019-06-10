MOTH_ENABLE=True#测试模块开关
GET_ENABLE=True#获取模块开关
API_ENABLE=True#接口模块开关
MOTH_CYCLE=20#测试时间间隔
GET_CYCLE=100#获取时间间隔
API_HOST='0.0.0.0'
API_PORT=5555

from multiprocessing import Process
from 代理池.Get_run import Get_proxies
from 代理池.Random_proxy_api import app
from 代理池.Moth_proxy import Moth
import time

class Scheduler():
    def scheduler_moth(self,cycle=MOTH_CYCLE):
        moth = Moth()
        while True:
            print("测试器开始执行")
            moth.run()
            time.sleep(cycle)

    def scheduler_get(self,cycle=GET_CYCLE):
        get = Get_proxies()
        while True:
            print("开始获取代理")
            get.run()
            time.sleep(cycle)

    def scheduler_api(self):
        app.run(API_HOST,API_PORT)

    def run(self):
        print("代理池开始运行")
        if GET_ENABLE:
            get_process=Process(target=self.scheduler_get)
            get_process.start()
        if MOTH_ENABLE:
            moth_process=Process(target=self.scheduler_moth)
            moth_process.start()
        if API_ENABLE:
            api_process=Process(target=self.scheduler_api)
            api_process.start()
