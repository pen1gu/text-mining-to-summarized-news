import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests as req
from abc import *
import re


# 뉴스 회사는 딱 3개 정도로만 지정하자

class Crawler:
    def __init__(self):
        return

    @abstractmethod
    def crawling(self, news_url):
        pass


# 각 뉴스 회사 별로 contents 태그가 다르니 하나하나 늘려가면서 코딩해보자
# 이거 너무 까다로워서 잠깐 중지


class SeoulEconomyCrawler(Crawler):
    def __init__(self):
        super(SeoulEconomyCrawler, self).__init__()

    def crawling(self, news_url):
        news_list = []
        # regex = re.compile('')  # 정규식 작성

        for element in news_url:
            news = requests.get(element)
            news.encoding = 'utf-8'
            news_html = BeautifulSoup(news.text, 'html.parser')
            news_text_area = news_html.find_all('#dic_area')
            # news_text_area  # 정규식 적용
            news_list.append(news_text_area)

        return news_list

    # 크롤링된 p 태그들은 전부 replace 해서 원본만 남기도록 한다.
