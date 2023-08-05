import em
from kooki.tools import DictAsMember

def DocumentName(document, metadata):
    interpreter = em.Interpreter()
    interpreter.setPrefix('@')
    metadata_member = DictAsMember.convert(metadata)
    name = interpreter.expand(document.name, metadata_member)
    return name
