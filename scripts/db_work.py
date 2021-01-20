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

class DB_work:
    PATH_DB = '/home/vladislav/var/tsd.sqlite'

    def __init__(self, *args, use_db=False):
        self.con = sqlite3.connect(self.PATH_DB) if use_db else False

    def db_get_article_data(self, PAGENAME_PREFIX, articlename, tablename):
        self.page_data = {}
        with self.con:
            cursor = self.con.cursor()
            # cursor.execute(
            # 	"UPDATE tsd1 SET do = 1 WHERE pagename LIKE '%/ДО'; UPDATE tsd1 SET do = 0 WHERE pagename NOT LIKE '%/ДО';")
            # cursor.execute("""
            # 	UPDATE tsd1 SET scan_from = NULL WHERE scan_from LIKE '';
            # 	UPDATE tsd1 SET book_from = NULL WHERE book_from LIKE '';
            # 	UPDATE tsd1 SET scan_to = NULL WHERE scan_to LIKE '';
            # 	UPDATE tsd1 SET book_to = NULL WHERE book_to LIKE '';
            # 	UPDATE tsd1 SET volume = NULL WHERE volume LIKE '';	""")
            pn_ = PAGENAME_PREFIX + '/' + articlename
            for pn in [pn_, pn_ + '/ДО']:
                cursor.execute("SELECT * FROM %s WHERE pagename = ?" % tablename, (pn,))
                r = cursor.fetchall()
                if len(r):
                    # если нет данных по статье СО попробовать ДО
                    break

            for p in r:
                self.page_data = {
                    'pagename': p[0],
                    'numscan_from_in_tag': p[1],
                    'booknum_from': p[2],
                    'numscan_to_in_tag': p[3],
                    'booknum_to': p[4],
                    'volume': p[5],
                    'do': p[6],
                    'onlysection': p[7],
                    'article_name': p[8],
                }
            pass

    def db_save_pagedata(self, data, table, path=''):
        d = {
            # 'index': self.page_data.get('index', 'NULL'),
            'pagename': self.page_data.get('pagename'),
            'article_name': self.page_data.get('article_name'),
            'volume': self.page_data.get('volume'),
            # 'indexpage': self.page_data.get('indexpage'),
            'onlysection': self.page_data.get('onlysection'),
            # 'fromsection': self.page_data.get('fromsection'),
            # 'tosection': self.page_data.get('tosection'),
            'numscan_from_in_tag': self.page_data.get('numscan_from_in_tag'),
            'numscan_to_in_tag': self.page_data.get('numscan_to_in_tag'),
            # 'offset': self.page_data.get('offset'),
            'booknum_from': self.page_data.get('booknum_from'),
            'booknum_to': self.page_data.get('booknum_to'),
            'do': self.page_data.get('do'),
            # --'obj': self.page_data.get('obj')
            # --'wikicode': self.page_data.get('wikicode')
            # --'tag_pages': self.page_data.get('tag_pages')
        }
        # con = sqlite3.connect(self.PATH_DB)
        with self.con:
            cur = self.con.cursor()
            # cur.execute("""	""")
            # q = "INSERT INTO %s VALUES(%s);" % (table, ','.join(['?'] * len(d.keys())))
            # k = ','.join(['"%s"' % k for k in list(d.values())])
            # v = ','.join(['"%s"' % k for k in list(d.values())])
            # q = "INSERT INTO %s (%s) VALUES(%s);" % (table, k, v)
            q = "INSERT INTO %s (%s) VALUES(%s);" % (table, d.keys(), d.values())
            # cur.executemany(q, d)
            # cur.execute("INSERT INTO %s VALUES(%s);" % (table, ','.join(['?'] * len(d.keys()))), d)
            cur.execute("INSERT INTO %s VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);" % table,
                        list(d.values()))  # [d]
