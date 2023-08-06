"""Utilities for processing log files."""
import mimetypes
import datetime
import tzlocal
import pathlib

from collections import namedtuple

_file_processors = {}


_FileProcessor = namedtuple('FileProcessor', 'mime_type load lookup_time')
DEFAULT_FILE_PROCESSOR = _FileProcessor('undefined', lambda x: None, lambda x: default_time_getter(x))


def register_mime_type(file_extension, mime_type):
    """Register the mime types in the system library. """
    mimetypes.add_type(mime_type, file_extension)


def lookup_mime_type(file_component):
    """Lookup the mime type based on the pathlib path provided."""
    file_component = file_component.resolve()
    file_type, encoding = mimetypes.guess_type(file_component.as_uri())
    return file_type


def default_time_getter(file):
    """Return localized now when time getter not defined."""
    return tzlocal.get_localzone().localize(datetime.datetime.now())


def register_file_processor(mime_type, file_loader, time_getter=default_time_getter):
    """Register file processor for specified mime_type."""
    _file_processors[mime_type] = _FileProcessor(mime_type, file_loader, time_getter)


def get_file_processor(file):
    """Retrieve the file processor for the provided file."""
    mime_type = lookup_mime_type(file)
    return _file_processors.get(mime_type, DEFAULT_FILE_PROCESSOR)


def walk_log_files(directories):
    """Generator that will walk through all of the log files and yield each file in datetime order."""
    sorted_files = {}

    # Need to find all of the files that are stored in the input_files directories in order to start building the
    # reports that will be used to generate the static log files.
    for input_path in directories:
        search_path = pathlib.Path(input_path)

        for file_component in search_path.glob('**/*'):

            if not file_component.is_dir():
                file_processor = get_file_processor(file_component)

                if file_processor:
                    entry = file_processor.load(file_component)
                    entry_time = file_processor.lookup_time(entry)

                    storage = sorted_files.setdefault(entry_time.year, {})
                    storage = storage.setdefault(entry_time.month, {})
                    storage.setdefault(entry_time.day, []).append(file_component)

    # Now need to process each of the files in order, and build up a master static page for the content.
    for year in sorted(sorted_files.keys()):
        month_files = sorted_files[year]

        for month in sorted(month_files.keys()):
            day_files = month_files[month]

            for day in sorted(day_files.keys()):
                time_files = day_files[day]

                date_to_process = datetime.date(year, month, day)

                for content_file in time_files:
                    try:
                        yield date_to_process, content_file
                    except Exception:
                        import traceback
                        print('Exception raised while processing: {}'.format(content_file))
                        traceback.print_exc()
