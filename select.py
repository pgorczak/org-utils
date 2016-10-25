import os.path

import appex
import dialogs
import reminders

import orgfile


def select(elements):
    titles = tuple(e['headline'] for e in elements)
    items = dict(zip(titles, elements))

    return tuple(items[s] for s in dialogs.list_dialog(
        items=titles, multiple=True))


def get_or_create_calendar(title):
    calendars = {c.title: c for c in reminders.get_all_calendars()}

    try:
        return calendars[title]
    except KeyError:
        new_calendar = reminders.Calendar()
        new_calendar.title = title
        new_calendar.save()
        return new_calendar


def create_reminder(item, calendar):
    r = reminders.Reminder(calendar)
    r.title = item['headline']
    if 'deadline' in item:
        r.due_date = item['deadline']
    if 'scheduled' in item:
        a = reminders.Alarm()
        a.date = item['scheduled']
        r.alarms = [a]
    return r


if __name__ == '__main__':
    fp = appex.get_file_path()
    if not fp:
        exit(0)
    fn, ext = os.path.splitext(os.path.basename(fp))
    c = get_or_create_calendar(fn)
    for item in select(orgfile.agenda_from_file(fp)):
        # TODO get existing reminders
        if item['todo'] != 'DONE':
            create_reminder(item, c).save()
