import requests
from urllib import parse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_headers():
    ua = UserAgent(platforms=['desktop'], browsers=['Edge']).random
    headers = {"UserAgent": ua}
    print("随机获得的请求头部",headers)
    return headers


def get_url():
    searchWeb = "https://cn.bing.com/search?q={}"
    searchName = parse.quote(input("请输入想要搜索的东西: "))
    searchUrl = searchWeb.format(searchName)
    return searchUrl


def get_html():
    response = requests.get(url=get_url(), headers=get_headers())
    if response.status_code == 200:
        response.encoding = "utf-8"
        html = response.text
        return html
    else:
        print("请求失败")
        return "None"


total = 0
def search_href():
    html = get_html()
    soup = BeautifulSoup(html,"lxml")
    with open("search_href.txt", "w", encoding="utf-8") as f:
        for i in soup.find_all("a",attrs={"target":"_blank"}):
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


if __name__ == "__main__":
    search_href()
    print("OK")