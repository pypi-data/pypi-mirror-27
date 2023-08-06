from kooki.tools import get_extension
import yaml
import toml
import json
import os

def Metadata(document):
    metadata_dict = {}
    for file_path, file_content in document.metadata.items():
        metadata = load(file_path, file_content)
        metadata_dict = data_merge(metadata, metadata_dict)
    return metadata_dict


def load(file_path, file_content):

    extension = get_extension(file_path)

    if extension == '':
        metadata = load_metadata(file_content)
    else:
        if extension == 'yaml' or extension == 'yml':
            metadata = yaml.safe_load(file_content)
        elif extension == 'toml':
            metadata = toml.loads(file_content)
        elif extension == 'json':
            metadata = json.loads(file_content)

    return metadata


def load_metadata(file_path, file_content):

    metadata_loaders = []
    metadata_loaders.append(yaml.safe_load)
    metadata_loaders.append(toml.loads)
    metadata_loaders.append(json.loads)

    for loader in metadata_loaders:
        try:
            metadata = loader(file_content)
            return metadata
        except:
            pass

    raise(Exception('Cannot load metadata provided: {}'.format(file_path)))


def data_merge(a, b):

    class MergeError(Exception):
        pass

    key = None

    try:
        if a is None or isinstance(a, str) or isinstance(a, bytes) or isinstance(a, int) or isinstance(a, float):
            a = b
        elif isinstance(a, list):
            if isinstance(b, list):
                a.extend(b)
            else:
                a.append(b)
        elif isinstance(a, dict):
            if isinstance(b, dict):
                for key in b:
                    if key in a:
                        a[key] = data_merge(a[key], b[key])
                    else:
                        a[key] = b[key]
            else:
                raise MergeError('Cannot merge non-dict "%s" into dict "%s"' % (b, a))
        else:
            raise MergeError('NOT IMPLEMENTED "%s" into "%s"' % (b, a))
    except TypeError as e:
        raise MergeError('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a))
    return a
