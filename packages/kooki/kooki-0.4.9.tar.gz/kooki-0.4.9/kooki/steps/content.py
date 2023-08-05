from kooki.kooki import Kooki
from kooki.tools.output import Output
from kooki import DocumentException

from . import Step

def Content(config, files, utensils):
    step = _Content(config, utensils)
    return step(files)


class _Content(Step):

    def __init__(self, config, utensils):
        super().__init__(config)
        self._infos = []
        self.utensils = utensils

    def __call__(self, files):

        content = ''
        error = False

        Output.start_step('contents')

        for source in files:
            try:
                kooki = self._load(source)
                kooki_cooked = kooki.cook()
                content += kooki_cooked['content']
                self._infos.append({'name': source, 'status': '[found]', 'info': ''})

            except DocumentException as e:
                self._infos.append({'name': source, 'status': ('[error]', 'red'), 'info': (str(e), 'red')})
                error = True

            except NameError as e:
                self._infos.append({'name': source, 'status': ('[error]', 'red'), 'info': (str(e), 'red')})
                error = True

            except Exception as e:
                # self._infos.append({'name': source, 'status': ('[missing]', 'red')})
                raise Exception(type(e))

        if len(files) > 0:
            Output.infos(self._infos, [('name', 'cyan'), ('status', 'green'), ('info', 'cyan')])
        else:
            Output.info('no content')

        if error:
            raise DocumentException('Something went wrong... :(')

        return content

    def _load(self, content_source):

        kooki = Kooki(content_source)

        for utensil in self.utensils:
            kooki.add_utensil(utensil)

        return kooki
