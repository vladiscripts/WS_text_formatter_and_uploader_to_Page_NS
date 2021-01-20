import re
# from .format_text_to_wiki_indexpage import scan_page_name
from vladi_helpers.file_helpers import file_readtext, filepaths_of_directory, file_savetext
from scripts import Parse_to_wiki


class Pagedata:

    # def __init__(self, filepath, workpagename, bookvolume_num='', parse_from=None):
    def __init__(self, workmeta, filepath=None, text=None, bookvolume_num=''):
        if filepath:
            self.filepath = filepath
            # self.filename = filepath.split('/')[-1]
            self.filename = filepath.name
            scanpagenum = re.search(r'(\d+)\.\w*$', filepath.name)
            self.scanpagenum = int(scanpagenum.group(1)) if scanpagenum else None
            # if scanpagenum:
            #     pn = int(scanpagenum.group(1))
            #     pn += 1
            #     if pn >= 6:
            #         pn -= 1
            #     if pn >= 7:
            #         pn -= 1
            #     self.scanpagenum = pn
            # else:
            #     scanpagenum = None
            self.pagename = scan_page_name(workmeta.workpagename, self.scanpagenum, volume_num=bookvolume_num)
            self.text_source = file_readtext(filepath)
        elif text:
            self.text_source = text
        parse_to_wiki = Parse_to_wiki()
        self.parsed_text = parse_to_wiki.dispatcher(self.text_source, workmeta.parse_from)
        self.posttext = ''


def scan_page_name(workpagename: str, scan_pn, volume_num=None):
    pagename = f'Страница:{workpagename}/{str(scan_pn)}'
    if '%s' in workpagename:
        pagename = pagename % volume_num
    return pagename
