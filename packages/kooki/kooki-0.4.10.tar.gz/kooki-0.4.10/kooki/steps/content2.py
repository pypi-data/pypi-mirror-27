from kooki.kooki import ContentKooki
from kooki.tools.output import Output
from kooki import DocumentException

def Content(contents, utensils):
    Output.start_step('contents')
    result = []
    infos = []

    for content in contents:
        kooki = ContentKooki(content)
        for utensil in utensils:
            kooki.add_utensil(utensil)
        kooki_cooked = kooki.cook()
        result.append(kooki_cooked['content'])

    return result
