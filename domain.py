import urllib
from urllib.parse import urlparse


# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return f'{results[-2]}.{results[-1]}'
    except:
        return ''


# Get sub domain name (name.example.edu)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


# When testing the below code, we get the netloc of archive.org not of
# howard.edu which I don't think will give us the results we want
# print(get_domain_name('https://web.archive.org/web/20080105102909/http://www.howard.edu/'))
