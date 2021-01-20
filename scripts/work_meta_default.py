import pathlib
import operator
from scripts.page_work_class import Parse_to_wiki, Pagedata
from scripts.format_text_to_wiki_indexpage import \
    formatting_output_page, perenos_slov, make_pwb_page
from vladi_helpers.file_helpers import file_readtext, filepaths_of_directory, file_savetext, csv_read,csv_read_to_dict


class WorkMeta_default:
    to_NSpages = False
    directory = ''
    input_csv = ''  # if to_NSpages
    filepaths_output_pwb = '/tmp/topost.txt'
    workpagename = ''
    range_pages_metric = [
        # диапазоны страниц скана.
        # В диапазоне "[-5, 7, 123, False]":
        # offset (смещение между номером страниц скана и с.книги), start, end, pagination_style (True - араб.цифры, False - римские, None - без нумерации)
        [0, 0, 0, None],
    ]
    from_scanpagenum = 0  # делать страницы начиная с этой
    parse_from = 'htm'  # 'fb2', 'htm', 'txt'
    wrap_to_VARtpl = True
    deyatification = True
    colontitul_on_top = True
    colontitul_center_only = True
    # закоментировать для откл.колонтитула
    # Колонтитул настраивается в format_text_to_wiki_indexpage: make_colontitul() и в make_colontitul_center_only()
    make_colontitul = dict(enable=False, on_top=True, center_only=True)
    do_precorrection = True
    # do_perenos_words = True
    pages = []

    def __init__(self):
        if self.to_NSpages:
            self.fext = f'*.{self.parse_from}'
            p = pathlib.Path(self.directory)
            self.filepaths = p.glob(self.fext)

    def files_to_list(self):
        # pages = [Pagedata(cls_parse_to_wiki, fp, m.workpagename, parse_from=m.parse_from) for fp in filepaths]
        # pages = [p for p in pages if p.scanpagenum >= m.from_scanpagenum]        
        for fp in self.filepaths:
            p = Pagedata(self, filepath=fp)
            if p.scanpagenum >= self.from_scanpagenum:
                self.pages.append(p)
        self.pages.sort(key=operator.attrgetter('scanpagenum'))

    def csv_to_list(self, text_field_name='content'):
        # pages = [Pagedata(cls_parse_to_wiki, fp, m.workpagename, parse_from=m.parse_from) for fp in filepaths]
        # pages = [p for p in pages if p.scanpagenum >= m.from_scanpagenum]
        data = csv_read_to_dict(self.input_csv)
        for b in data:
            p = Pagedata(self, text=b[text_field_name])
            if self.to_NSpages:
                if p.scanpagenum >= self.from_scanpagenum:
                    self.pages.append(p)
            else:
                self.pages.append(p)
        self.pages.sort(key=operator.attrgetter('scanpagenum'))

    def format_pages_to_NSpage(self):
        """форматировать страницы для ПИ Страница"""
        for page in self.pages:
            page.posttext = formatting_output_page(
                page, self.range_pages_metric,
                do_precorrection=self.do_precorrection,
                colontitul=self.make_colontitul,
                deyatification=self.deyatification,
                VARtpl_wrap=self.wrap_to_VARtpl)

    def make_pwb_file(self):
        """форматировать файл для pwb"""
        topost = [make_pwb_page(p.pagename, p.posttext) for p in self.pages]
        topostall = '\n'.join(topost)
        pathlib.Path(self.filepaths_output_pwb).write_text(topostall)

    def perenos_slov(self):
        """расстановка шаблона {{перенос}} на страницы со словом, и {{перенос2}} на след. страницы"""
        # if self.do_perenos_words:
        perenos_slov(self.pages)
