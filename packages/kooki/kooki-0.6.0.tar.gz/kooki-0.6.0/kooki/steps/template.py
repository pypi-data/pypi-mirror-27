import em
from kooki.tools import DictAsMember

def Template(data, metadata):
    interpreter = em.Interpreter()
    interpreter.setPrefix('@')
    metadata_member = DictAsMember.convert(metadata)

    if type(data) == list:
        result = []
        for d in data:
            result.append(interpreter.expand(d, metadata_member))
    else:
        result = interpreter.expand(data, metadata_member)

    return result
