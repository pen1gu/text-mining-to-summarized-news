from crawling_helper.crawling_function import Cralwer
from crawling_helper.news_summarization import Summarizator

crawler = Cralwer()

crawler.set_search_keyword("코로나")

crawler.selection_crawling_page(2)

c = crawler.get_contents()

print(len(c['contents'][0]))
print(c['contents'])
print(c['contents'][0])

# 여기서 패키지 제작 테스트 하고 나중에 실제 ipynb에서 사용

# 원하는 형태로 list에 적재가 되었음
# 그러면 이제 크롤링을 하는 단계에서는 끝. 전처리를 어떻게 할지 고민할 단계가 되었다