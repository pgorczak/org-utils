import collections
import datetime
import re


def str_to_datetime(s):
    """ Org date-time-stamp to datetime object. """
    match = re.match(r'\[(.*)\ .*\ (\d\d:\d\d)\]', s)
    if match:
        date, time = match.groups()
        return datetime.datetime.strptime(date + time, '%Y-%m-%d%H:%M')


def datetime_to_str(dt):
    """ datetime object to Org date-time-stamp. """
    return dt.strftime('[%Y-%m-%d %a %H:%M]')


def str_to_date(s):
    """ Org date-stamp to datetime object. """
    match = re.match(r'<(.*)\ .*>', s)
    if match:
        return datetime.datetime.strptime(match.group(1), '%Y-%m-%d')


def date_to_str(d):
    """ datetime object to Org date-stamp. """
    return d.strftime('<%Y-%m-%d %a>')


# regexes and conversion functions for agenda-related markup
agenda_items = {
    'closed': (
        re.compile(r'CLOSED:\ (.*?\])'), str_to_datetime, datetime_to_str),
    'deadline': (
        re.compile(r'DEADLINE:\ (.*?>)'), str_to_date, date_to_str),
    'scheduled': (
        re.compile(r'SCHEDULED:\ (.*?>)'), str_to_date, date_to_str)
}


def str_to_agenda(l):
    """ Extracts agenda data from line of text.

    Returns:
        dict with agenda_items keys mapped to datetimes if present.
    """
    agenda = {}
    for key, (regex, from_string, to_string) in agenda_items.items():
        match = regex.search(l)
        if match:
            agenda[key] = from_string(match.group(1))
    return agenda


def str_to_headline(headline):
    """ Parse a headline.

    Returns:
        A dict with keys
            - headline: headline without markup
            - todo: 'TODO', 'DONE' or None
            - level: int, level of the headline

    Raises:
        AttributeError if line does not start with '*' (not a headline).
    """
    match = re.match(r'(\*+)\ (TODO|DONE)?\ ?(.*)', headline)
    return {'headline': match.group(3), 'todo': match.group(2),
            'level': match.end(1)}


def iter_agenda(org_str):
    """ Parses an org-file.

    Yields:
        A dict for every section with agenda info, containing:
            - output of str_to_headline()
            - output of str_to_agenda()
            - headline_location: line number of headline
            - agenda_location: line number of agenda

    Args:
        org_str: org file as string.
    """

    lines = collections.deque(enumerate(org_str.splitlines(), 1))

    def recur(lines, headline):
        while lines:
            n, l = lines.popleft()
            if l.startswith('*'):
                next_headline = str_to_headline(l)
                if next_headline['level'] > headline['level']:
                    next_headline['headline_location'] = n
                    yield from recur(lines, next_headline)
                else:
                    lines.appendleft((n, l))
                    break
            else:
                a = str_to_agenda(l)
                if a:
                    headline.update(a)
                    headline['agenda_location'] = n
                    yield headline

    yield from recur(lines, {'level': 0})
