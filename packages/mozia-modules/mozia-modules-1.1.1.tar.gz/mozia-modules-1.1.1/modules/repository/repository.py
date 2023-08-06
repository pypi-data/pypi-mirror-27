import pymysql


class DevelopConfiguration:
    host = "172.16.8.147"
    port = 3306
    user = "dba"
    passwd = "123456"
    db = "farfetch"

    def __init__(self):
        print "Default Configuration"


__CONFIGURATION__ = DevelopConfiguration()


def set_repository_configuration(configuration):
    global __CONFIGURATION__
    __CONFIGURATION__ = configuration


class Repository:
    @staticmethod
    def configure(configuration):
        global __CONFIGURATION__
        if configuration.get("host"):
            __CONFIGURATION__.host = configuration["host"]

        if configuration.get("port"):
            __CONFIGURATION__.port = configuration["port"]

        if configuration.get("user"):
            __CONFIGURATION__.user = configuration["user"]

        if configuration.get("passwd"):
            __CONFIGURATION__.passwd = configuration["passwd"]

        if configuration.get("db"):
            __CONFIGURATION__.db = configuration["db"]

    def __init__(self, host=None,
                 port=None,
                 user=None,
                 passwd=None,
                 db=None,
                 cursorclass=pymysql.cursors.DictCursor,
                 charset='utf8mb4'):

        host = host or __CONFIGURATION__.host
        port = port or __CONFIGURATION__.port
        user = user or __CONFIGURATION__.user
        passwd = passwd or __CONFIGURATION__.passwd
        db = db or __CONFIGURATION__.db
        print "connect to %s@%s:%s - %s" % (user, host, port, db)
        self.connection = pymysql.connect(host=host,
                                          port=port,
                                          user=user,
                                          passwd=passwd,
                                          db=db,
                                          cursorclass=cursorclass,
                                          charset=charset)
