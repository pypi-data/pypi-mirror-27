from kooki.kooki import ContentKooki
from kooki.tools.output import Output
from kooki import DocumentException

def Custom(parts, merger):
    Output.start_step('custom')
    result = []
    for index, part in enumerate(parts):
        result.append(merger(part, index))
    return result
