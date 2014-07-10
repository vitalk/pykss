import os

from pykss.comment import CommentParser
from pykss.exceptions import SectionDoesNotExist
from pykss.loaders import FileSystemLoader
from pykss.section import Section


class Parser(object):

    def __init__(self, *paths):
        self.loader = FileSystemLoader(paths)

    def parse(self):
        sections = {}

        for filename in self.loader.list_files():
            parser = CommentParser(filename)
            for block in parser.blocks:
                section = Section(block, os.path.basename(filename))
                if section.section:
                    sections[section.section] = section

        return sections

    @property
    def sections(self):
        if not hasattr(self, '_sections'):
            self._sections = self.parse()
        return self._sections

    def section(self, reference):
        try:
            return self.sections[reference]
        except KeyError:
            raise SectionDoesNotExist('Section "%s" does not exist.' % reference)
