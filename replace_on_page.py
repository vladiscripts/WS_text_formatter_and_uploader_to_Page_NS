#!/usr/bin/env python3
# coding: utf-8
import requests
import sqlite3
import json
from lxml.html import fromstring
import re
from roman import fromRoman
from pathlib import Path
from urllib.parse import urlencode, urlsplit, parse_qs, parse_qsl, unquote, quote
# from vladi_helpers import vladi_helpers
# from vladi_helpers.file_helpers import json_save_to_file, json_load_from_file
from scripts.get_list_pages import Get_listpages
from scripts.wiki_methods import WikiMethods
import mwparserfromhell as mwp
from copy import copy

"""викиссылки: вынос наружу названий книг Библии
python3 $PWBPATH/pwb.py replace -family:wikisource -regex  "({{Библия[^}]+т=)([А-Яа-я.\s]+)" '\2\1'  -cat:'Категория:БЭАН' -prefixindex:'БЭАН/'
"""

# re_matches = re.compile(r"\s*([IVXLC]+,\s+\d+(?:[-–\d,\s]+)?),?\s*")
# re_matches = re.compile(r"\s*([IVXLC]+,\s+\d+[^IVXLC]+)")
re_chk = re.compile(r"^\s*[IVXLC]\s*[^А-Яа-я]+")
re_matches = re.compile(r"\s*([IVXLC]+(?:,\s*\d*)?[^IVXLCА-Яа-я]*)")
re_param = re.compile(r"([IVXLC]+)(?:,\s*(\d+))?")

# tests
for s in [
    "(I Пар. {{Библия|1Пар|2:36|т=II. 36}}) сын  ",
    ' (Пс. {{Библия|Пс|90:13|т=XC, 13}}), ',
    'Нав. {{Библия|Нав|15:55|т=XV: 55, XXI, 16}}). В ',
    'Цар. {{Библия|4Цар|8:28|т=VIII, 28, 29, IX, 5, 14, 15}}), и вот',
    # 'Иуд. {{Библия|Иуд|1:11|т=I: 11}}, ',
    # ' з) ({{Библия|1Езд|10:18|т={{r|1}} Езд. {{r|10}}, 18, 21, 22}}) три',
    'Цар. {{Библия|2Цар|3:3|т=III, 3, I}} Пар',
    '(I Пар. {{Библия|1Пар|19:18|т=XIX, 18, 19, XX:I}}) – место',
    'Моисея (Исх. {{Библия|Исх|24:14|т=XXIV. 14}}).',
    'мира (Быт. {{Библия|Быт|7:4|-10|т=VII, 4–10, VIII, 10–12}}), и ',
    'Пс. {{Библия|Пс|118:176|т=CXVIII, 176}}; Ис. {{Библия|Ис|11:6|т=XI, 6, III, 6, 7}},  Мих.',
    '(IV Цар. {{Библия|4Цар|8:28|т=VIII, 28, 29, IX, 5, 14, 15}}), и',
    ' Ин. {{Библия|1Ин|3:12|т=III, 12}}; Иуд. {{Библия|Иуд|1:11|т=I: 11}},  Евр. {{Библия|Евр|11:4|т=XI, 4}}) ',
    ' (Числ. {{Библия|Чис|22|-24|т=XXII-XXIV}},  Нав. {{Библия|Нав|24:9|т=XXIV, 9}}; ',
    ' (Нав. {{Библия|Нав|15:55|т=XV: 55, XXI, 16}}). ',
    'б) ({{Библия|1Пар|4:7|т=I Пар. IV, 7}}) из',
    # '(Еф. {{Библия|Еф|4|-6|т=IV-VI}}).',
    # 'гл. {{Библия|Быт|16:7|т={{опечатка|XXVI|XVI|О1|nocat=}}, 7}}), замечает ',
]:
    # matches = re.findall(r"т=\s*([IVXLC]+,\s+\d+(?:[-–\d,\s]+)?),?\s*", s)
    # assert matches
    # assert len(matches) > 1
    print()

w = WikiMethods()
lp = Get_listpages(w.SITE)
lp.get_pagelists(path='/tmp/list.txt')
titles = lp.pagelists_titles
# titles = ['БЭАН/Елеазар']

