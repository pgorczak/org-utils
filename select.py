import codecs

import appex
import dialogs

import utils

fp = appex.get_file_path()
if fp:
    with codecs.open(fp, 'r', 'utf-16') as f:
        org_str = f.read()

    elements = tuple(utils.iter_agenda(org_str))
    titles = tuple(e['headline'] for e in elements)
    items = dict(zip(titles, elements))

    selected = tuple(items[s] for s in dialogs.list_dialog(items=titles))

    print(selected)
