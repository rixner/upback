"""
Misc utilities
"""

import datetime
import dateutil.parser
import dateutil.tz
import os
import fnmatch
import re

utc = dateutil.tz.tzutc()
num = re.compile(".*\.(\d+)")

#TODO: implement a more refined matching
# e.g. wildcard/ only matches dirs
# and others similarly to .gitignore
def wildcard_match(item, wildcard):
    return fnmatch.fnmatch(item, wildcard)

def is_path_local(path):
    return not ":" in path

def parse_rfc3339(datetime_string, report_precision=False):
    """ Returns a datetime object for
        a RFC3339-formatted string
    """
    time_3339 = dateutil.parser.parse(datetime_string)
    if time_3339.tzinfo == None:
        time_3339 = time_3339.replace(tzinfo=utc)
    else:
        time_3339 = time_3339.astimezone(utc)
    if report_precision:
        precision = 0
        match = num.match(datetime_string)
        if match:
            frac = match.group(1)
            precision = len(frac)
        return (time_3339, precision)
    else:
        return time_3339

def lock_file(path):
    """ Creates a lockfile
        Returns True if the lockfile was absent and has been created
        Returns False if the lockfile was already present
    """
    #TODO if open fails and the lockfile is present, check its creation date
    # and, if it's more than ??? remove it and retry
    # pylint: disable=global-statement
    try:
        lock_fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_EXCL)
    except OSError:
        return False
    else:
        global LOCK_FILENAME
        LOCK_FILENAME = path
        os.close(lock_fd)
        return True

def remove_lock_file():
    """ Removes a previously created lockfile (if any) """
    # pylint: disable=global-statement
    global LOCK_FILENAME

    if LOCK_FILENAME is not None and os.path.isfile(LOCK_FILENAME):
        os.unlink(LOCK_FILENAME)

LOCK_FILENAME = None
