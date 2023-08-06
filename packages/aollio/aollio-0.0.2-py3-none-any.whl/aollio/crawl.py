"""
Using scrapy shell methods in Jupyter notebook.
"""

import requests
from scrapy.http import TextResponse
from werkzeug.local import LocalProxy

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

_res = [None]
response = LocalProxy(lambda: _res[-1])

USER_AGENTS = [
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; ']


def fetch(url):
    """fetch url. Update response"""
    resp = requests.get(url)
    fetch_from_response(resp)


def fetch_from_response(res):
    """Update local response from requests response"""
    resp = TextResponse(res.url, body=res.text, encoding='utf-8')
    _res[-1] = resp
