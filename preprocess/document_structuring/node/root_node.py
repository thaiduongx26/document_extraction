import json
import os

from .node import Node


class RootNode(Node):
    CONTRACT = 'contract'
    CONSORTIUM = 'consortium'

    def __init__(self, filename):
        super().__init__()
        self._filename = os.path.basename(filename)
        self._type = self.CONTRACT if os.path.dirname(filename).lower().endswith(
            self.CONTRACT) else self.CONSORTIUM

    def __repr__(self):
        return json.dumps({
            'filename': self.filename,
            'type': self.type,
            'children': [json.loads(child.__repr__()) for child in self.children]
        }, ensure_ascii=False, indent=2)

    @property
    def filename(self):
        return self._filename

    @property
    def type(self):
        return self._type
