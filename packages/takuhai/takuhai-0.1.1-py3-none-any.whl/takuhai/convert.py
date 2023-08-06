import codecs
import datetime
import os
from collections import OrderedDict


def convert(path, root='.'):
    """
    Insert metadata to a Pelican markdown file and
    overwrite the file.

    `path` format is `<YYMMDD><sep><title>.<ext>`.
    For example, `171206_Let's start.md`.

    Parameters
    ----------
    path : str
        Filename of a markdown file to be converted.
    root : str, optional
        Root directory. If ommited, the current directory is used.
    """
    abspath = os.path.join(root, path)
    with codecs.open(abspath, 'r', 'utf-8') as file:
        lines = file.readlines()

    metadata = create_metadata(path, root)
    insert_metadata(lines, metadata)

    with codecs.open(abspath, 'w', 'utf-8') as file:
        file.write(''.join(lines))


def create_metadata(path, root='.'):
    category = None
    directory, basename = os.path.split(path)
    while directory:
        directory, category = os.path.split(directory)

    basename = os.path.splitext(basename)[0]
    date, title = basename[:6], basename[7:]
    date = '-'.join(['20' + date[0:2], date[2:4], date[4:6]])

    abspath = os.path.join(root, path)
    if os.path.exists(abspath):
        st_mtime = os.stat(abspath).st_mtime
        dt = datetime.datetime.fromtimestamp(st_mtime)
        modified = dt.strftime('%Y-%m-%d %H:%M')
    else:
        modified = None

    metadata = OrderedDict()
    metadata['Title'] = title
    metadata['Date'] = date
    metadata['Modified'] = modified
    metadata['Category'] = category

    return metadata


def insert_metadata(lines, metadata):
    def key_value(key, sep):
        return ': '.join([key, metadata.pop(key)]) + sep

    # Until the first null line or line without ':'.
    for index, line in enumerate(lines):
        sep = '\r\n' if line.endswith('\r\n') else '\n'
        if line.strip() == '' or ':' not in line:
            break
        key, *_ = line.split(':')
        key = key.strip()
        if key in metadata and metadata[key]:
            lines[index] = key_value(key, sep)

    # insert the rest metadata.
    for key in list(metadata.keys()):  # for pop
        if metadata[key]:
            lines.insert(index, key_value(key, sep))
            index += 1
