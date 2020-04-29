import logging
from pathlib import Path

from preprocess.document_structuring.node import RootNode
from preprocess.document_structuring.node.node import Node

logger = logging.getLogger(__name__)


class ParsingManager:
    def __init__(self):
        """ To manage parsers.
        All the parser will be run by the order of registration until one of them is passed.
        """
        self._parsers = []

    @property
    def parsers(self):
        return self._parsers

    def register_parser(self, parser):
        """ Register a parser to be run while parsing the document.
        :rtype: None
        """
        self.parsers.append(parser)

    def register_parsers(self, parsers: tuple):
        self.parsers.extend(parsers)

    def run(self, document):
        logger.info(f'Structuring "{Path(document.file_name).name}"')
        root = RootNode(document.file_name)

        index = 0
        current_node = root
        for paragraph in document:
            node = Node(paragraph)
            index += 1
            for parser in self.parsers:
                try:
                    if parser.run(current_node, node):
                        current_node = node
                        break
                except BaseException as e:
                    logger.exception(f'Exception happens while parsing.\n{e}')
        else:
            return root
