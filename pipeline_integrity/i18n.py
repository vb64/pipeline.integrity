"""Localization stuff."""
from py23 import open_text_file, gen_next


class Lang:
    """Embedded languages for localize explain text."""

    Ru = 'ru'


def fake_gettext(text, context):
    """Translate text in given context."""
    if isinstance(context.is_explain, dict):
        return context.is_explain.get(text, text)

    return text


def read_item(sign, line, inp):
    """Read multiline text item from given start line and input.

    Return tuple from item and last read line.
    """
    item = [line.strip().split(sign)[1].strip('"')]
    line = gen_next(inp).strip()
    while line.startswith('"'):
        item.append(line.strip('"'))
        line = gen_next(inp).strip()

    return (''.join(item), line)


def read_pair(line, inp):
    """Read and return pair msgid, msgstr from given start line and input."""
    msgid, line = read_item('msgid ', line, inp)
    msgstr, line = read_item('msgstr ', line, inp)

    return (msgid, msgstr)


def load_po(file_name):
    """Load data from given po file and return it as dict."""
    data = {}
    with open_text_file(file_name, 'r', 'utf-8') as inp:
        for line in inp:
            if line.startswith('msgid '):
                msgid, msgstr = read_pair(line, inp)
                if msgid and msgstr:
                    data[msgid] = msgstr

    return data
