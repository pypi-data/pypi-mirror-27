"""
Defines the markdown file processor.  Registers the mimetype that will be used to fetch the time values from the
markdown file, as well as a means of translating the data into a data definition.

This will be registered in the generator as part of the report initialization plugin.
"""
import frontmatter
from autology.reports.timeline import keys as fmkeys
from autology.utilities import log_file
from autology.configuration import get_configuration
import pytz


MIME_TYPE = 'text/markdown'


def load_file(path):
    """
    Translate the file pointed to by path into a front matter post.  It will also go through all of the timestamps that
    are stored in the front matter and make them timezone aware.
    :param path:
    :return:
    """
    with path.open() as loaded_file:
        entry = frontmatter.load(loaded_file)

    _process_datetimes(entry.metadata)

    return entry


def time_value(entry):
    """
    Translate the entry into the time value for the start.
    :param entry:
    :return:
    """
    return entry.metadata[fmkeys.TIME]


def register():
    """Register the markdown file processor."""
    log_file.register_file_processor(MIME_TYPE, load_file, time_value)


def _process_datetimes(dictionary):
    """
    Translate all of the datetime objects that are stored in the front matter and make them timezone aware.
    :param dictionary: the dictionary containing the values to process.  This will need to be called recursively on all
    dictionaries contained within.
    :return:
    """
    for key in dictionary.keys():
        if hasattr(dictionary[key], 'tzinfo') and dictionary[key].tzinfo is None:
            # All of the values read in are parsed into UTC time, yaml does this conversion for us when there is
            # timezone information
            utc_value = pytz.utc.localize(dictionary[key])
            site_timezone = pytz.timezone(get_configuration().site.timezone)
            dictionary[key] = utc_value.astimezone(site_timezone)
        elif hasattr(dictionary[key], 'keys'):
            _process_datetimes(dictionary[key])

    return dictionary