for title in titles:
    page_data = w.open_page(title)
    # text = page_data.obj.text
    # text = "'''Блюда, чаши, кружки''' и пр. (глубокая чаша, сосуды с плоским дном и невысокими краями) (Исх. {{Библия|Исх|25:29|т=XXV, 29, XXXVII, 16}}, IV Цар. {{Библия|4Цар|21:13|т=XXI, 13}}, I Ездр. {{Библия|1Ездр|1:9|т=I, 9}}, Числ. {{Библия|Чис|7:13|т=VII, 13}}, Мф. {{Библия|Мф|26:23|т=XXVI, 23}}) "
    # text = "(I Пар. {{Библия|1Пар|2:36|т=II. 36}}) сын  "
    # text = ''.join([
    #     'Цар. {{Библия|2Цар|3:3|т=III, 3, I, 4, II, V}} Пар',
    #     "(I Пар. {{Библия|1Пар|2:36|т=II. 36}}) сын  ",
    #     ' (Пс. {{Библия|Пс|90:13|т=XC, 13}}), ',
    #     'Нав. {{Библия|Нав|15:55|т=XV: 55, XXI, 16}}). В ',
    #     'Цар. {{Библия|4Цар|8:28|т=VIII, 28, 29, IX, 5, 14, 15}}), и вот',
    #     # 'Иуд. {{Библия|Иуд|1:11|т=I: 11}}, ',
    #     # ' з) ({{Библия|1Езд|10:18|т={{r|1}} Езд. {{r|10}}, 18, 21, 22}}) три',
    #     'Цар. {{Библия|2Цар|3:3|т=III, 3, I}} Пар',
    #     '(I Пар. {{Библия|1Пар|19:18|т=XIX, 18, 19, XX:I}}) – место',
    #     'Моисея (Исх. {{Библия|Исх|24:14|т=XXIV. 14}}).',
    #     'мира (Быт. {{Библия|Быт|7:4|-10|т=VII, 4–10, VIII, 10–12}}), и ',
    #     'Пс. {{Библия|Пс|118:176|т=CXVIII, 176}}; Ис. {{Библия|Ис|11:6|т=XI, 6, III, 6, 7}},  Мих.',
    #     '(IV Цар. {{Библия|4Цар|8:28|т=VIII, 28, 29, IX, 5, 14, 15}}), и',
    #     ' Ин. {{Библия|1Ин|3:12|т=III, 12}}; Иуд. {{Библия|Иуд|1:11|т=I: 11}},  Евр. {{Библия|Евр|11:4|т=XI, 4}}) ',
    #     ' (Числ. {{Библия|Чис|22|-24|т=XXII-XXIV}},  Нав. {{Библия|Нав|24:9|т=XXIV, 9}}; ',
    #     ' (Нав. {{Библия|Нав|15:55|т=XV: 55, XXI, 16}}). ',
    #     'б) ({{Библия|1Пар|4:7|т=I Пар. IV, 7}}) из',
    #     # '(Еф. {{Библия|Еф|4|-6|т=IV-VI}}).',
    #     # 'гл. {{Библия|Быт|16:7|т={{опечатка|XXVI|XVI|О1|nocat=}}, 7}}), замечает ',
    # ])
    # page_data.wikicode = mwp.parse(text)
    for p in page_data.wikicode.filter_templates():
        if not p.name.matches('библия'): continue
        tparam = str(p.get('т').value)
        if not re_chk.search(tparam): continue

        # matches = re.findall(r"([IVXLC]+,\s+(?:[-–\d,\s]+)?),?\s*", tparam)
        # matches = re.findall(r"\s*([IVXLC]+,\s+\d+?[^IVXLCА-Яа-я]+)", tparam)
        # matches = re.findall(r"\s*([IVXLC]+(?:,\s*\d*)?[^IVXLCА-Яа-я]*)", tparam)
        matches = re_matches.findall(tparam)
        if len(matches) > 1:
            # print(matches)
            # p.get('т').value = matches[0]
            i = page_data.wikicode.index(p)
            book = str(p.get(1).value)
            # c = copy(p)
            # n = matches[1]
            pp = []
            # pp.append(str(p))
            # for e in sorted(matches, reverse=False):
            for e in matches:
                # b = re.search(r"([IVXLC]+),\s*(\d+)?", e.strip(' ,'))  # r"([IVXL]+),\s*(\d+)?([-–\d,\s]+)?"
                b = re_param.search(e.strip(' ,'))  # r"([IVXL]+),\s*(\d+)?([-–\d,\s]+)?"
                if b:
                    b1, b2 = b.group(1), b.group(2)
                    t = mwp.parse('{{Библия}}').nodes[0]
                    t.add(1, book)
                    part = fromRoman(b1)
                    stih = f':{b2}' if b2 else ''
                    t.add(2, f'{part}{stih}')
                    # if b2:
                    #     t.add(3, b2)
                    # t.add('т', b.group(0))
                    # stih2 = f',\xa0{b2}' if b2 else ''
                    # t.add('т', f"{b1}{stih2}")
                    t.add('т', e.strip(' \xa0,'))
                    pp.append(str(t))
                    # wikicode.insert_after(p, t)
            bb = ',\xa0'.join(pp)
            page_data.wikicode.replace(p, bb)
            # print(bb)
            # print(str(wikicode))

    pass
    # разделение сдвоенных ссылок {{библия}}.
    # надо применить модуль roman для конвертации вики-ссылок на стихи
    # for i in range(5):
    #     text = re.sub(
    #         r"({{Библия[^}]+т=)"
    #         r"((?:[IVXL]+\s+(?:[А-Яа-я., ]+)?)?\s*[IVXL,\s]+(?:[\d–]+)?)"
    #         r"(,\s*)"
    #         r"([IVXL,\s]+(?:[\d–]+\s*)?.*?)"
    #         r"(}})",
    #         lambda m: f'{m.group(1)}{m.group(2)}{m.group(5)}{m.group(3)}{m.group(1)}{m.group(4)}{m.group(5)}',
    #         # r'\1\2\5\3\1\4\5',
    #         text
    #     )

    pass
    text_new = str(page_data.wikicode)
    w.wiki_posting_page(page_data.obj, text_new, '{{библия}}: разделение спаренных викиссылок')
