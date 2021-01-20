from abc import abstractmethod
from pywikibot import xmlreader


class WorkWikiDump:

    def __init__(self, xml_path, function_to_proc_entry):
        self.xml_path = xml_path
        self.proceess_entry = function_to_proc_entry

    def work_pages(self):
        dump = xmlreader.XmlDump(self.xml_path)
        for entry in dump.parse():
            self.proceess_entry(entry)

    @abstractmethod
    def proceess_entry(self, entry):
        """Это место для замещения внешней функцией для обработки entry страницы."""
        pass


# Пример:
"""
def proceess_entry(entry):
    if int(entry.ns) not in [0] \
            or not entry.title.startswith('БЭАН/'):
        return
    if entry.isredirect:
        print(f'{entry.title}: {entry.isredirect=}')

    # if 'РСКД/Цезарь' in entry.title:
    #     print(entry.title)
    # all_found_titles.append(entry.title)

    # links = []
    # links.extend(wikilink_re1.findall(entry.text))
    return entry
"""