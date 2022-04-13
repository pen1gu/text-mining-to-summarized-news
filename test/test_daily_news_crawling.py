import pandas as pd
import numpy as np
import feedparser
from bs4 import BeautifulSoup as bs
import urllib
import urllib.request as req
import requests
from konlpy.tag import Kkma, Okt, Komoran

okt = Okt()
from konlpy.utils import pprint
import warnings

warnings.filterwarnings("ignore")

href_list = []  # 기사 주소가 들어갈 리스트
TitDesc_list = []  # 제목 + 요약 내용 리스트
title_list = []  # 제목 리스트


def Crawling(keyword, date):
    keyword = '+'.join(keyword.split(' '))

    last = False
    page_num = 1

    ds = date
    de = ds
    while last == False:
        url = "https://search.naver.com/search.naver?&where=news&query={0}".format(
            keyword
        )
        raw = requests.get(url)
        html = raw.content
        soup = bs(html, 'html.parser')

        ul = soup.find('ul', {'class': 'list_news'})
        li_list = ul.findAll('li')

        for li in li_list:
            try:
                href_list.append(li.dl.dt.a['href'])

                d_list = li.findAll('dd')
                # 자식 노드 dd가 두 개인데 두 번째 노드에 description이 들어가있으므로 전부 불러온 후 인덱싱할 것임

                title = li.dl.dt.a['title']
                description = d_list[1].text
                # 자식 노드 dd의 두 번째에 들어가 있는 description을 text로 불러옴

                title_list.append(title)
                TitDesc_list.append(title + ' ' + description)
                # 제목과 요약내용을 붙여서 리스트에 넣음
            except AttributeError:
                pass

        # 마지막 페이지 주소 확인 (다음페이지 버튼이 없으면 종료페이지로 간주)
        page = soup.find('div', {'class': 'paging'})
        page_a_list = page.findAll('a')
        if '다음페이지' in str(page_a_list[-1]):
            page_num += 10
        else:
            last = True


Crawling('코로나', '2022.01.31')
