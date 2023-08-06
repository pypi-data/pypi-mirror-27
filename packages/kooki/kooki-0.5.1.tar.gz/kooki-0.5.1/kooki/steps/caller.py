from kooki.tools import get_front_matter, DictAsMember
import em

def Caller(file_full_path, metadata={}):
    def call(*args, **kwargs):
        with open(file_full_path,'r') as f:
            file_content = f.read()
            interpreter = em.Interpreter()
            interpreter.setPrefix('@')
            front_matter, new_content = get_front_matter(file_content)
            metadata_copy = metadata.copy()
            metadata_copy.update(front_matter)
            metadata_copy.update({**kwargs})
            new_metadata = DictAsMember.convert(metadata_copy)
            try:
                ret_content = interpreter.expand(new_content, new_metadata)
            except:
                ret_content = new_content
            return ret_content
    return call
