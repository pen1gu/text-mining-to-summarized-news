import re

import pandas as pd
from bs4 import BeautifulSoup
import requests
import time


# 근데 이제 제목이랑 contents를 mapping을 하고 그 다음에 contents 요약이 필요하다.

class Crawler:
    def __init__(self):
        self.search = ""
        self.url = ""
        self.title = ""

    def set_search_keyword(self, search):
        # 키워드가 빠져있어야 하는 이유는 다른 메서드, 데이터 저장할 때 search가 topic이 되기 때문이다.
        self.search = search

    def selection_crawling_page(self, page):
        # 사실 무조건 몇 페이지를 가져오는 것 보다는 batch 파일로 만들어서 하루에 하나 씩 그 전날에 올라온 뉴스들을 크롤링하는게 편함
        # 그러면 페이지로 크롤링하는 기능 하나, 일별로 크롤링하는 기능 하나 이렇게 2개를 만들자
        page_num = 0

        if page == 1:
            page_num = 1
        elif page == 0:
            page_num = 1
        else:
            page_num = page + 9 * (page - 1)

        # url 생성
        self.url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + self.search + "&start=" + str(
            page_num)

    def 몇일동안의_뉴스를_크롤링할지(self, days):
        # 이제 여기에 네이버 기본 필터에 저장되어있는 날짜 별 링크 제작 시스템을 만들어야한다.
        # parameter 설명 적어야됨 이게 일정하지가 않아
        pass

    def get_articles(self):
        # html불러오기
        original_html = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        html = BeautifulSoup(original_html.text, "html.parser")
        time.sleep(0.01)
        # 검색결과
        
        articles = html.select("div.group_news > ul.list_news > li div.news_area > a")
        # 검색된 기사의 갯수
        return articles

    def get_titles(self):
        # 뉴스기사 제목 가져오기
        # Q1. 여기서 제목과 특정 행동과의 상관관계를 구하자

        news_title = []
        articles = self.get_articles()
        time.sleep(0.01)
        for i in articles:
            news_title.append(i.attrs['title'])
        return news_title

    def get_urls(self):
        # 처음 URL 작성할 때 날짜 기준 자체도 넣으면 좋을듯
        news_urls = []
        articles = self.get_articles()
        time.sleep(0.01)
        for i in articles:
            news_urls.append(i.attrs['href'])
        return news_urls

    def get_contents(self):
        contents_df_list = []
        news_url = self.get_urls()
        news_title = self.get_titles()

        time.sleep(0.01)

        print("{0}개의 기사가 검색됨".format(len(news_url)))

        for url, title in zip(news_url, news_title):
            # 각 기사 html get하기
            news = requests.get(url)  # url 리스트에서 하나 가져옴
            news.encoding = 'utf-8'  # 크롤링 시 텍스트 인코딩
            news_html = BeautifulSoup(news.text, "html.parser")  # 어떻게 가져올지

            text = news_html.find_all('p')  # p 태그 전부 찾기

            craw_list = text[:]  # 가져온 p 태그 리스트 list type으로 저장

            craw_list_str = []
            for element in craw_list:
                processing_contents = self.preprocessing_contents(element.text)
                craw_list_str.append(processing_contents)
            
            # contents가 비어있거나 이상한 값일 시 -1 로 설정
            
            craw_list_str = '\n'.join(craw_list_str)
            contents_df_list.append([title, craw_list_str])  # 제목과 기사 내용 mapping 해서 contents 변수에 저장
        # content_df.append(pd.DataFrame([0, date, title, keyword, company, contents]))

        return pd.DataFrame(contents_df_list, columns=['title', 'contents'])

    def preprocessing_contents(self, contents):  # 정재 안된 contents를 인자로 받음
        # 정재해서 return을 주고 그 다음 함수에서 자연어처리 진행
        # 이 부분에서 지워야할 텍스트 지정하는 단계가 필요하다

        # replace

        contents = contents.replace({
            '\\n': '',
            '\\t': '',
            '\\r': '',
        })

        if contents is None:
            contents = -1

        # remove

        return contents
