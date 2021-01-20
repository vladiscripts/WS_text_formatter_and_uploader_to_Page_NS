#!/usr/bin/env python3
# coding: utf-8
from io import StringIO
from xml.etree import ElementTree as ET
import re
# import mwparserfromhell
from pywikibot import xmlreader
from vladi_helpers.file_helpers import file_readtext, filepaths_of_directory
# from . import Parse_to_wiki
from . import deyatificator
import roman


def formatting_output_page(page, range_pages_metric, colontitul, VARtpl_wrap=False,
        deyatification=False, do_precorrection=True):
    text = page.parsed_text
    # section_text = mkindexpage.wrap_to_section_tag(page.parsed_text, subpagename)

    if do_precorrection:
        text = precorrection(text)

    # Конвертировать текст в современную орфографию
    page.neworph_text = deyatificator(text) if deyatification else ''

    if VARtpl_wrap:
        text = wrap_to_VARtpl(text.strip(), page.neworph_text.strip())
    book_pn, pagination_style = calc_bookpagenum_by_scanpagenum(page.scanpagenum, range_pages_metric)

    if colontitul['enable']:
        if colontitul['center_only']:
            colontitul_txt = make_colontitul_center_only(book_pn, pagination_style) if book_pn else ''
        else:
            # todo ? range_pages_metric.subpagename
            subpagename = ''
            colontitul_txt = make_colontitul(book_pn, pagination_style=pagination_style, subpagename='')
    else:
        colontitul_txt = ''

    scanpagetext = make_pagetext(text, colontitul_txt, colontitul_on_top=colontitul['on_top'])
    return scanpagetext


def make_pagetext(text, colontitul='', colontitul_on_top=True, header=None, footer=None):
    colontitul_top = colontitul_bottom = ''
    # header_common_begin = '__NOEDITSECTION__<div class="serif">'
    header_common_end = '<div class="indent">'
    header_common_begin = '__NOEDITSECTION__<div class="text">'
    header_common_end = ''
    footer_common = '<!-- -->\n<references />'

    if text.strip() == '':
        header_common_begin = header_common_end = footer_common = colontitul = ''

    if colontitul_on_top:
        colontitul_top = colontitul
    else:
        colontitul_bottom = colontitul

    if not header:
        header = '<noinclude><pagequality level="1" user="TextworkerBot" /><div class="pagetext">' \
                 f'{header_common_begin}{colontitul_top}{header_common_end}</noinclude>'
        if text.strip() == '':
            header = header.replace('pagequality level="1"', 'pagequality level="0"')
        # '<!--<div style="text-align:justify">-->'
    if not footer:
        footer = f'<noinclude>{footer_common}{colontitul_bottom}</div></div></div></noinclude>'
    scanpagetext = f'{header}{text}{footer}'
    return scanpagetext


def make_colontitul(book_pn, subpagename='', pagination_style=False):
    def label_interpages(number: int, string_chet: str, str_nechet: str) -> str:
        """Возвращает строку в зависимости чётная ли страница"""
        return str(string_chet) if not number % 2 else str(str_nechet)

    colontitul = colontitul_center = colontitul_left = colontitul_right = ''

    # colontitul = 'Народная Русь' if not scan_pn % 2 else subpagename  # чередующийся на чётных/нечётных страницах
    # colontitul = (colontitul + '.').upper()  # в верхнем регистре с точкой
    # colontitul = str(page_pn)  # колонтитул — номер страницы
    # чередующийся на чётных/нечётных страницах

    # colontitul = ''
    # first_pages_without_colontitul = True  # на первых страницах без колонтитула

    if book_pn != '':
        book_pn_int = book_pn
        try:
            if not re.match(r'^\d+$', str(book_pn)):
                book_pn_int = roman.fromRoman(book_pn)
        except:
            pass

        if pagination_style is True:
            # todo: toRoman need int
            book_pn = roman.toRoman(book_pn)

            colontitul_left = label_interpages(book_pn_int, book_pn, '')
            colontitul_right = label_interpages(book_pn_int, '', book_pn)
            # римские цифры
            # label_interpages(book_pn, roman.toRoman(book_pn+32), ''),	colontitul_center, label_interpages(book_pn, '', roman.toRoman(book_pn+32))
            # '',	'— ' + str(book_pn) + ' —',	''

        elif pagination_style is None:
            colontitul_left = colontitul_right = ''


    else:
        raise Exception("make_colontitul(), book_pn == ''. Нет номера страницы, вероятно ошибка в указ.диапазона")

    # colontitul_center = colontitul_center.replace(' (ПЛАТОН/КАРПОВ)', '').replace(' (ПСЕВДО-ПЛАТОН/КАРПОВ)', '').replace('КАРПОВ В. Н., ', '').replace('ПОЛИТИКА ИЛИ ГОСУДАРСТВО. ','')
    # if re.search(r'[цкнгшщзхфвпрлджчсмтбѳ]$', colontitul_center, re.I):
    # colontitul_center = colontitul_center + 'ъ'
    # colontitul_center = colontitul_center.replace('СОДЕРЖАНИЕ ', '').replace('ПЕРВОЙ КНИГИ', 'КНИГА ПЕРВАЯ').replace('ВТОРОЙ КНИГИ', 'КНИГА ВТОРАЯ').replace('ТРЕТЬЕЙ КНИГИ', 'КНИГА ТРЕТЬЯ').replace('ЧЕТВЕРТОЙ КНИГИ', 'КНИГА ЧЕТВЕРТАЯ').replace('ПЯТОЙ КНИГИ', 'КНИГА ПЯТАЯ').replace('ШЕСТОЙ КНИГИ', 'КНИГА ШЕСТАЯ').replace('СЕДЬМОЙ КНИГИ', 'КНИГА СЕДЬМАЯ').replace('ВОСЬМОЙ КНИГИ', 'КНИГА ВОСЬМАЯ').replace('ДЕВЯТОЙ КНИГИ', 'КНИГА ДЕВЯТАЯ').replace('ДЕСЯТОЙ КНИГИ', 'КНИГА ДЕСЯТАЯ')
    # colontitul_center = 'Платона.'
    # colontitul_center = label_interpages(page_pn, 'жизнь', colontitul_center)
    # colontitul_center = label_interpages(page_pn, 'О сочинениях', colontitul_center)
    # colontitul_center = label_interpages(book_pn_int, 'Феноменологія духа.', colontitul_center)
    # colontitul_center = 'ПРЕДИСЛОВІЕ'
    # colontitul_center = colontitul_center + '.'
    # colontitul_center = label_interpages(page_pn, (subpagename + '.').upper().replace(' ВВЕДЕНИЕ (КАРПОВ).', ''), '')
    # if colontitul_center == '':  colontitul_center = 'ВВЕДЕНІЕ.'

    # colontitul_center = f'— {colontitul_center} —'

    # colontitul_center = colontitul_center.upper()

    if colontitul_center == colontitul_left == colontitul_right == '':
        return ''

    colontitul = f'{{{{колонтитул|{colontitul_left}|{colontitul_center}|{colontitul_right}}}}}'

    # на первых страницах без колонтитула
    # if first_pages_without_colontitul and page_pn == page[1]:
    # 	colontitul = ''

    return colontitul


