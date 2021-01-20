# -*- coding: utf-8 -*-
import re
import sqlite3
from collections import namedtuple
import pywikibot as pwb
import mwparserfromhell as mwp
import requests
from urllib.parse import urlparse, parse_qs, parse_qsl, unquote, quote
from lxml.html import fromstring
from vladi_helpers.file_helpers import csv_read, csv_save_dict, json_save_to_file, json_load_from_file, \
    file_readtext, file_readlines, file_savelines
from vladi_helpers.vladi_helpers import listdic_pop, lines2list
import vladi_wikihelpers.lib_for_mwparserfromhell
from scripts.db_work import DB_work


class P:
    pagename: str
    article_name: str
    obj: pwb.Page
    wikicode: mwp.wikicode.Wikicode

    # def __init__(self, pagename: str, article_name: str, obj: pwb.Page, wikicode: mwp.wikicode.Wikicode):
    def __init__(self, page_obj: pwb.Page, wmp=True):
        self.parse_page(page_obj, wmp)

    def parse_page(self, page_obj, wmp):
        pagename = page_obj.title(with_section=False)
        self.pagename = pagename
        self.article_name = self.get_cur_article_name(pagename)
        self.obj = page_obj
        self.wikicode = mwp.parse(page_obj.text) if wmp else None

    def get_cur_article_name(self, pagename):
        return self.string_strip(pagename.split('/')[1])

    def string_strip(self, s):
        return str(s).replace('\u200e', '').replace('&lrm;', '').replace('&#8206;', '').strip()


