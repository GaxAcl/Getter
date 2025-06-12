import requests
from urllib import parse
from bs4 import BeautifulSoup
from typing import Optional
from fake_useragent import UserAgent


def get_amount() -> Optional[int]:
    """用于获取请求的体量
    :return: 一个int类型的体量
    """
    searchAmount = int(input("请输入查找体量： "))
    if  searchAmount < 1 or searchAmount > 100:
        return get_amount()
    else:
        return searchAmount


def get_headers() -> Optional[dict]:
    """用于获取随机请求头部
    :arg:无输入
    :return:一个dict类型的请求头
    """
    ua = UserAgent(platforms=['desktop'], browsers=['Edge']).random
    headers = {'User-Agent': ua}
    # print("随机获得的请求头部",headers)
    return headers


def get_url() -> Optional[str]:
    """用于获取用户搜索网页
    :arg:无输入
    :return:一个str类型的url地址
    """
    searchWeb = 'https://cn.bing.com/search?q={}'
    searchFinding = str(input("请输入想要搜索的东西: "))
    if searchFinding == '':
        print("请输入有效查询目标")
        return get_url()
    searchUrl = searchWeb.format(parse.quote(searchFinding))
    return searchUrl


def search_href(searchUrl:str, headers:dict, amount:int) -> Optional[list]:
    """爬取目标url的网址
    :param searchUrl: 一个str类型的url地址
    :param headers: 一个dict类型的请求头
    :param amount: 一个int类型的数量限制
    :return: 一个列表包含所有获得的网址
    """
    global total, websiteList
    if headers is None:
        headers = get_headers()
    response = requests.get(searchUrl, headers)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        html = response.text
    else:
        print("请求失败")
        return None
    soup = BeautifulSoup(html,"lxml")
    websiteFind = soup.find_all('li',attrs={'_class':'b_logo'})
    total = total + len(websiteFind)
    for i in websiteFind:
        websiteList.append(i)
    if amount < total:
        newUrl = f"{searchUrl}&first={amount}"
        search_href(newUrl, get_headers(),amount)
    else:
        with open("test.html","w",encoding="utf-8") as f:
            for i in websiteList:
                href = i.get("href")
                text = i.get_text()
                if href is None:
                    continue
                else:
                    f.write(href)
                    f.write("     ")
                    f.write(text)
                    f.write("\n")
            f.close()
    return None


if __name__ == '__main__':
    total = 0
    websiteList = []
    search_href(searchUrl=get_url(), headers=get_headers(), amount=get_amount())
    print("OK")