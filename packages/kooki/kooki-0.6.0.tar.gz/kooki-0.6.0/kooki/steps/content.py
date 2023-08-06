from kooki.tools import get_front_matter, DictAsMember
import em

def Content(content, metadata):
    interpreter = em.Interpreter()
    interpreter.setPrefix('@')
    ret_content = ''
    for file_path, file_content in content.items():
        front_matter, new_content = get_front_matter(file_content)
        metadata_copy = front_matter.copy()
        metadata_copy.update(metadata)
        metadata = DictAsMember.convert(metadata_copy)
        ret_content += interpreter.expand(new_content, metadata)
    return ret_content
