"""Localization stuff."""


def fake_gettext(text):
    """For marking text to translate."""
    return text


def load_po(file_name):
    """Load data from given po file and return it as dict."""
    data = {'': file_name}
    return data
