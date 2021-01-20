#!/usr/bin/env python3
# coding: utf-8
# from io import StringIO
# from xml.etree import ElementTree as ET
# import mwparserfromhell
# from pywikibot import xmlreader
from vladi_helpers.file_helpers import file_readtext, filepaths_of_directory, file_savetext
from scripts import Parse_to_wiki, mkindexpage, Pagedata
from wikiworks_data import WorkMeta
from urllib.parse import urlparse, parse_qs, parse_qsl, unquote, quote

if __name__ == '__main__':
    m = WorkMeta()
    if m.to_NSpages:
        m.files_to_list()
    else:
        m.csv_to_list()

    # расстановка шаблона {{перенос}} на страницы со словом, и {{перенос2}} на след. страницы
    mkindexpage.perenos_slov(m.pages)

    # форматировать страницы для ПИ Страница
    m.format_pages_to_NSpage()

    # форматировать файл для pwb
    m.make_pwb_file()
