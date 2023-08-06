import json
import time

from keys import KEY_MONITOR_PRODUCT_TASKS
from modules.scheduler.scheudler import RedisTaskScheduler
from repository import dao

task_scheduler = RedisTaskScheduler()


def get_monitor_task_length():
    return task_scheduler.redis.llen(KEY_MONITOR_PRODUCT_TASKS)


def create_monitor_product_tasks():
    task_length = get_monitor_task_length()
    if task_length > 0:
        print "Have task in queue:", task_length
        return

    for monitor_task in dao.product.get_products_from_spider():
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


def crawl_product_for_monitor(monitor_task):
    resource_code = monitor_task["resource_code"]
    catalogs = dao.catalog.get_product_source_urls(resource_code)
    if not catalogs:
        print "No found catalog for resource:", resource_code

    for catalog in catalogs:
        print catalog


if __name__ == "__main__":
    create_monitor_product_tasks()
    task = get_monitor_product_task()
    while task:
        crawl_product_for_monitor(task)
        task = get_monitor_product_task()
