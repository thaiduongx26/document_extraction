import json

from ...document_reader import Paragraph


class Node:
    def __init__(self, paragraph: Paragraph = None):
        ''' A node of bidirectional tree, representing a document structure.
        :param text_block:
        :param index:
        '''
        self.parent: Node = None
        self.is_document_title = False
        self.children = []

        self.paragraph = paragraph
        self.parser_name = ''

    def __repr__(self):
        return json.dumps({
            'text': self.paragraph.text,
            'page': self.paragraph.page_number,
            'parser': self.parser_name,
            'index': self.paragraph.index,
            'parent_index': self.parent_index,
            'is_title': self.paragraph.is_title(),
            'is_table': self.paragraph.is_table(),
            'indentation': str(self.paragraph.indentation),
            'children': [json.loads(child.__repr__()) for child in self.children]
        }, ensure_ascii=False, indent=2)

    @property
    def parent_index(self):
        parent_index = None
        if not self.parent.is_root():
            parent_index = self.parent.paragraph.index
        return parent_index

    def is_root(self):
        return self.parent is None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def level(self):
        lev = 0
        node = self
        while node.parent is not None:
            node = node.parent
            lev += 1
        else:
            return lev

    def ancestor(self, level):
        node = self
        while node.level() > level:
            node = node.parent
        else:
            return node

    def root(self):
        return self.ancestor(0)

    def find_up(self, comparer):
        if self.is_root():
            return self

        if comparer(self):
            return self

        return self.parent.find_up(comparer)

    def can_has_child(self):
        return self.is_root() \
               or self.paragraph.is_title() \
               or self.paragraph.has_numbering() \
               or self.paragraph.has_bullet() \
               or self.is_document_title
