from kooki.kooki import ContentKooki
from kooki.tools.output import Output
from kooki import DocumentException

def Merge(parts):
    Output.start_step('merge')
    result = ''
    for part in parts:
        result += part
    return result
