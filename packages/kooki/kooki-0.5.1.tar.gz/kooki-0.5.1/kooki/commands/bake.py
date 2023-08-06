from .command import Command
from kooki.jars import search_file, search_recipe, search_jar
from kooki.config import parse_args
from kooki.tools import DictAsMember, Output
from kooki.steps import Content, Metadata, Template, Reader, Extension, Caller, Export

import argparse

__command__ = 'bake'
__description__ = 'Bake a kooki'

output = []

def output_search_start():
    global output
    output = []


def output_search(path, fullpath):
    if fullpath:
        output.append({'name': path, 'status': '[found]', 'path': fullpath})
    else:
        output.append({'name': path, 'status': ('[missing]', 'red'), 'path': ''})


def output_search_finish():
    Output.infos(output, [('name', 'blue'), ('status', 'green'), ('path', 'cyan')])


class BakeCommand(Command):

    def __init__(self):
        super(BakeCommand, self).__init__(__command__, __description__)
        self.add_argument('documents', nargs='*')
        self.add_argument('--config-file', default='kooki.yaml')
        self.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
        self.add_argument('-v', '--verbose', help='Show more information about the bake processing.', action='store_true')

    def callback(self, args):
        documents = parse_args(args)

        for name, document in documents.items():
            recipe = document.recipe
            jars = document.jars

            Output.start_document(name)

            # jars
            Output.start_step('jars')
            output_search_start()
            full_path_jars = []
            for jar in document.jars:
                jar_full_path = search_jar(jar)
                output_search(jar, jar_full_path)
                full_path_jars.append(jar_full_path)
            document['jars'] = full_path_jars
            output_search_finish()

            # extensions
            Output.start_step('extensions')
            output_search_start()
            extensions = Extension(document.jars, document.recipe)
            new_extensions = {}
            for extension_name, extension_path in extensions.items():
                new_extensions[extension_name] = Caller(extension_path)
                output_search(extension_name, extension_path)
            output_search_finish()

            # template
            Output.start_step('template')
            output_search_start()
            file_full_path = search_file(jars, recipe, document.template)
            output_search(document.template, file_full_path)
            if file_full_path:
                with open(file_full_path,'r') as f:
                    file_read = f.read()
                document['template'] = file_read
            output_search_finish()

            # metadata
            Output.start_step('metadata')
            metadata_full_path = {}
            output_search_start()
            for metadata in document.metadata:
                file_full_path = search_file(jars, recipe, metadata)
                with open(file_full_path,'r') as f:
                    file_read = f.read()
                metadata_full_path[file_full_path] = file_read
                output_search(metadata, file_full_path)
            document['metadata'] = metadata_full_path
            output_search_finish()

            # content
            Output.start_step('content')
            content_full_path = {}
            output_search_start()
            for content in document.content:
                file_full_path = search_file(jars, recipe, content)
                with open(file_full_path,'r') as f:
                    file_read = f.read()
                content_full_path[file_full_path] = file_read
                output_search(content, file_full_path)
            document['content'] = content_full_path
            output_search_finish()

            Output.start_step('recipe')
            output_search_start()
            file_full_path = search_recipe(recipe)
            output_search(document.recipe, file_full_path)
            output_search_finish()

            if file_full_path:
                with open(file_full_path,'r') as f:
                    recipe_read = f.read()
                    variables = {}
                    exec(recipe_read, variables)
                    if 'recipe' in variables:
                        recipe = variables['recipe']
                    recipe(document, new_extensions)
            else:
                raise(Exception('bad recipe'))
