import os
import kooki

resource_dir_env = 'KOOKI_DIR'
resource_dir_default = '~/.kooki'

def get_kooki_dir():
    resource_dir = os.environ.get(resource_dir_env)
    if not resource_dir:
        resource_dir = os.path.expanduser(resource_dir_default)
    return resource_dir


def get_kooki_dir_jars():
    resources_dir = get_kooki_dir()
    jars_dir = os.path.join(resources_dir, 'jars')
    return jars_dir


def get_kooki_dir_recipes():
    resources_dir = get_kooki_dir()
    recipes_dir = os.path.join(resources_dir, 'recipes')
    return recipes_dir
