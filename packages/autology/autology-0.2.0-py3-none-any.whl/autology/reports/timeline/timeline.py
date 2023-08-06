"""
Timeline report that will process all of the files into a timeline in order to be published to the log.
"""
from datetime import datetime, time

from collections import namedtuple

from autology import topics
from autology.publishing import publish
from autology.reports.models import Report
from autology.reports.timeline import keys as fm_keys
from autology.reports.timeline.processors import markdown as md_loader, yaml_processor as yaml_loader

from autology.utilities import log_file

# The content that is stored for each individual day
_day_content = []

# Dates that have been collected
_dates = []

DayReport = namedtuple('DayReport', 'date url num_entries')


def register_plugin():
    """
    Subscribe to the initialize method and add default configuration values to the settings object.
    :return:
    """
    topics.Application.INITIALIZE.subscribe(_initialize)
    md_loader.register()
    yaml_loader.register()


def _initialize():
    """
    Register for all of the required events that will be fired off by the main loop
    :return:
    """
    topics.Processing.DAY_START.subscribe(_start_day_processing)
    topics.Processing.PROCESS_FILE.subscribe(_data_processor)
    topics.Processing.DAY_END.subscribe(_end_day_processing)
    topics.Processing.END.subscribe(_end_processing)


def _start_day_processing(date=None):
    """
    Event handler that will be notified when a day's files are starting to be processed.
    :param date: the day that is being processed.
    :return:
    """
    global _day_content
    _day_content = []


def _data_processor(file, date):
    """
    Checks to see if the data can be processed and stores any data required locally.
    :param file:
    :return:
    """
    file_loader = log_file.get_file_processor(file)

    if file_loader.mime_type is not md_loader.MIME_TYPE:
        return

    entry = file_loader.load(file)

    _day_content.append(entry)


def _end_day_processing(date=None):
    """Publish the content of the collated day together."""
    url = publish('timeline', 'day', entries=sorted(_day_content, key=lambda x: x.metadata[fm_keys.TIME]), date=date)
    _dates.append(DayReport(date=datetime.combine(date=date, time=time.min), url=url, num_entries=len(_day_content)))


def _end_processing():
    """All of the input files have been processed, so now need to build the master input value."""
    # Iterate through all of the values and count entries per day so can determine a decent legend value
    if _dates:
        max_entries = max(_dates, key=lambda x: x.num_entries).num_entries
        max_year = max(_dates, key=lambda x: x.date).date.year
        min_year = min(_dates, key=lambda x: x.date).date.year
    else:
        max_entries = 0
        max_year = min_year = datetime.now().year

    url = publish('timeline', 'index', dates=_dates, max_entries=max_entries, max_year=max_year, min_year=min_year)
    topics.Reporting.REGISTER_REPORT.publish(report=Report('Timeline', 'List of all report files', url))
