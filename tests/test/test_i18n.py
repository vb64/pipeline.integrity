"""Test i18n.py module.

make test T=test_i18n.py
"""
import os
from . import TestBase


class TestsI18n(TestBase):
    """Module i18n.py."""

    def test_fgettext(self):
        """Check fake_gettext function."""
        from pipeline_integrity.i18n import fake_gettext, Lang
        from pipeline_integrity.method.asme.b31g_1991 import Context

        asme = Context(self.pipe.add_metal_loss(10, 100, 10, 20, 1.5))
        asme.is_explain = Context.lang(Lang.Ru)
        assert fake_gettext('xxx', asme) == 'xxx'
        text = fake_gettext("Parameter B.", asme)
        assert " B." in text
        assert "Parameter " not in text

        asme.is_explain = False
        assert fake_gettext("Parameter B.", asme) == "Parameter B."

    @staticmethod
    def test_load_po():
        """Check load_po function."""
        from pipeline_integrity.i18n import load_po

        data = load_po(os.path.join(
          'pipeline_integrity', 'method', 'asme', 'locale',
          'ru', 'LC_MESSAGES', 'messages.po'
        ))
        assert len(data) > 1
