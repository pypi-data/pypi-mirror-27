# -*- coding: UTF-8 -*-
import json
import time
import logging
import farfetch.network
import re
import os
import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(os.path.basename(__file__))

from farfetch.keys import KEY_MONITOR_PRODUCT_TASKS
from modules.scheduler import task_scheduler
from repository import dao
from modules.repository import repositories


def get_monitor_task_length():
    return task_scheduler.redis.llen(KEY_MONITOR_PRODUCT_TASKS)


def create_monitor_product_tasks():
    task_length = get_monitor_task_length()
    if task_length > 0:
        print "Have task in queue:", task_length
        return

    for monitor_task in dao.monitor.get_monitor_products():
        print "create monitor task:", monitor_task
        monitor_task["time"] = int(time.time())
        task_scheduler.push(KEY_MONITOR_PRODUCT_TASKS, json.dumps(monitor_task))


def get_monitor_product_task():
    task_length = get_monitor_task_length()
    print "tasks in queue:", task_length
    task_string = task_scheduler.pop(KEY_MONITOR_PRODUCT_TASKS)
    if not task_string:
        return None
    return json.loads(task_string)


def get_product_sizes_url(product_id, store_id, category_id, manufacturer_id):
    url = "https://www.farfetch.cn/it/product/GetDetailState?productId=%s&storeId=%s&sizeId=&categoryId=%s&designerId=%s"
    return url % (product_id, store_id, category_id, manufacturer_id)


def is_from_farfetch(monitor_task):
    source_url = monitor_task["source_url"]
    return source_url.startswith("https://www.farfetch.cn/")


def is_need_crawl(monitor_task):
    last_crawl = dao.monitor.get_last_crawl_time(monitor_task["product_id"])
    if not last_crawl:
        return True

    # 两小时内不重复爬
    date_modified = last_crawl["date_modified"]
    passed_seconds = ((datetime.datetime.now() - date_modified).total_seconds())
    return passed_seconds > 3600 * 2


def check_platform_product_sizes(monitor_task, source_sizes):
    platform_product = dao.monitor.get_platform_product(monitor_task["product_id"])
    if not platform_product:
        print("platform product no exists", monitor_task["product_id"])
        return True

    platform_product_sizes = platform_product.get("skus")

    # 平台商品没有sku,直接下架
    if not platform_product_sizes or len(platform_product_sizes) == 0:
        print("platform product no sizes:", monitor_task["product_id"])
        dao.monitor.set_platform_product_status(monitor_task["product_id"], 0)

    source_sizes_mapped = {}
    for size in source_sizes:
        size_name = ("%s[%s]" % (size["Description"], size["ScaleDescription"])).upper()
        source_sizes_mapped[size_name] = size
        source_sizes_mapped[size["Description"]] = size

    close_size_number = 0
    for size in platform_product_sizes:
        if not source_sizes_mapped.get(size["size"].upper()):
            dao.monitor.set_platform_product_sizes_status(monitor_task["product_id"], size["size"], "OFF")
            close_size_number += 1

    return len(platform_product_sizes) > close_size_number


def crawl_product_for_monitor(monitor_task):
    if not is_from_farfetch(monitor_task):
        return

    # if not is_need_crawl(monitor_task):
    #     return

    source_url = monitor_task["source_url"].replace("https://www.farfetch.cn/cn/", "https://www.farfetch.cn/it/")
    monitor_task["source_url"] = source_url
    monitor_task["source_type"] = "FARFETCH"
    timestamp = int(time.time())

    print "begin task:", json.dumps(monitor_task)
    page = farfetch.network.download(source_url)

    if re.search("HTTP/1.0 500 Server Error", page):
        print("farfetch server error, sleep 30s")
        time.sleep(30)
        return

    soup = BeautifulSoup(page, "html.parser")

    sold_out_soup = soup.find("div", class_="soldOut color-red bold h4")
    if sold_out_soup:
        sold_out_string = sold_out_soup.string.strip()
        print("product sold out:", sold_out_string)
        dao.monitor.set_platform_product_status(monitor_task["product_id"], 0)
        dao.monitor.update_crawl_time(monitor_task, 0)
        return

    script_soup = soup.find("script", text=re.compile("window.universal_variable.product\s*=\s*"))

    # 找不到商品信息
    if not script_soup:
        # 商品已售罄
        print "product sold out:", json.dumps(monitor_task)
        dao.monitor.set_platform_product_status(monitor_task["product_id"], 0)
        return

    product = json.loads(
        script_soup.string.strip().replace("window.universal_variable.product =", "").strip().rstrip(";"))
    sizes_url = get_product_sizes_url(product["id"], product.get("storeId"), product["categoryId"],
                                      product["manufacturerId"])

    sizes_string = farfetch.network.download(sizes_url)
    if sizes_string:
        sizes_info = json.loads(sizes_string)["SizesInformationViewModel"]
        sizes = sizes_info["AvailableSizes"]
        if not sizes:
            print "[%s]product no available sizes" % monitor_task["product_id"], monitor_task["source_url"]
            dao.monitor.set_platform_product_status(monitor_task["product_id"], 0)
            dao.monitor.update_crawl_time(monitor_task, 0)
        else:
            # TODO: 这里需要处理尺码已下架的情况
            if check_platform_product_sizes(monitor_task, source_sizes=sizes):
                dao.monitor.update_crawl_time(monitor_task, 1)
            else:
                print "[%s]product all size closed" % monitor_task["product_id"], monitor_task["source_url"]
                dao.monitor.update_crawl_time(monitor_task, 0)
    else:
        # 没有尺码则下架
        print "product no size info:", sizes_string
        dao.monitor.set_platform_product_status(monitor_task["product_id"], 0)
        dao.monitor.update_crawl_time(monitor_task, 0)

    print "end task, cost(%d):" % (int(time.time()) - timestamp), monitor_task["product_id"]


def start_farfetch_monitor():
    create_monitor_product_tasks()
    task = get_monitor_product_task()
    while task:
        crawl_product_for_monitor(task)
        task = get_monitor_product_task()


if __name__ == "__main__":
    task_scheduler.connect()
    repositories.connect()
    task = {"spider_product_id": 1924, "product_id": 27102,
            "source_url": "https://www.farfetch.cn/it/shopping/women/moschino-rat-a-porter--item-11978207.aspx?storeid=9306&from=listing&ffref=lp_pic_7_102_",
            "source_type": "FARFETCH", "flag": "001", "time": 1515038438, "resource_code": "11978207"}

    crawl_product_for_monitor(task)
