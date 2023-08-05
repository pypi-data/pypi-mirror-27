from kooki.kooki import ContentKooki
from kooki.tools.output import Output
from kooki import DocumentException
from kooki.tools import read_file
from kooki.utensils import MarkdownToHTML, HTMLToTeX, Empy, FrontMatter
from xml.dom import minidom

from . import Step

def Slides(config, files, metadata):
    step = _Slides(config)
    return step(files, metadata)


class _Slides(Step):

    def __init__(self, config):
        self._infos = []
        self._name = 'contents'

    def __call__(self, files, metadata):

        content = ''
        missing = False

        Output.start_step(self._name)

        slide_number = 1

        for source in files:
            try:
                kookis = self._load(source, metadata)

                for kooki in kookis:
                    kooki_cooked = kooki.cook()

                    classes = ''
                    html_id = ''
                    others = ''
                    slide_content = kooki_cooked['content']

                    if kooki_cooked['content'].startswith('<p>{:'):
                        end = kooki_cooked['content'].find('}</p>')
                        attrs = kooki_cooked['content'][5:end].split()
                        slide_content = kooki_cooked['content'][end + 5:]

                        for attr in attrs:

                            if attr.startswith('.'):
                                classes += attr[1:]

                            elif attr.startswith('#'):
                                html_id = attr[1:]

                            else:
                                others += attr

                    content += '<section id="{0}" class="slide slide-{3} {1}" {2}>'.format(html_id, classes, others, slide_number)
                    content += '<div class="slide-number">{0}</div>'.format(slide_number)
                    content +=  '<div class="slide-content"><div class="slide-content-child">'
                    content += slide_content
                    content += '</div></div></section>'

                    slide_number += 1

                self._infos.append({'name': source, 'status': '[found]'})

            except Exception as e:
                print(e)
                self._infos.append({'name': source, 'status': ('[missing]', 'red')})
                missing = True

        if len(files) > 0:
            Output.infos(self._infos, [('name', 'cyan'), ('status', 'green')])
        else:
            Output.info('no content')

        if missing:
            raise DocumentException('Missing files ou sources')

        return content

    def _load(self, content_source, metadata):

        template = Empy(metadata)
        html = MarkdownToHTML()

        content = read_file(content_source)

        splitted = content.split('---\n')

        kookis = []

        for part in splitted:

            kooki = ContentKooki(part)
            kooki.add_utensil(template)
            kooki.add_utensil(html)

            kookis.append(kooki)

        return kookis
