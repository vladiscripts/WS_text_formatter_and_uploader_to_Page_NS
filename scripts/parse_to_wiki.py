#!/usr/bin/env python3
# coding: utf-8
# import requests
# from urllib.parse import quote
# from lxml import etree
from lxml.html import fromstring, tostring
# from lxml import cssselect
# from io import StringIO
# from xml.etree import ElementTree as ET
import re
# import mwparserfromhell
# import pywikibot
# from pywikibot import output, xmlreader
# from vladi_helpers.file_helpers import file_savetext, file_readtext, filepaths_of_directory
from vladi_helpers.vladi_helpers import remove_empty_tags


class Parse_to_wiki:
    re_get_section = re.compile(r'<section[^>]*?>\s*(.*?)\s*</section>', flags=re.DOTALL)
    re_get_section_cite = re.compile(r'<section id=(".*?")>\s*(.*?)\s*</section>', flags=re.DOTALL)

    re_get_body = re.compile(r'<body>\s*(.*?)\s*</body>', flags=re.DOTALL)
    re_clean_roottag = re.compile(r'^<[a-zA-Z]+[^>]*>(.+)</[a-zA-Z]+>$', flags=re.DOTALL)

    # теги p, b, emphasis
    re_tag_b = re.compile(r'</?b>')
    re_tag_strong = re.compile(r'</?strong>')
    re_tag_emphasis = re.compile(r'</?emphasis>')
    re_tag_p = re.compile(r'<p>\s*(.*?)\s*</p>', flags=re.DOTALL)
    re_tag_subtitle = re.compile(r'<subtitle>\s*(.*?)\s*</subtitle>')

    # чистка пробелов и абзацев
    re_spaces_on_strbegin = re.compile(r'^ +', flags=re.MULTILINE)
    re_tag_clean_spaceslineends = re.compile(r'^\s+$', flags=re.MULTILINE)
    re_tag_clean_spaces = re.compile(r' {2,}')
    re_tag_clean_newlines = re.compile(r'\n{2,}')

    # сноски
    re_ref_from_footnotes_to_text = re.compile(r'<ref name="#(bookmark\d+)" */>(.*?)(<ref name="\1" *>.*?</ref>)',
                                               flags=re.DOTALL)

    def dispatcher(self, text, parse_from):
        funcs = {'fb2': self.parseFB2XMLasText, 'htm': self.parseHTMasText, 'txt': self.parseTXTasText}
        text = funcs[parse_from](text)
        text = self.commons_clean(text)
        return text

    def parseFB2XMLasText(self, xml: str):
        xml = self.re_get_section_cite.sub(r'<section id=\1><ref name=\1>\2</ref></section>', xml)
        sections = self.re_get_section.findall(xml)
        if not sections:
            return
        text = '\n'.join(sections)

        text = self.re_tag_p.sub(r'\1\n\n', text)

        # сноски
        text = re.sub(r'<a l:href=("#bookmark\d+") type="note"><sup>\d</sup></a>', r'<ref name=\1 />', text)
        text = text.replace('a l:href', 'ref name').replace(' type="note"', '')
        text = re.sub(r'(<ref name="bookmark\d+">)\s*<title>\s*(<p>[\s*\d]+</p>|[\s*\d]+)?\s*</title>\s*', r'\1', text,
                      flags=re.DOTALL)
        text = re.sub(r'(<ref.*?>)\s*<p>\s*(.*?)\s*</p>\s*(</ref>)', r'\1\2\3', text, flags=re.DOTALL)
        text = re.sub(r'(<ref.*?>)\s*(.*?)\s*(</ref>)', r'\1\2\3', text, flags=re.DOTALL)
        text = re.sub(r'<sup>\s*(<ref[^>]*?/>)\s*</sup>', r'\1', text, flags=re.DOTALL)
        for i in range(20):
            text = self.re_ref_from_footnotes_to_text.sub(r'\3\2', text)
        text = re.sub(r'<ref name="(bookmark\d+)" *>', r'<ref>', text)
        text = re.sub(r'<p>\) *', r'<p>', text)
        text = re.sub(r'(<ref.*?>)\) *', r'\1', text)
        # text = text.replace('</ref>\)', '</ref>')

        text = text.replace('<empty-line/>', '')
        if text == '':
            return ''

        # теги p, b, emphasis
        text = self.re_tag_b.sub("'''", text)
        text = self.re_tag_strong.sub("'''", text)
        text = self.re_tag_emphasis.sub("''", text)
        # text = self.re_tag_subtitle.sub(r"{{центр|\1|рш=200%}}\n", text)
        text = self.re_tag_subtitle.sub(r"{{h3|\1}}\n", text)

        # чистка тегов
        text = text.replace('<sup></sup>', '')
        text = text.replace('<sup> +</sup>', ' ')
        text = re.sub(r'<a name="caption\d+"></a>', '', text)
        return text

    def parseHTMasText(self, html: str):
        # xml = self.re_get_section_cite.sub(r'<section id=\1><ref name=\1>\2</ref></section>', xml)
        dom = fromstring(html)
        html2 = remove_empty_tags(dom, convert_to_str=True, tags_ignore=['br', 'img', 'a', 'span'])

        # body = self.re_get_body.search(html)
        body = self.re_clean_roottag.search(html2)
        if not body:
            return
        text = body.group(1)

        text = self.re_tag_p.sub(r'\1\n\n', text)

        # # сноски
        # text = re.sub('<a l:href=("#bookmark\d+") type="note"><sup>\d</sup></a>', r'<ref name=\1 />', text)
        # text = text.replace('a l:href', 'ref name').replace(' type="note"', '')
        # text = re.sub('(<ref name="bookmark\d+">)\s*<title>\s*(<p>[\s*\d]+</p>|[\s*\d]+)?\s*</title>\s*', r'\1', text,
        #               flags=re.DOTALL)
        # text = re.sub('(<ref.*?>)\s*<p>\s*(.*?)\s*</p>\s*(</ref>)', r'\1\2\3', text, flags=re.DOTALL)
        # text = re.sub('(<ref.*?>)\s*(.*?)\s*(</ref>)', r'\1\2\3', text, flags=re.DOTALL)
        # text = re.sub(r'<sup>\s*(<ref[^>]*?/>)\s*</sup>', r'\1', text, flags=re.DOTALL)
        # for i in range(20):
        #     text = self.re_ref_from_footnotes_to_text.sub(r'\3\2', text)
        # text = re.sub(r'<ref name="(bookmark\d+)" *>', r'<ref>', text)
        # text = re.sub('<p>\) *', r'<p>', text)
        # text = re.sub('(<ref.*?>)\) *', r'\1', text)
        # text = text.replace('</ref>\)', '</ref>')
        # text = text.replace('<empty-line/>', '')
        # if text == '':
        #     return ''

        # теги p, b, emphasis
        text = self.re_tag_b.sub("'''", text)
        text = self.re_tag_emphasis.sub("''", text)
        text = self.re_tag_subtitle.sub(r"{{центр|\1|рш=200%}}\n", text)

        # чистка тегов
        for _ in range(5):
            # text = re.sub('(<span\s+style="[^"]*?)font-weight:bold;([^"]*?">)(.*?</span>)', r"\1\2'''\3'''", text)
            text = re.sub(r'font-weight:bold;', '', text)  # жирный удалять
            text = re.sub(r'(<span\s+style="[^"]*?)font-style:italic;([^"]*?"\s*>)(.*?</span>)', r"\1\2''\3''", text)
            text = re.sub(r'<span\s+style="">(.*?)</span>', r'\1', text)

            text = text.replace('<sup></sup>', '')
            text = text.replace('<div></div>', '')
            text = text.replace('<br clear="all"/>', '\n')
            text = re.sub(r'<a name="caption\d+"></a>', '', text)
            text = re.sub(r'class="font\d"', ' ', text)
            text = re.sub(r'<span *>(.*?)</span>', r'\1', text)
            text = re.sub(r'<a (name|href)="#?(footnote|bookmark)\d*">[^<]*?</a>', '', text)

        return text

    def parseTXTasText(self, txt: str):
        txt = txt.replace('\uFEFF', '')
        return txt

    def commons_clean(self, text):

        # нормализация пунктуации
        # text = text.replace('|', "{{!}}")
        text = re.sub(r'([^a-z])=([^a-z"\'])', r"\1{{=}}\2", text)
        text = text.replace('—', ' — ')
        text = re.sub(r'(\d)\s*—\s*(\d)', r'\1—\2', text)
        text = text.replace(' ,', ',')

        # чистка пробелов и абзацев
        text = self.re_spaces_on_strbegin.sub('', text)
        text = self.re_tag_clean_spaceslineends.sub('', text)
        text = self.re_tag_clean_spaces.sub(' ', text)
        text = self.re_tag_clean_newlines.sub('\n\n', text)
        return text

    #
    # def work_xml_wikidump(self, PATHTOXML: str):
    #     dump = xmlreader.XmlDump(PATHTOXML)
    #
    #     # readPagesCount = 0
    #     for entry in dump.parse():
    #         if int(entry.ns) not in [NS_PAGE] \
    #                 or not entry.title.startswith('Страница:Толковый словарь Даля (2-е издание)'):
    #             # or not entry.title.startswith('РСКД/') \
    #             # or 'РСКД/Словник' in entry.title \
    #             # or 'РСКД/Русский указатель статей' == entry.title \
    #             # or 'РСКД/Список сокращений названий трудов античных авторов' == entry.title:
    #             continue
    #         # if entry.isredirect:
    #         #     redirects.append(dict(t=entry.title, r=redirect_target_re.search(entry.text).group(1)))
    #
    #         # if 'РСКД/Цезарь' in entry.title:
    #         #     print(entry.title)
    #
    #         # all_found_titles.append(entry.title)
    #
    #         e = dict(page_title=entry.title, page_text=entry.text, )
    #
    #         self.entries.append(e)
    #
    # def parseBookXML(self, xml: str):
    #     # with open(xmlFile) as fobj:
    #     # 	xml = fobj.read()
    #     # xml = txt
    #
    #     root = ET.fromstring(xml)
    #     # root = etree.parse('path_to_file')
    #
    #     ns = {'t': "http://www.gribuser.ru/xml/fictionbook/2.0",
    #           'l': "http://www.w3.org/1999/xlink"}
    #
    #     # b = root.find(".//t:description//t:genre", ns)
    #     # b = root.find(".//t:description", ns)
    #     # a = b.find(".//t:genre", ns).text
    #
    #     for ab in root.findall("t:body", ns):
    #         for s in ab.find('t:section', ns):
    #             a = s.text
    #
    #     parser = ET.XMLParser(ns_clean=True)
    #     tree = ET.parse(StringIO(xml), parser)
    #
    #     # namespaces
    #     NS_MAIN = 2
    #     NS_PAGE = 104
    #
    #     book_dict = {}
    #     books = []
    #     for book in root.getchildren():
    #         for elem in book.getchildren():
    #             if elem.tag != 'page': continue  # work only on pages
    #             if int(elem.ns) not in [NS_PAGE]: continue
    #             if not elem.text:
    #                 text = "None"
    #             else:
    #                 text = elem.text
    #             print(elem.tag + " => " + text)
    #             book_dict[elem.tag] = text
    #
    #             if book.tag == "book":
    #                 books.append(book_dict)
    #                 book_dict = {}
    #
    #     return books
