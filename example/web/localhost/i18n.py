"""Module for i18n stuff."""
import os
import gettext


def activate(lang_code):
    """Activate given locale."""
    locale_path = os.path.dirname(os.path.abspath(__file__))
    gettext.translation(
      'messages',
      os.path.join(locale_path, 'locale'),
      languages=[lang_code]
    ).install()
