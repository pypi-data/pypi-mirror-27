"""
Using scrapy shell methods in Jupyter notebook.
"""
import os

import requests
from scrapy.http import TextResponse
from aollio.fileutil import write_file

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

response = None

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

_DEFAULT_ENCODING = 'utf-8'


def fetch(url):
    """fetch url. Update response"""
    resp = requests.get(url)
    resp.encoding = _DEFAULT_ENCODING
    fetch_from_response(resp)


def fetch_from_response(res):
    """Update local response from requests response"""
    resp = TextResponse(res.url, body=res.text, encoding=_DEFAULT_ENCODING)
    global response
    response = resp


def _platform():
    return os.uname().sysname


def _get_var_path():
    platform = _platform()
    var_path = ''
    if platform == 'Darwin':
        # macOs
        var_path = '/tmp/'
    assert var_path, 'unknown system platform.'
    return var_path


def view(resp=None):
    if not resp:
        resp = response
    path = _get_var_path() + resp.url.replace('/', '') + '.html'
    write_file(path, resp.text.encode(), bytes_mode=True)
    os.system('open %s' % path)


if __name__ == '__main__':
    fetch('http://jianshu.com')
    view()
