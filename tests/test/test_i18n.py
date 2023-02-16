"""Test i18n.py module.

make test T=test_i18n.py
"""
import os
from . import TestBase


class TestsI18n(TestBase):
    """Module i18n.py."""

    @staticmethod
    def test_fake_gettext():
        """Function fake_gettext."""
        from pipeline_integrity.i18n import fake_gettext

        assert fake_gettext('xxx') == 'xxx'

    @staticmethod
    def test_load_po():
        """Function load_po."""
        from pipeline_integrity.i18n import load_po

        data = load_po(os.path.join(
          'pipeline_integrity', 'method', 'asme_b31g', 'locale',
          'ru', 'LC_MESSAGES', 'messages.po'
        ))
        assert len(data) == 23
