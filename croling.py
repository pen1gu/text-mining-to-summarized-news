# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import random
import csv
from sqlalchemy import create_engine

# %%
def get_read_content(read_url):
    response = requests.get(read_url, headers=headers)

    res = bs(response.text, "html.parser")
    try:
        journalist_name = res.find("div", {"class": "journalistcard_summary_name"}).text
    except:
        try:
            journalist_name = res.find("p", {"class": "b_text"}).text
            journalist_name = journalist_name.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ,]", "")
        except:
            journalist_name = None

    # likeit_list = res.find_all("span",{"class":"u_likeit_list_count _count"})
    # print(likeit_list)
    res = res.find("div", {"class": "_article_body_contents article_body_contents"})

    try:
        img_coment = res.find("em", {"class": "img_desc"}).text.strip()
    except:
        img_coment = ""

    full_con = (
        res.text.strip()
        .replace("// flash 오류를 우회하기 위한 함수 추가", "")
        .replace("function _flash_removeCallback() {}", "")
        .replace("\n", "")
        .replace(img_coment, "")
    )

    return img_coment, full_con, journalist_name
    # return full_con, journalist_name


def get_content(news_list):
    news_page_df = None
    for news in news_list:
        inf = {
            "date": None,
            "title": None,
            "lede": None,
            "writing": None,
            "journalist": None,
            "news_url": None,
            "img_url": None,
            "content": None,
            "img_coment": None,
        }

        inf["date"] = date
        head = news.find("dl").find("dt")
        news_url = head.find("a")["href"]
        inf["img_coment"], inf["content"], inf["journalist"] = get_read_content(
            news_url
        )
        # inf["content"], inf["journalist"] = get_read_content(news_url)

        inf["news_url"] = news_url
        img_url = inf["img_url"] = head.find("a").find("img")

        if img_url is not None:
            inf["img_url"] = img_url["src"][:-14]
            inf["title"] = img_url["alt"]
        else:
            inf["title"] = head.text.strip()

        dd = news.find("dl").find("dd")
        inf["lede"] = dd.find("span", {"class": "lede"}).text
        inf["writing"] = dd.find("span", {"class": "writing"}).text
        if len(inf["content"]) > 1:
            try:
                news_page_df = news_page_df.append(inf, ignore_index=True)
            except:
                news_page_df = pd.DataFrame([inf])
        time.sleep(random.randrange(1, 7))
    return news_page_df


# %%
all_news_df = pd.DataFrame(
    columns=[
        "date",
        "title",
        "lede",
        "writing",
        "journalist",
        "news_url",
        "img_url",
        "content",
        "img_coment",
    ]
)


date = 20211116
list_url_base = "https://news.naver.com/main/list.naver"
list_url_start = f"?mode=LS2D&mid=shm&sid2=250&sid1=102&date={date}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}

response = requests.get(list_url_base + list_url_start, headers=headers)

time.sleep(random.randrange(20, 30))

while True:
    list_page = bs(response.text, "html.parser")
    news_list = list_page.find("div", {"class": "content"})
    news_list = news_list.find_all("li")

    print("serch page...")

    all_news_df = all_news_df.append(get_content(news_list), ignore_index=True)

    page_indexs = list_page.find("div", {"class": "paging"}).find_all("a")
    if "next" in page_indexs[-1]["class"]:
        news_list_url_list = page_indexs[:-1]
        next_page_url = page_indexs[-1]["href"]
    else:
        news_list_url_list = page_indexs
        next_page_url = None

    for news_list_url in news_list_url_list:
        print("serch page...")
        response = requests.get(list_url_base + news_list_url["href"], headers=headers)
        list_page = bs(response.text, "html.parser")
        news_list = list_page.find("div", {"class": "content"})
        news_list = news_list.find_all("li")
        all_news_df = all_news_df.append(get_content(news_list), ignore_index=True)

    if next_page_url is None:
        break
    else:
        response = requests.get(list_url_base + next_page_url, headers=headers)

        time.sleep(random.randrange(10, 20))


# all_news_df.to_csv(
#     f"C:/workspace/naver_news/news_{date}.csv",
#     sep="",
#     quoting=csv.QUOTE_NONE,
#     escapechar="|",
# )

# %%
db_connection_str = "mysql+pymysql://root:wlsghks1234*@127.0.0.1/naver_news"
db_connection = create_engine(db_connection_str)
# conn = db_connection.connect()
# conn = pymysql.connect(host='127.0.0.1',user='root',password='wlsghks1234*',db= 'testdb',charset='utf8')
all_news_df.to_sql(name="news", con=db_connection, if_exists="replace", index=False)

import kobert

