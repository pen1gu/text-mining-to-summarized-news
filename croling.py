# %%

# - 공통 설명
## - 개발자 - 추후 수정을 위한 메모
### - 사용자 - 이용을 위한 부가 설명

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import random
import json
from sqlalchemy import create_engine


with open("conection_info_mylocal.json", "r") as f:
    conection_info = json.loads(f.read())

db_info = conection_info["database"]
request_info = conection_info["http_request"]

# %%
def get_read_content(read_url):
    response = requests.get(read_url, headers=request_info)

    res = bs(response.text, "html.parser")

    # 기자 이름 추출
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

    # 이미지 주석 추출
    try:
        img_coment = res.find("em", {"class": "img_desc"}).text.strip()
    except:
        img_coment = ""

    full_con = (
        res.text.strip()
        # 불필요한 주석 제거
        .replace("// flash 오류를 우회하기 위한 함수 추가", "").replace(
            "function _flash_removeCallback() {}", ""
        )
        # 줄바꿈 제거
        .replace("\n", "")
        # 이미지 주석 제거
        .replace(img_coment, "")
    )

    return img_coment, full_con, journalist_name
    # return full_con, journalist_name


def get_content(news_list):
    news_page_df = None
    for news in news_list:
        # 적제할 데이터 정의
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

        # 뉴스 날짜
        ## 현재 년월일 적제중
        ## 정확한 업로드시점 탐색 가능 여부 확인하기
        inf["date"] = date
        head = news.find("dl").find("dt")
        # 뉴스 원문 접근 url 추출
        news_url = head.find("a")["href"]
        inf["news_url"] = news_url
        # 이미지 주석, 원문, 기자 이름 추출
        inf["img_coment"], inf["content"], inf["journalist"] = get_read_content(
            news_url
        )
        # inf["content"], inf["journalist"] = get_read_content(news_url)

        # 이미지 접근 url 및 기사 제목 추출
        ## 이미지 db는 금지됨
        ## url은 괜찮은가?
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
                ## df.append 사용 금지!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                ## pd.concat 으로 바꿀것!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                news_page_df = news_page_df.append(inf, ignore_index=True)
            except:
                news_page_df = pd.DataFrame([inf])
        time.sleep(random.randrange(1, 2))
    return news_page_df


# %%
all_news_df = pd.DataFrame(
    ## 함수의 적제 데이터 정의 부분과 통일/일관성 유지?
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

# 검색 날짜
## 현재 하루단위로 검색
## 범위 검색에 대한 방안 찾기
date = 20220415

# 검색 url
list_url_base = "https://news.naver.com/main/list.naver"

# 검색 요청 sid
## 현재 사회-교육 요청 sid
## 다른 필터에 대한 sid탐색 및 dict 변환 필요
### 경제 sid1 = 101
list_url_start = f"?mode=LS2D&mid=shm&sid2=250&sid1=102&date={date}"

response = requests.get(list_url_base + list_url_start, headers=request_info)

# 과도한 탐색 방지용 딜레이
### 수정/삭제 하셔도 됩니다.
time.sleep(random.randrange(2, 3))

while True:
    # 첫 페이지 탐색
    list_page = bs(response.text, "html.parser")
    news_list = list_page.find("div", {"class": "content"})
    news_list = news_list.find_all("li")

    print("serch page...")

    all_news_df = all_news_df.append(get_content(news_list), ignore_index=True)

    page_indexs = list_page.find("div", {"class": "paging"}).find_all("a")

    # 첫 페이지 이후 페이지가 존재하는지 확인
    if "next" in page_indexs[-1]["class"]:
        news_list_url_list = page_indexs[:-1]
        next_page_url = page_indexs[-1]["href"]
    else:
        news_list_url_list = page_indexs
        next_page_url = None

    # 첫페이지 이후 나머지 페이지 탐색
    for news_list_url in news_list_url_list:
        print("serch page...")
        response = requests.get(
            list_url_base + news_list_url["href"], headers=request_info
        )
        list_page = bs(response.text, "html.parser")
        news_list = list_page.find("div", {"class": "content"})
        news_list = news_list.find_all("li")
        ## df.append 사용 금지!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ## pd.concat 으로 바꿀것!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        all_news_df = all_news_df.append(get_content(news_list), ignore_index=True)

    if next_page_url is None:
        break
    else:
        response = requests.get(list_url_base + next_page_url, headers=request_info)

        time.sleep(random.randrange(1, 2))


# all_news_df.to_csv(
#     f"C:/workspace/naver_news/news_{date}.csv",
#     sep="",
#     quoting=csv.QUOTE_NONE,
#     escapechar="|",
# )

# %%
# db접근 엔진 생성
### 기본적으로 localdb에 접근하도록 되어있음.
### 다른 서버 접근 필요시 db_connection_str 직접 수정

db_id = db_info["id"]
db_psw = db_info["psw"]
db_name = db_info["db_name"]

db_connection_str = f"mysql+pymysql://{db_id}:{db_psw}@127.0.0.1/{db_name}"
db_connection = create_engine(db_connection_str)

# 최종 Dataframe을 db에 적제

# mode = "append"
mode = "replace"

all_news_df.to_sql(name="news", con=db_connection, if_exists="replace", index=False)
