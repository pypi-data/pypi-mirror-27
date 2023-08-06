import pymysql


class Repository:
    def __init__(self, host='172.16.8.147', port=3306, user='dba', passwd='123456', db='farfetch'):
        self.connection = pymysql.connect(host=host,
                                          port=port,
                                          user=user,
                                          passwd=passwd,
                                          db=db,
                                          cursorclass=pymysql.cursors.DictCursor,
                                          charset='utf8mb4')
