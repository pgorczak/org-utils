import codecs

import appex
import dialogs
import reminders

import utils


def select_from_file():
    fp = appex.get_file_path()
    if fp:
        with codecs.open(fp, 'r', 'utf-8') as f:
            org_str = f.read()

        elements = tuple(utils.iter_agenda(org_str))
        titles = tuple(e['headline'] for e in elements)
        items = dict(zip(titles, elements))

        selected = tuple(items[s] for s in dialogs.list_dialog(
            items=titles, multiple=True))

        return selected


def get_or_create_calendar(title):
    calendars = {c.title: c for c in reminders.get_all_calendars()}

    try:
        return calendars['title']
    except KeyError:
        new_calendar = reminders.Calendar()
        new_calendar.title = title
        new_calendar.save()
        return new_calendar


def create_reminder(item):
    r = reminders.Reminder(c)
    r.title = item['headline']
    if 'deadline' in item:
        r.due_date = item['deadline']
    if 'scheduled' in item:
        a = reminders.Alarm()
        a.date = item['scheduled']
        r.alarms = [a]
    return r


if __name__ == '__main__':
    c = get_or_create_calendar('org-utils')
    for item in select_from_file():
        # TODO get existing reminders
        item['todo'] != 'DONE':
            create_reminder(item).save()
