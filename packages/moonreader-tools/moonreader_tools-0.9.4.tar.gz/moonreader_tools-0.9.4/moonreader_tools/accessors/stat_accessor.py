"""
Contains class responsible for Statistics object
reading and writing to files
"""
import io
import os
import re

from moonreader_tools.conf import STAT_EXTENSION
from moonreader_tools.stat import Statistics


class StatsAccessor(object):
    """
    Import and export statistics objects
    """
    _STATISTICS_FORMAT_RE = r"""
(^(?P<timestamp>[\d]+))     # When book was added to the shelf
(\*(?P<pages>[\d]+))        # total number of pages
(\@(?P<no1>[\d]+))?         # unknown field 1
(\#(?P<no2>[\d]+))?         # unknown field 1
(:(?P<percentage>[\d.]+))%  # ratio of already read pages
"""
    _STATISTICS_FORMAT_RE = re.compile(_STATISTICS_FORMAT_RE, re.VERBOSE)

    def stats_from_string(self, text: str) -> Statistics:
        match = self._STATISTICS_FORMAT_RE.match(text)
        if not match:
            raise ValueError("Note content cannot be analyzed.")
        items = match.groupdict()
        return Statistics(**items)

    def stats_to_string(self, stats: Statistics) -> str:
        """Creates string representation of the object,
        ready to be saved into the file"""
        result = ""
        result += str(stats.timestamp)
        result += "*"

        result += str(stats.pages)
        result += ":"

        result += str(stats.percentage) + "%"
        return result

    def stats_to_file(self, stats: Statistics, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.stats_to_string(stats))

    def stats_from_file(self, filename: str) -> Statistics:
        if not filename or not os.path.exists(filename):
            raise ValueError("File does not exist: {}".format(filename))
        assert filename.endswith(STAT_EXTENSION)

        with io.open(filename, encoding="utf-8") as stat_file:
            content = stat_file.read()
            if isinstance(content, type(b'bytes')):
                content = content.decode('utf-8')
            if len(content) == 0:
                return Statistics.empty_stats()
            return self.stats_from_string(content)
