"""
Using scrapy shell methods in Jupyter notebook.
"""
import os
from random import choice
import requests
from os import path
from scrapy.http import TextResponse
from werkzeug.local import LocalProxy

from .fileutil import write_file

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

_here = path.abspath(path.dirname(__file__))

_DEFAULT_ENCODING = 'utf-8'
_resp = [None]
response = LocalProxy(lambda: _resp[0])

user_agents = [line for line in open(path.join(_here, 'user_agents.txt'), 'r').read().split('\n')]
user_agent = LocalProxy(lambda: choice(user_agents))


def fetch(url, *args, **kwargs):
    """fetch url. Update response"""
    resp = requests.get(url, *args, **kwargs)
    resp.encoding = _DEFAULT_ENCODING
    fetch_from_response(resp)


def fetch_from_response(res):
    """Update local response from requests response"""
    resp = TextResponse(res.url, body=res.text, encoding=_DEFAULT_ENCODING)
    global _resp
    _resp[0] = resp


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
