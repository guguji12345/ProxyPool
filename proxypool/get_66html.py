from lxml import etree
from selenium import webdriver


def get_66page(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    cookies = browser.get_cookies()
    for cookie in cookies:
        browser.add_cookie({"name": cookie.get("name"), "value": cookie.get("value")})
    browser.get(url)
    text = browser.page_source
    html = etree.HTML(text)
    return html


