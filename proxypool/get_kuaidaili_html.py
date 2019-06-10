import requests
from lxml import etree

def get_kuaidaili(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }

    url = 'https://www.kuaidaili.com/free/inha/1/'
    response = requests.get(url, headers=headers)
    text = response.content.decode("utf-8")
    html = etree.HTML(text)
    return html