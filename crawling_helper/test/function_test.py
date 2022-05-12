from cmath import log
import re

import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import logging
from company_id import it_companys
from datetime import date, datetime,timedelta



#TODO: 내가 필요한 naver news의 tag들 -> oid, date, page

logging.basicConfig(level=logging.info)
logger = logging()

class Crawler:
    def __init__(self):
        self.topic = ""
        self.urls_info = []
        self.title = ""


    # TODO: Topic을 정하면 그 분야에 있는 모든 회사거를 가져오도록 시행해보자
    def set_search_topic(self, topic): #FIXME: 키워드가 아닌 oid, 선택 분야가 필요하다.
        # 키워드가 빠져있어야 하는 이유는 다른 메서드, 데이터 저장할 때 search가 topic이 되기 때문이다.
        self.topic = topic

    def get_topic_url(self):

        topic = self.topic

        # TODO: Topic에 따른 인자를 유동적으로 수정할 수 있게 모든 Topic에 대한 정보를 넣는다.
        
        pass

    def get_pages_count(self, url) :
        try:
            original_html = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0'})
            html = BeautifulSoup(original_html.text, "html.parser")
            time.sleep(0.01)
        except Exception as ex:
            logging.exception('crawling error : ')

        count = int(html.select("#main_content > div.paging > strong")[0].text)

        return count

    # IT/과학의 분야 별로 tag를 나눠서
    def selection_crawling_to_date(self, days = 1):
        # 사실 무조건 몇 페이지를 가져오는 것 보다는 batch 파일로 만들어서 하루에 하나 씩 그 전날에 올라온 뉴스들을 크롤링하는게 편함
        # 그러면 페이지로 크롤링하는 기능 하나, 일별로 크롤링하는 기능 하나 이렇게 2개를 만들자

        # 몇쪽부터 몇쪽까지 할지

        '''TODO: 회사 별로 oid 라는게 url에서 작용됨 이를 정의 필요

            date는 원하는 날짜만큼 현재 날짜 - 1 에서빼서 사용. (맨 처음 한번만 할거기에)
            page는 유동적으로 총 몇 페이지인지 구할 수 있을까?
            임의로 최대값을 넣을 시 가장 마지막 페이지를 가리킴 -> default를 10으로 하기 (그 뒤는 X)
            어떤 종목인지, 분야 관련주인지 무엇을 예측할건지에 대한 정의도 필요하다.
        '''
        #main_content > div.paging > strong

        # FIXME: 나중에 선택이 가능하도록 시행 -> 현재는 "디지털 데일리" 
        # https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=138&date=20220510&page=2


        for i in range(days+1, 1, -1):
            # current url
            pages = self.get_pages_count("https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=" + \
                str(138) + "&date=" + (datetime.now() - timedelta(days=i)).strftime("%Y%m%d") + "&page=" + str(10)       
            )   

            url = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=" + \
            str(138) + "&date=" + (datetime.now() - timedelta(days=i)).strftime("%Y%m%d") + "&page=" + str(pages)               

            self.urls_info.append(
                {   
                    'url':url,
                    'page_count' : pages
                 }
            )

    # default로 하루 동안으로 해둘거고, 맨 처음 돌릴 때 6달 돌릴 생각
    # 분야 별로 

    def get_articles(self):
        # html불러오기
        urls_info = self.urls_info

        for url in urls_info:
            #TODO: url을 어떻게 불러올지 구상 필요
            url['url']
            pass

        # 한 토픽, 한 페이지, 페이지의 기사 -> ex) 1 topic, 10 days, 3pages, 10news

        original_html = requests.get(1, headers={'User-Agent': 'Mozilla/5.0'})
        html = BeautifulSoup(original_html.text, "html.parser")
        time.sleep(0.01)
        # 검색결과
        
        articles = html.select("#section_body")
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
