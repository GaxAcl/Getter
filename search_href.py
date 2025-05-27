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
    searchFinding = str(input("请输入想要搜索的东西: "))
    if searchFinding == "":
        print("请输入有效查询目标")
        return get_url()
    searchUrl = searchWeb.format(parse.quote(searchFinding))
    return searchUrl


def get_html(url, headers):
    response = requests.get(url, headers)
    if response.status_code == 200:
        response.encoding = "utf-8"
        html = response.text
        return html
    else:
        print("请求失败")
        return None


def search_href(html):
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


def search_website(url, amount):
    pass


if __name__ == "__main__":
    print("OK")