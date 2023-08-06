import yaml
from kooki.tools import read_file
from kooki.jars import get_jars
from .command import Command

from vcstool.commands.import_ import generate_jobs as import_generate_jobs
from vcstool.commands.import_ import add_dependencies as import_add_dependencies
from vcstool.commands.import_ import get_repositories as import_get_repositories

__command__ = 'update'
__description__ = 'Update a kooki project'


class UpdateCommand(Command):

    def __init__(self):
        super(UpdateCommand, self).__init__(__command__, __description__)

    def callback(self, args):
        freeze_file = read_file('.kooki_freeze')
        freeze_data = yaml.safe_load(freeze_file)
        apply_kooki_freeze(freeze_data, freeze_file)


def apply_kooki_freeze(freeze_data, freeze_file):
    jars = get_jars()
    Output.start_step('jars')
    for jar in freeze_data['repositories']:
        version_freezed = freeze_data['repositories'][jar]['version']
        Output._print_colored(jar, 'blue')
        Output._print_colored('  freezed: ', 'yellow', end='')
        Output._print_colored(version_freezed, 'cyan')
        Output._print_colored('  installed: ', 'yellow', end='')
        if jar in jars:
            version_installed = jars[jar]['version']
            if version_freezed == version_installed:
                Output._print_colored(version_installed, 'green')
            else:
                Output._print_colored('Installing new version')
                apply_vcs_import(freeze_file)
        else:
            Output._print_colored('Installing new jar')
            apply_vcs_import(freeze_file)


def apply_vcs_import(freeze_file):
    resources_dir = get_kooki_dir()
    user_jars_dir = os.path.join(resources_dir, 'jars')
    repos = import_get_repositories(freeze_file)
    import_args = argparse.Namespace()
    import_args.path = user_jars_dir
    import_args.force = False

    jobs = import_generate_jobs(repos, import_args)
    import_add_dependencies(jobs)

    results = execute_jobs(jobs, show_progress=True, number_of_workers=1, debug_jobs=False)
    output_results(results)
