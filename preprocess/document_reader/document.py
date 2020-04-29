import logging
from pathlib import Path
from typing import List

from .paragraph import Paragraph

logger = logging.getLogger(__name__)


class Document:

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.paragraphs: List[Paragraph] = []

        self.load()

    def __iter__(self) -> List[Paragraph]:
        for paragraph in self.paragraphs:
            yield paragraph

    def __repr__(self):
        import json
        return json.dumps({
            'file_name': self.file_name,
            'extension': self.extension,
            'paragraphs': [json.loads(p.__repr__()) for p in self.paragraphs]
        }, ensure_ascii=False, indent=2)

    def _load_pdf(self):
        from . import PDF
        self.paragraphs = PDF(self.file_name).load()

    def _load_html(self):
        from . import HTML
        self.paragraphs = HTML(self.file_name).load().paragraphs

    def _load_docx(self):
        raise NotImplementedError(f'Not yet support for .doc/.docx extensions')
        # TODO: implement docx reading

    def _load_text(self):
        raise UserWarning(f'Unknown file format or extension {self.file_name}')
        # TODO: if the extension is not recognized, try to read the file in text mode.

    @property
    def extension(self):
        return Path(self.file_name).suffix.lower()

    def load(self):
        {'.pdf': self._load_pdf,
         '.html': self._load_html,
         '.doc': self._load_docx,
         '.docx': self._load_docx
         }.get(self.extension, self._load_text)()

        return self
