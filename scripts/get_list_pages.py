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
import pywikibot
import re
import sqlite3
from collections import namedtuple
import pywikibot
import mwparserfromhell as mwp
import requests
from urllib.parse import urlparse, parse_qs, parse_qsl, unquote, quote
from lxml.html import fromstring
from vladi_helpers.file_helpers import csv_read, csv_save_dict, json_save_to_file, json_load_from_file, \
    file_readtext, file_readlines, file_savelines
from vladi_helpers.vladi_helpers import listdic_pop, lines2list
import vladi_wikihelpers.lib_for_mwparserfromhell
from scripts.req import Req


class Get_listpages:
    EDITION = 3
    TEXTOVKA_FROM_FILE = 0  # or from wikipage
    PAGELIST_TITLES = []
    LIST_OF_WORDLISTS_FROM_FILE = 1  # or from wikipage
    WORDLIST_TITLES = []
    wordlist_title = ''
    # pagelists_titles = ''
    # pagelist = ''
    # wordlist_text = ''
    # wordlists = []
    # FO = FI + '_pages_to_rename'
    # FI_pagelist = '/home/vladislav/var/tsd%s_doubles_tagpages.txt' % EDITION
    # FO_pagelist = FI_pagelist + '_pages_to_rename'
    # FI_listpages = '/home/vladislav/var/tsd%s_listpages.txt' % EDITION

    # FO_wl_list = FI_wordlists_list + '_pages_to_rename'
    # FO_wl_text = FI_wl_text + '_pages_to_rename'
    FI = '/home/vladislav/var/tsd%s_worlists.txt' % EDITION
    FI_wordlists_list = '/home/vladislav/var/tsd%s_worlists.txt' % EDITION
    FI_wl_text = '/home/vladislav/var/tsd%s_worlists.txt' % EDITION

    def __init__(self, SITE):
        self.SITE = SITE

    def get_pagelists(self, from_file=True, path=''):
        """PAGELIST_FROM_FILE = True or from wikipage"""
        if from_file:
            self.pagelists_titles = file_readlines(path)
        else:
            for WORDLIST_TITLE in lines2list(self.PAGELIST_TITLES):
                self.pagelist = pywikibot.Page(self.SITE, WORDLIST_TITLE)
                self.pagelists_titles.append(self.pagelist.get())

    def get_lists_of_wordlists(self):
        if self.LIST_OF_WORDLISTS_FROM_FILE == 1:
            self.wordlists_titles = file_readlines(self.FI_wordlists_list)
        else:
            for WORDLIST_TITLE in lines2list(self.WORDLIST_TITLES):
                self.wordlist_page_obj = pywikibot.Page(self.SITE, WORDLIST_TITLE)
                self.wordlists_titles.append(self.wordlist_page_obj.get())

    def get_text_of_wordlist(self):
        if self.TEXTOVKA_FROM_FILE == 1:
            self.wordlist_text = file_readlines(self.FI)
        else:
            self.wordlist = pywikibot.Page(self.SITE, self.wordlist_title)
            self.wordlist_text = self.wordlist.text

    def get_wordlists(self, use_pywikibot=True, use_mwparser=True, get_html=False):
        self.get_lists_of_wordlists()
        # self.parse_wordlist()
        # self.operate_wordlist_pagelinks()
        self.wordlists = []
        for wordlist_title in self.wordlists_titles:
            # for TEXTOVKA_TITLE in lines2list(self.WORDLIST_TITLES):
            # if self.TEXTOVKA_FROM_FILE == 1:
            # 	self.get_text_of_wordlists()
            # self.get_text_of_wordlist()
            w = {
                'title': wordlist_title,
                'obj': None,
                'text': None,
                'wikicode': None,
                'html': None,
                'html_parsed': None,
            }
            if use_pywikibot:
                w['obj'] = page_obj = pywikibot.Page(self.SITE, wordlist_title)
                w['text'] = text_of_wordlist = page_obj.text if self.TEXTOVKA_FROM_FILE != 1 \
                    else file_readlines(self.FI_wl_text)
                w['wikicode'] = mwp.parse(text_of_wordlist) if use_mwparser else None
            if get_html:
                req = Req()
                r = req.get_page(title=wordlist_title)
                if r:
                    w['html'], w['html_parsed'] = r
            self.wordlists.append(w)
