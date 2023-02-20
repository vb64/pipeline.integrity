"""Module for i18n stuff."""
import os
import gettext

LANG_CODE = 'ru'


def activate(app, lang_code):
    """Activate locale for given language code."""
    lang_code = lang_code or 'en'
    locale_path = os.path.dirname(os.path.abspath(__file__))
    trans = gettext.translation(
      'messages',
      os.path.join(locale_path, 'locale'),
      languages=[lang_code]
    )
    trans.install()
    app.jinja_env.add_extension('jinja2.ext.i18n')
    app.jinja_env.install_gettext_translations(trans)
