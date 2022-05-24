import threading
from queue import PriorityQueue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'howard'
HOMEPAGE = 'https://web.archive.org/web/20000510121541/http://www.howard.edu/'
# DOMAIN_NAME = get_domain_name(HOMEPAGE) # This will produce archive.org
DOMAIN_NAME = 'howard.edu'
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4
# below is defining thread queue
queue = PriorityQueue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        (priority, url) = queue.get()
        Spider.crawl_page(threading.current_thread().name, url, priority)
        queue.task_done()


# Define a priority based on the contents of the URL
# Note that this is initially intentionally naive
def get_priority(link) -> int:
    priority = 10
    high_priority = 1
    med_priority = 5
    high_priority_keys = ['faculty', 'people']
    med_priority_keys = ['dept', 'departments']

    # Check if any terms in the set of keys above is in the URL
    # > assign a "higher" priority if so for presedence in processing
    priority = med_priority if any(u in link for u in med_priority_keys) else priority
    priority = high_priority if any(u in link for u in high_priority_keys) else priority

    return priority


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        priority = get_priority(link)
        queue.put((priority, link))
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(f'{str(len(queued_links))} links in the queue')
        create_jobs()


create_workers()
crawl()
