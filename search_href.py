import requests
from urllib import parse
from bs4 import BeautifulSoup
from typing import Optional
from fake_useragent import UserAgent


def get_headers() -> dict:
    ua = UserAgent(platforms=['desktop'], browsers=['Edge']).random
    headers = {'User-Agent': ua}
    print("随机获得的请求头部",headers)
    return headers


def get_url() -> str:
    searchWeb = 'https://cn.bing.com/search?q={}'
    searchFinding = str(input("请输入想要搜索的东西: "))
    if searchFinding == '':
        print("请输入有效查询目标")
        return get_url()
    searchUrl = searchWeb.format(parse.quote(searchFinding))
    return searchUrl


def search_href(url, headers) -> Optional[list]:
    global total, websiteList
    if headers is None:
        headers = get_headers()
    response = requests.get(url, headers)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        html = response.text
    else:
        print("请求失败")
        return None
    soup = BeautifulSoup(html,"lxml")
    websiteFind = soup.find_all('a',attrs={'target':'_blank'})
    total = total + len(websiteFind)
    for i in websiteFind:
        websiteList.append({i.get('href'),i.get_text()})
    return websiteList


def search_website(searchUrl, amount):
    if total < amount:
        newUrl = (searchUrl + "first{}").format(str(total+1))
        search_href(newUrl, get_headers())
        return search_website(searchUrl, amount)


if __name__ == '__main__':
    total = 0
    websiteList = []
    print("OK")