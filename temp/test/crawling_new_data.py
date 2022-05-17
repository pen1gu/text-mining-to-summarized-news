# 뉴스 데이터 불러오는 파일을 만들어보자
# 1. 어떤 플랫폼에서 가져올지
# 2. 어떤 주제를 가져올지
# 3. 어떤 키워드로 가져올지

# Ch_selenium/example/tutorial1.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests as req

# 창 숨기는 옵션 추가
options = webdriver.ChromeOptions()
options.add_argument("headless")

# 웹 드라이버
driver = webdriver.Chrome('C:\hjun\webdriver\chromedriver.exe', options=options)
# 네이버 금융

search = driver.get('https://news.naver.com/main/list.naver')

driver.find_elements_by_xpath('//*[@id="lnb"]/ul/li[6]/a')[0].click()
driver.find_elements_by_xpath('//*[@id="snb"]/ul/li[5]/a')[0].click()

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

information_list = []

for i in range(1, 5):
    s = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li:nth-child({0})'.format(i))
    information_list.append(s)

    print(s[0])

    # 이제 이 안에서 링크를 들어가서 내용을 요약 할건지 선택

    # 우선 기본 요약 부분만 가지고 틀을 짜자.
    # 물론 넘겨 받는 부분만 나누어서 나중에 내부를 요약해서 가져와도 상관없도록 설계 필요

# dataframe으로 날짜, 제목, 키워드, 기사 넣기
# 오늘은 기사 별 html 긁어옴

# print(information_list)
