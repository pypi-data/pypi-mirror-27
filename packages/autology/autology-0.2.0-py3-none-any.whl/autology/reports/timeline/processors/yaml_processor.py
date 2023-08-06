"""
Defines the yaml file processor.
"""
import yaml
from autology.utilities import log_file


MIME_TYPE = 'application/x-yaml'


def load_file(path):
    """
    Translate the file pointed to by path into a dictionary.
    :param path:
    :return:
    """
    with path.open() as loaded_file:
        data = [d for d in yaml.load_all(loaded_file)]

    return data


def register():
    """Register the YAML mimetype and the YAML file processor."""
    log_file.register_mime_type('.yaml', MIME_TYPE)
    log_file.register_file_processor(MIME_TYPE, load_file)
