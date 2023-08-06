from kooki.jars import search_file
from kooki.tools import Output, get_front_matter, DictAsMember
import em

def Reader(document, metadata={}):
    def read(file_path):
        file_full_path = search_file(document.jars, document.recipe, file_path)
        ret_content = ''

        output = []
        if file_full_path:
            output.append({'name': file_path, 'status': '[found]', 'path': file_full_path})

            with open(file_full_path,'r') as f:
                file_content = f.read()
                interpreter = em.Interpreter()
                interpreter.setPrefix('@')
                front_matter, new_content = get_front_matter(file_content)
                metadata_copy = metadata.copy()
                metadata_copy.update(front_matter)
                new_metadata = DictAsMember.convert(metadata_copy)
                try:
                    ret_content = interpreter.expand(new_content, new_metadata)
                except:
                    ret_content = new_content
        else:
            output.append({'name': file_path, 'status': ('[missing]', 'red'), 'path': ''})

        Output.infos(output, [('name', 'blue'), ('status', 'green'), ('path', 'cyan')])

        return ret_content

    return read
