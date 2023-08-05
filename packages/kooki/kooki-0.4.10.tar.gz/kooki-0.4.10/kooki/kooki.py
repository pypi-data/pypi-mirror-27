from kooki.tools import get_extension, read_file, write_file
from kooki.document_exception import DocumentException

import yaml

class Kooki():
    def __init__(self, source):

        try:
            self._content = read_file(source)
            self._extension = get_extension(source)
            self.utensils = []

        except FileNotFoundError as e:
            raise DocumentException('No such file: {0}'.format(source))

    def __call__(self, **kwargs):
        result = self.cook(**{'metadata': kwargs})
        return result['content']

    def cook(self, **kwargs):

        result = {'content': self._content}
        result.update(kwargs)

        for utensil in self.utensils:
            utensil_result = utensil(**result)
            result.update(utensil_result)

        return result

    def content(self):
        return self._content

    def extension(self):
        return self._extension

    def add_utensil(self, utensil):
        self.utensils.append(utensil)

    def remove_utensil(self):
        self.utensils.pop()


class ContentKooki(Kooki):

    def __init__(self, content):
        self._content = content
        self.utensils = []
