import requests
from pyquery import PyQuery as pq

def get_goubanjia(url):
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    text = response.content.decode("utf-8")
    html = pq(text)
    return html
