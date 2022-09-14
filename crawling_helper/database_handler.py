from mimetypes import init
import pymysql


# 이제 여기에는 데이터 베이스 헨들링 패키지 제작 예정

class db_handler:
    def __init__(self, server, port, user, pw) -> None:
        self.server = server
        self.port = port
        self.user = user
        self.pw = pw


    def connect(self):
        pass

    def close(self):
        pass

    def select_to_dict(self, sql):
        pass
    
    def insert(self, sql):
        pass