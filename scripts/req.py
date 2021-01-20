#!/usr/bin/env python3
# coding: utf-8
import requests
import sqlite3
import json
from lxml.html import fromstring
import re
from urllib.parse import urlencode, urlsplit, parse_qs, parse_qsl, unquote, quote
# from vladi_helpers import vladi_helpers
# from vladi_helpers.file_helpers import json_save_to_file, json_load_from_file

class Req:
    def __init__(self, wiki_lang='ru', wiki_project='wikisource'):
        self.wiki_lang = wiki_lang
        self.wiki_project = wiki_project
        self.session = self.open_reqsession()

    def open_reqsession(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0',
            # 'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
            # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/61.0.3163.79 Chrome/61.0.3163.79 Safari/537.36',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept': 'application/json, text/javascript, */*; q=0.01'
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Content-Type': 'x-www-form-urlencoded',
            'Content-Type': 'text/plain;charset=UTF-8',
            # 'Host': 'www.site.ru',
            # 'Referer': 'http://www.site.ru/index.html',
        }
        proxyDict = {
            "http": 'http://212.161.91.178:65103',
            "https": 'https://212.161.91.178:65103',
            # "http": 'http://92.27.91.253:53281',
            # "https": 'https://92.27.91.253:53281',
            # "ftp"   : ftp_proxy
        }
        s = requests.Session()
        s.headers = headers
        s.proxies.update(proxyDict)
        return s

    def get_page(self, url=None, title=None):
        if title:
            url = self.make_wiki_url(title)
        if url:
            r = self.session.get(url, params={"action": "render"}, headers={'user-agent': 'user:textworkerBot'})
            if r.status_code == 200:
                html = r.text
                html_parsed = fromstring(r.text)
                return html, html_parsed

    def make_wiki_url(self, title):
        return 'https://' + self.wiki_lang + '.' + self.wiki_project + '.org/wiki/' + quote(title)

