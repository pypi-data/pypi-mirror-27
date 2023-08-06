import os, yaml, logging
import kooki
from kooki.tools import DictAsMember

import pykwalify
import pykwalify.core
import pkgutil

class EmptyLog():
    def debug(*args, **kwargs):
        pass
    def error(*args, **kwargs):
        pass
    def info(*args, **kwargs):
        pass

def parse_args(args):
    config_file_checker(args.config_file)
    config = config_file_parser(args.config_file)
    document_rules = create_document_rules(config, args.documents)
    return document_rules


def config_file_checker(config_file):

    if not os.path.isfile(config_file):
        raise Exception('The config file provided (\'{}\') does not exist'.format(config_file))

    format_path = os.path.join(os.path.dirname(kooki.config.__file__), 'format.yaml')
    pykwalify.core.log = EmptyLog()
    c = pykwalify.core.Core(source_file=config_file, schema_files=[format_path])

    try:
        c.validate(raise_exception=True)
        return c.source

    except pykwalify.errors.SchemaError as e:
        message = 'The config file provided (\'{}\') is invalid\n'.format(config_file)
        for error in c.errors[:-1]:
            message += '{}\n'.format(error)
        message += '{}'.format(c.errors[-1])
        raise Exception(message)


def config_file_parser(config_file):
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream.read())
        return config


def create_document_rules(config, documents):

    default = {
        'name': '',
        'template': '',
        'recipe': '',
        'jars': [],
        'metadata': [],
        'content': []}

    document_names = []

    for key, value in config.items():
        if key in default:
            default[key] = value
        else:
            document_names.append(key)

    document_rules = {}

    if documents == []:
        for document_name in document_names:
            specific = default.copy()
            for key, value in config[document_name].items():
                if key in specific:
                    specific[key] = value
            document_rules[document_name] = DictAsMember(specific)
    else:
        for document_name in documents:
            if document_name in document_names:
                specific = default.copy()
                for key, value in config[document_name].items():
                    if key in specific:
                        specific[key] = value
                document_rules[document_name] = DictAsMember(specific)
            else:
                raise Exception('There is no rule for the document \'{}\''.format(document_name))

    return DictAsMember(document_rules)
