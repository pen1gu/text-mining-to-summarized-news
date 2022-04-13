import requests
from bs4 import BeautifulSoup

raw = requests.get('https://finance.naver.com/news/news_list.naver', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'})
html = BeautifulSoup(raw.text, "html.parser")

articles = html.select("#contentarea_left > ul > li.newsList.top")

title = articles[0].select_one("dl > dd:nth-child(2)")
source = articles[0].select_one("dl > dd:nth-child(3)")

print(title, source)
