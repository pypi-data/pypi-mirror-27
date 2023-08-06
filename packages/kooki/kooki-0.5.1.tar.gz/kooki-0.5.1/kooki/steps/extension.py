import os
from kooki.tools.output import Output

def Extension(jars, recipe):
    current = os.getcwd()
    extensions = {}
    path = os.path.join(current, 'extensions')
    if os.path.isdir(path):
        load_extensions(path, extensions)
    for jar in jars:
        path = os.path.join(jar, recipe, 'extensions')
        if os.path.isdir(path):
            load_extensions(path, extensions)
        path = os.path.join(jar, 'extensions')
        if os.path.isdir(path):
            load_extensions(path, extensions)
    return extensions


def load_extensions(directory, extensions):
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        extension_name = os.path.splitext(file_name)[0]
        if not extension_name in extensions:
            extensions[extension_name] = path
