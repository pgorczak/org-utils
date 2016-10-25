import unittest

from orgfile import *


class TestOrgfile(unittest.TestCase):
    def test_datetime(self):
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        self.assertEqual(now, str_to_datetime(datetime_to_str(now)))

    def test_date(self):
        now = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(now, str_to_date(date_to_str(now)))

    def test_agenda(self):
        scheduled = datetime.datetime(year=2001, month=1, day=1)
        closed = datetime.datetime(year=2002, month=2, day=2)
        deadline = datetime.datetime(year=2003, month=3, day=3)

        line = '  CLOSED: {} SCHEDULED: {} DEADLINE: {}'.format(
            datetime_to_str(closed), date_to_str(scheduled),
            date_to_str(deadline))

        self.assertEqual(str_to_agenda(line), {
            'scheduled': scheduled,
            'closed': closed,
            'deadline': deadline})

    def test_headline(self):
        self.assertEqual(str_to_headline('* lorem ipsum'), {
            'headline': 'lorem ipsum', 'todo': None, 'level': 1})

        self.assertEqual(str_to_headline('** TODO lorem ipsum'), {
            'headline': 'lorem ipsum', 'todo': 'TODO', 'level': 2})

        self.assertEqual(str_to_headline('*** DONE lorem ipsum'), {
            'headline': 'lorem ipsum', 'todo': 'DONE', 'level': 3})

    def test_file(self):
        agenda = agenda_from_file('test_file.org')

        self.assertEqual(agenda, (
            {
                'headline': 'Do the first thing',
                'level': 1,
                'todo': None,
                'headline_location': 1,
                'deadline': datetime.datetime(2016, 10, 18),
                'scheduled': datetime.datetime(2016, 10, 17),
                'agenda_location': 2
            },
            {
                'headline': 'Do the second thing',
                'level': 1,
                'todo': 'TODO',
                'headline_location': 5,
                'deadline': datetime.datetime(2016, 10, 23),
                'scheduled': datetime.datetime(2016, 10, 18),
                'agenda_location': 6
            },
            {
                'headline': 'Do the third thing',
                'level': 1,
                'todo': 'DONE',
                'headline_location': 8,
                'closed': datetime.datetime(2016, 10, 16, 22, 18),
                'deadline': datetime.datetime(2016, 10, 19),
                'agenda_location': 9
            }))
