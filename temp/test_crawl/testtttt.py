from function_test import Crawler
from datetime import date, datetime, timedelta
c = Crawler()

# print(c.get_pages_count("https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=" + \
#                 str(138) + "&date=" + (datetime.now() - timedelta(days=1)).strftime("%Y%m%d") + "&page=" + str(10)       
# ))

c.selection_crawling_to_date(days=5)
print(c.urls_info)

