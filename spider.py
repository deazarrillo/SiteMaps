from urllib.request import urlopen
import urllib.error
from link_finder import LinkFinder
from general import *


class Spider:
    # Class variables (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = f'{Spider.project_name}/queue.txt'
        Spider.crawled_file = f'{Spider.project_name}/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        # first spider creates a directory first
        create_project_dir(Spider.project_name)
        # then it creates the two data files: queue and crawled
        create_data_files(Spider.project_name, Spider.base_url)
        # then it takes links and converts them to a set
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url, priority=10):
        if page_url not in Spider.crawled:
            print(f'{thread_name} now crawling {page_url} @ priority {priority}')
            print(f'Queue {str(len(Spider.queue))} | '
                  f'Crawled {str(len(Spider.crawled))}')
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)

            if 'text/html' \
                    or 'text/html; charset=UTF-8' \
                    or 'text/html; charset=iso-8859-1' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except urllib.error.HTTPError as e:
            print(page_url)
            print('HTTPError: {}'.format(e.code))
            return set()
        except UnicodeDecodeError as e:
            print('decoding error based on the UTF-8 assumption')
            print(page_url)
            return set()
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            # bypassing external urls!
            if Spider.domain_name not in url:
                continue
            # How to make more dynamic?
            if 'howard.edu' not in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
