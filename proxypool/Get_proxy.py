import json
from 代理池.get_66html import get_66page
from 代理池.get_goubanjia_html import get_goubanjia
from 代理池.get_kuaidaili_html import get_kuaidaili


class ProxyMetaclass(type):#继承type创建为元类
    def __new__(cls, name,bases,attrs):#name-->我是谁,bases-->我从哪里来,一般为object,attrs-->我要到哪里去
        count = 0
        attrs['crawl_name']=[]
        for key,value in attrs.items():#可看做字典形式
            if 'crawl_' in key:
                attrs['crawl_name'].append(key)#向attrs中添加所有获取代理的方法,后进行调用
                count += 1
        attrs['crawl_count']=count-1
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print("成功获取到代理%s"%proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self,page_count=5):
        start_url='http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            html = get_66page(url)
            trs = html.xpath("//div[@class='containerbox boxindex']//tr[position()>1]")
            for tr in trs:
                ip = tr.xpath("./td[1]/text()")[0]
                port = tr.xpath("./td[2]/text()")[0]
                yield ip+":"+port

    def crawl_goubanjia(self):
        start_url = "http://www.goubanjia.com/index.html"
        html = get_goubanjia(start_url)
        tds = html("td.ip").items()
        for td in tds:
            td.find("p").remove()
            yield (td.text().replace(" ", "").replace("\n", ""))

    def crawl_kuaidaili(self,page_count=5):
        start_url = "https://www.kuaidaili.com/free/inha/{}/"
        html = get_kuaidaili([start_url.format(page) for page in range(1,page_count)])
        trs = html.xpath("//table[@class='table table-bordered table-striped']//tr[position()>1]")
        for tr in trs:
            ip = tr.xpath("./td[1]/text()")[0]
            port = tr.xpath("./td[2]/text()")[0]
            yield ip+":"+port

