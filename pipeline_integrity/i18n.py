"""Localization stuff."""


class Lang:
    """Embedded languages for localize explain text."""

    Ru = 'ru'


def fake_gettext(text):
    """For marking text to translate."""
    return text


def read_item(sign, line, inp):
    """Read multiline text item from given start line and input.

    Return tuple from item and last read line.
    """
    item = [line.strip().split(sign)[1].strip('"')]
    line = inp.__next__().strip()  # pylint: disable=unnecessary-dunder-call
    while line.startswith('"'):
        item.append(line.strip('"'))
        line = inp.__next__().strip()  # pylint: disable=unnecessary-dunder-call

    return (''.join(item), line)


def read_pair(line, inp):
    """Read and return pair msgid, msgstr from given start line and input."""
    msgid, line = read_item('msgid ', line, inp)
    msgstr, line = read_item('msgstr ', line, inp)

    return (msgid, msgstr)


def load_po(file_name):
    """Load data from given po file and return it as dict."""
    data = {}
    with open(file_name, 'rt', encoding='utf-8') as inp:
        for line in inp:
            if line.startswith('msgid '):
                msgid, msgstr = read_pair(line, inp)
                if msgid and msgstr:
                    data[msgid] = msgstr

    return data