def make_colontitul_center_only(string, pagination_style=None):
    if pagination_style is None:
        colontitul = ''
        return colontitul

    if pagination_style is False:
        string = roman.toRoman(int(string))
    colontitul = f'{{{{колонтитул||— {str(string)} —|}}}}'
    # colontitul = f'{{{{колонтитул||{string}|}}}}'
    return colontitul


def wrap_to_section_tag(text, sectionname=''):
    return f'<section begin="{sectionname}" />{text}<section end="{sectionname}" />'


def wrap_to_VARtpl(text_oldorph='', text_neworph=''):
    t = text_oldorph if text_oldorph == '' \
        else '{{ВАР\n|%s<!--\n-->|<!--\n-->%s}}' % (text_oldorph, text_neworph)
    return t


def make_pwb_page(pagename, pagetext):
    pwb_post_page = "{{-start-}}\n" \
                    "'''%s'''\n" \
                    "%s\n" \
                    "{{-stop-}}\n" % (pagename, pagetext)
    return pwb_post_page


def precorrection(text):
    text = re.sub(r'(\w+)-$', r'{{перенос|\1|}}', text, flags=re.MULTILINE)
    text = text.replace('&apos;', "'")
    text = text.replace('&nbsp;', " ")
    text = text.replace('бблып', "ббльш").replace('бблын', "ббльш") \
        .replace('бб', "бо{{акут}}")
    text = re.sub(r'([„”«»]|&quot;)', '"', text)

    return text


def perenos_slov(pages: list):
    """Расстановка шаблона {{перенос}} на страницы со словом, и {{перенос2}} на след. страницы"""
    re_perenos_start = re.compile(r'(\w+)-$')
    re_perenos_second = re.compile(r'^(\w+)')
    for i, p in enumerate(pages):
        perenos_begin_re = re_perenos_start.search(p.parsed_text)
        if perenos_begin_re:
            perenos_begin = perenos_begin_re.group(1)
            text_next_page = pages[i + 1].parsed_text
            perenos_end_re = re_perenos_second.search(text_next_page)
            perenos_end = perenos_end_re.group(1) if perenos_end_re else ''
            p.parsed_text = re_perenos_start.sub(r'{{перенос|%s|%s}}' % (perenos_begin, perenos_end), p.parsed_text)
            text_next_page = re_perenos_second.sub(r'{{перенос2|%s|%s}}' % (perenos_begin, perenos_end),
                                                   text_next_page)
            pages[i + 1].parsed_text = text_next_page


def pagenum_to_scanpagenum(pagenum, offset: int) -> int:
    scanpagenum = int(pagenum) + offset
    return scanpagenum


def scanpagenum_to_pagenum(scanpnum, offset: int) -> int:
    scanpagenum = int(scanpnum) + offset
    return scanpagenum


def calc_scanpagenum_by_bookpagenum(book_pn, range_pages_metric: list) -> dict:
    book_pn = int(book_pn)
    scan_pn = ''
    for rangemetric in range_pages_metric:
        offset, start, end = rangemetric
        if start <= book_pn <= end:
            scan_pn = book_pn + offset
            break
    return scan_pn


def calc_bookpagenum_by_scanpagenum(scan_pn, range_pages_metric: list):
    scan_pn = int(scan_pn)
    book_pn = ''
    pagination_style = None
    for rangemetric in range_pages_metric:
        offset, start, end, pagination_style = rangemetric
        if start <= scan_pn <= end:
            book_pn = scan_pn + offset
            break
    return book_pn, pagination_style
