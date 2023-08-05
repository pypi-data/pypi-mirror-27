import em
from kooki.tools import DictAsMember

def Template(text, metadata):
    interpreter = em.Interpreter()
    interpreter.setPrefix('@')
    metadata_member = DictAsMember.convert(metadata)
    result = interpreter.expand(text, metadata_member)
    return result
