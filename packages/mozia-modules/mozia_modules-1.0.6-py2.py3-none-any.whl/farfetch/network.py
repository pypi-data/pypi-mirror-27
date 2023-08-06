# -*- coding: UTF-8 -*-
import urllib


def download(url):
    try:
        page = urllib.urlopen(url)
        return page.read()
    except Exception as e:
        print(e)


# 内容不全重新下载
def download_image(url, filename):
    try:
        urllib.urlretrieve(url, filename)
    except urllib.ContentTooShortError:
        print 'Network conditions is not good.Reloading.', url
        download_image(url, filename)