class WikiMethods:
    # LISTPAGES_FILENAME = 'listpages.txt'  # список страниц для обработки
    # REWRITE_EXIST_PAGES = None
    # CLEAN_TEXT_FROM_POSTED = None  # Не ясен смысл и алгоритм очистки текстовки от залитых
    # MAKE_REDIRECTS = None
    PAGENAME_PREFIX = ''
    # PAGENAME_POSTFIX = ''
    # SUMMARY = 'заливка'
    # wordlists_text = []
    lat_redirects = []
    list2rename = []
    # page = ''  # pywikibot object
    # page_wikicode = ''  # mwp object
    pagename = ''
    cur_article_name = ''

    stock_redirects = False
    redirects = []
    page_data = P

    # log = set()  # already_exists_pages
    # re_pagename_from_wikilink = re.compile(r'\[\[%s/(.*?)\s*(?:\||\]\])' % PAGENAME_PREFIX)

    def __init__(self, *args, use_db=False, wiki_lang='ru', wiki_project='wikisource'):
        self.wiki_lang = wiki_lang
        self.wiki_project = wiki_project
        self.SITE = pwb.Site(wiki_lang, wiki_project, user='TextworkerBot')
        # self.PAGELIST_TITLES = str2list(args[0])
        if use_db:
            DB_work()

        # self.get_pagelists()
        # self.parse_wordlist()
        # self.operate_wordlist_pagelinks()

    def get_cur_article_name(self, pagename):
        return self.string_strip(pagename.split('/')[1])

    def open_page(self, pagename, switch_to_RedirectTarget=True, mark_RedirectPages_category=False, wmp=True):
        page_obj = pwb.Page(self.SITE, pagename)
        if page_obj.exists():
            if page_obj.isRedirectPage():
                # для редиректов создание файл-списка переименования для pwb
                RedirectTarget = page_obj.getRedirectTarget()
                if self.stock_redirects:
                    self.redirects.append(pagename)
                    self.redirects.append(RedirectTarget)
                if switch_to_RedirectTarget:
                    page_obj = RedirectTarget
                    pagename = RedirectTarget.title()
                if mark_RedirectPages_category:
                    page_obj.text = page_obj.text + '\n[[Категория:%s]]' % mark_RedirectPages_category
            page_data = P(page_obj, wmp)
            return page_data
        else:
            return None

    def work_dump_xml(self, xml_path):
        from pywikibot import xmlreader
        dump = xmlreader.XmlDump(xml_path)
        yield from dump.parse()
        # for entry in dump.parse():
        #     self.proceess_entry(entry)

    def get_args_from_tagPages(self):
        """парсинг тэга <pages>"""
        tagsPages = [tag for tag in self.page_data.wikicode.filter_tags() if tag.tag.matches('pages')]
        if len(tagsPages) > 1:
            print('%s: len(count_tags) > 1' % self.page_data.pagename)
            return

        elif len(tagsPages) == 1:

            self.page_data.tag_pages = tagsPages[0]
            # 'indexpage': str(tagsPages[0].get('index').value.strip()),
            self.page_data.volume = self.tsd_calc_volume(tagsPages[0].get('index').value, self.EDITION)
            self.page_data.onlysection = str(tagsPages[0].get('onlysection').value) if tagsPages[0].has(
                'onlysection') else ''
            # 'fromsection': str(tagsPages[0].get('fromsection').value) if tagsPages[0].has('fromsection') else '',
            # 'tosection': str(tagsPages[0].get('tosection').value) if tagsPages[0].has('tosection') else '',
            self.page_data.numscan_from_in_tag = str(tagsPages[0].get('from').value.strip())
            self.page_data.numscan_to_in_tag = str(tagsPages[0].get('to').value.strip())

            # self.page_data['offset'] = self.calc_pagenum_offset(str(self.page_data['indexpage']))
            # self.page_data['booknum_from'] = int(self.page_data['numscan_from_in_tag']) - self.page_data['offset']
            # self.page_data['booknum_to'] = int(self.page_data['numscan_to_in_tag']) - self.page_data['offset']
            self.page_data.do = True if 'ДО' in self.page_data.pagename.split('/') else False

    def get_pagestags(self, wikicode):
        return [tag for tag in wikicode.filter_tags() if tag.tag.matches('pages')]

    def add_param_SECTION_in_headertpl(self, sectionname_new):
        """добавление параметра СЕКЦИЯ в шаблон-шапку, иначе удаление параметра"""
        for pagetpl in self.page_data.wikicode.filter_templates():
            if pagetpl.name.matches('ТСД'):
                if sectionname_new != self.cur_article_name:
                    pagetpl.add('СЕКЦИЯ', sectionname_new)
                else:
                    if pagetpl.has('СЕКЦИЯ'):
                        pagetpl.remove('СЕКЦИЯ')

    def string_strip(self, s):
        return str(s).replace('\u200e', '').replace('&lrm;', '').replace('&#8206;', '').strip()

    def update_wordlist_item(self, tpl, wordlist_data, use_pagenum_instead_scannum=True):
        """
        :param tpl: шаблон словника из mwparserfromhell,{{tsds}} и т.п.
        :param wordlist_data:
        :param use_pagenum_instead_scannum:
        :return:
        """
        # self.page_data['pagination_in_tpl'] = re.findall('\d+', self.cur_wl_tpl.get(3).value.strip())
        if use_pagenum_instead_scannum:
            booknum_from = 'booknum_from'
            booknum_to = 'booknum_to'
            if booknum_from in wordlist_data and booknum_to in wordlist_data:
                b_from = wordlist_data[booknum_from]
                b_to = wordlist_data[booknum_to]
                if b_from is None or b_to is None:
                    print('проблема с пагинацией страницы в БД, is None')
                    return
                pagination_book_new = b_from if b_from == b_to else '%s—%s' % (b_from, b_to)
                if tpl.has(3):
                    tpl.get(3).value = pagination_book_new
                else:
                    tpl.add(3, pagination_book_new)
            else:
                pass
            pass
        else:
            # 4-й параметр, страницы скана
            numscan_from_in_tag = 'numscan_from_in_tag'
            numscan_to_in_tag = 'numscan_to_in_tag'
            if numscan_from_in_tag in wordlist_data and numscan_to_in_tag in wordlist_data:
                s_from = wordlist_data[numscan_from_in_tag]
                s_to = wordlist_data[numscan_to_in_tag]
                if s_from is None or s_to is None:
                    print('проблема с пагинацией скана в БД, is None')
                    return
                params_pagination_scan_new = s_from if s_from == s_to else '%s/%s' % (s_from, s_to)
                if tpl.has(4):
                    tpl.get(4).value = params_pagination_scan_new
                else:
                    tpl.add(4, params_pagination_scan_new)
            else:
                pass

        # сдвиг 'p=' в конец
        if tpl.has('p'):
            v = tpl.get('p').value.strip()
            tpl.remove('p')
            tpl.add('p', v)
        pass

    def wiki_posting_page(self, page_obj, text_new, summary, remove_more_newlines=False):
        if remove_more_newlines:
            text_new = re.sub(r'\n\n+', r'\n\n', text_new)
        if page_obj.text != text_new:
            page_obj.text = text_new
            page_obj.save(summary=summary)

    def savelist2rename(self, filename):
        file_savelines(filename, self.list2rename)
        file_savelines('lat_redirects', self.lat_redirects)
