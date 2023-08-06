import yaml, os, argparse
import pretty_output

from kooki.config import read_config_file, get_kooki_dir_jars, get_kooki_dir_recipes
from kooki.tools import write_file, read_file
from kooki.jars import get_jars
from kooki.rule_parser import parse_document_rules

from .command import Command

__command__ = 'freeze'
__description__ = 'Freeze version of Kooki and Jars'


class FreezeCommand(Command):

    def __init__(self):
        super(FreezeCommand, self).__init__(__command__, __description__)
        self.add_argument('documents', nargs='*')
        self.add_argument('-f', '--config-file', default='kooki.yaml')

    def callback(self, args):
        config = read_config_file(args.config_file)
        document_rules = parse_document_rules(config)
        version = freeze_kooki()
        jars = freeze_jars(document_rules)
        recipes = freeze_recipes(document_rules)

        repositories = {
            'kooki': version,
            'repositories': jars}

        write_file('.kooki_freeze', yaml.safe_dump(repositories, default_flow_style=False))


def freeze_kooki():
    from kooki.version import __version__
    pretty_output.start_step('kooki')
    pretty_output._print_colored('version ', 'blue', end='')
    pretty_output._print_colored(__version__, 'cyan')
    return __version__


def freeze_jars(documents):
    from vcstool.commands.export import ExportCommand
    from vcstool.crawler import find_repositories
    from vcstool.executor import execute_jobs, generate_jobs

    pretty_output.start_step('jars')

    infos = []
    jars = set()
    export_jars = {}

    user_jars_dir = get_kooki_dir_jars()

    for name, document in documents.items():
        for jar in document.jars:
            jars.add(jar)

    for jar in jars:
        jar_path = os.path.join(user_jars_dir, jar)

        pretty_output._print_colored(jar, 'blue', end='')
        pretty_output._print_colored(' [found] ', 'green', end='')
        pretty_output._print_colored(jar_path, 'cyan')

        if os.path.isdir(jar_path):
            export_args = argparse.Namespace()
            export_args.path = jar_path
            export_args.exact = True
            command = ExportCommand(export_args)
            clients = find_repositories([jar_path])
            jobs = generate_jobs(clients, command)
            results = execute_jobs(jobs)

            pretty_output._print_colored('  vcs: ', 'yellow', end='')
            if results == []:
                pretty_output._print_colored('no vcs set', 'red')
            elif len(results) == 1:
                result = results[0]
                export_data = result['export_data']
                vcs_type = result['client'].__class__.type
                vcs_url = export_data['url']
                vcs_version = export_data['version']

                pretty_output._print_colored(vcs_type, 'cyan')
                pretty_output._print_colored('  url: ', 'yellow', end='')
                pretty_output._print_colored(vcs_url, 'cyan')
                pretty_output._print_colored('  version: ', 'yellow', end='')
                pretty_output._print_colored(vcs_version, 'cyan')

                save_jar = {}
                save_jar['type'] = vcs_type
                save_jar['url'] = vcs_url
                save_jar['version'] = vcs_version
                export_jars[jar] = save_jar

        else:
            pretty_output._print_colored('[missing]', 'red')

    return export_jars

def freeze_recipes(documents):
    from vcstool.commands.export import ExportCommand
    from vcstool.crawler import find_repositories
    from vcstool.executor import execute_jobs, generate_jobs

    pretty_output.start_step('recipes')

    recipes = set()
    export_recipes = {}

    user_recipes_dir = get_kooki_dir_recipes()

    for name, document in documents.items():
        recipes.add(document.recipe)

    for recipe in recipes:
        recipe_path = os.path.join(user_recipes_dir, recipe)

        pretty_output._print_colored(recipe, 'blue', end='')
        pretty_output._print_colored(' [found] ', 'green', end='')
        pretty_output._print_colored(recipe_path, 'cyan')

        if os.path.isdir(recipe_path):
            export_args = argparse.Namespace()
            export_args.path = recipe_path
            export_args.exact = True
            command = ExportCommand(export_args)
            clients = find_repositories([recipe_path])
            jobs = generate_jobs(clients, command)
            results = execute_jobs(jobs)

            pretty_output._print_colored('  vcs: ', 'yellow', end='')
            if results == []:
                pretty_output._print_colored('no vcs set', 'red')
            elif len(results) == 1:
                result = results[0]
                export_data = result['export_data']
                vcs_type = result['client'].__class__.type
                vcs_url = export_data['url']
                vcs_version = export_data['version']

                pretty_output._print_colored(vcs_type, 'cyan')
                pretty_output._print_colored('  url: ', 'yellow', end='')
                pretty_output._print_colored(vcs_url, 'cyan')
                pretty_output._print_colored('  version: ', 'yellow', end='')
                pretty_output._print_colored(vcs_version, 'cyan')

                export_recipe = {}
                export_recipe['type'] = vcs_type
                export_recipe['url'] = vcs_url
                export_recipe['version'] = vcs_version
                export_recipes[recipe] = export_recipe

        else:
            pretty_output._print_colored('[missing]', 'red')

    return export_recipes
