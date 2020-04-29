class Bullet:
    patterns = '➢･・●※◆•‣-⁃⁌⁍∙○◘◦⦾⦿􀂾◇'

    def __init__(self, text='', indentation=0):
        self.char = None
        self.indentation = indentation

        self._parse(text)

    def __eq__(self, other):
        return self.char == other.char and self.indentation == other.indentation

    def __str__(self):
        return self.text

    def __repr__(self):
        import json
        return json.dumps({
            'text': self.text,
            'indentation': self.indentation
        }, ensure_ascii=False, indent=2)

    @property
    def text(self):
        return self.char if self.char is not None else ''

    def _parse(self, text):
        try:
            if text.startswith('(cid:190)'):
                text = text.replace('(cid:190)', '􀂾', 1)

            if len(text) >= 1 and text[0] in Bullet.patterns:
                self.char = text[0]
        except ...:
            pass

    def is_empty(self):
        return self.char is None
