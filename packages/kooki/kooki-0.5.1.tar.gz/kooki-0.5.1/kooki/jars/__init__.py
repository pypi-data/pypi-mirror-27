from os.path import join, isfile, isdir
from os import getcwd
from kooki.config import get_kooki_dir, get_kooki_dir_recipes, get_kooki_dir_jars

import argparse
from vcstool.commands.export import ExportCommand
from vcstool.crawler import find_repositories
from vcstool.executor import ansi, execute_jobs, generate_jobs, output_repositories, output_results


def search_jar(jar):
    ret_jar_path = None
    user_jars_dir = get_kooki_dir_jars()
    jar_path = join(user_jars_dir, jar)
    if isdir(jar_path):
        ret_jar_path = jar_path
    return ret_jar_path


def search_recipe(recipe):
    ret_recipe_path = None
    user_recipes_dir = get_kooki_dir_recipes()
    recipe_path = join(user_recipes_dir, recipe, 'recipe.py')
    if isfile(recipe_path):
        ret_recipe_path = recipe_path
    return ret_recipe_path


def search_file(jars, recipe, filename):
    ret_file_path = None
    ret_file_path = search_file_in_local(filename)
    if not ret_file_path:
        ret_file_path = search_file_in_jars(jars, recipe, filename)
    return ret_file_path


def search_file_in_local(filename):
    ret_file_path = None
    file_path = join(getcwd(), filename)
    if isfile(file_path):
        ret_file_path = file_path
    return ret_file_path


def search_file_in_jars(jars, recipe, filename):
    user_jars_dir = get_kooki_dir_jars()
    for jar in jars:
        jar_path = join(user_jars_dir, jar)
        ret_file_path = search_file_in_jar(jar_path, recipe, filename)
        if ret_file_path: break
    return ret_file_path


def search_file_in_jar(jar_path, recipe, filename):
    ret_file_path = search_file_in_jar_recipe(jar_path, recipe, filename)
    if not ret_file_path:
        ret_file_path = search_file_in_jar_local(jar_path, filename)
    return ret_file_path


def search_file_in_jar_recipe(jar_path, recipe, filename):
    ret_file_path = None
    recipe_jar_path = join(jar_path, recipe)
    file_path = join(recipe_jar_path, filename)
    if isfile(file_path):
        ret_file_path = file_path
    return ret_file_path


def search_file_in_jar_local(jar_path, filename):
    ret_file_path = None
    file_path = join(jar_path, filename)
    if isfile(file_path):
        ret_file_path = file_path
    return ret_file_path


def get_jars():
    resources_dir = get_kooki_dir()
    user_jars_dir = os.path.join(resources_dir, 'jars')

    jars = {}

    for jar in os.listdir(user_jars_dir):
        jar_path = os.path.join(user_jars_dir, jar)
        export_args = argparse.Namespace()
        export_args.path = jar_path
        export_args.exact = True
        command = ExportCommand(export_args)
        clients = find_repositories([jar_path])
        jobs = generate_jobs(clients, command)
        results = execute_jobs(jobs)

        if len(results) == 1:
            result = results[0]
            if 'export_data' in result:
                export_data = result['export_data']
                vcs_type = result['client'].__class__.type
                vcs_url = export_data['url']
                vcs_version = export_data['version']
                save_jar = {}
                save_jar['type'] = vcs_type
                save_jar['url'] = vcs_url
                save_jar['version'] = vcs_version
                jars[jar] = save_jar

    return jars
