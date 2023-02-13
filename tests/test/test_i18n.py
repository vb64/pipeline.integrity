"""Test i18n.py module.

make test T=test_i18n.py
"""
from . import TestBase


class TestsI18n(TestBase):
    """Module i18n.py."""

    @staticmethod
    def test_fake_gettext():
        """Function fake_gettext."""
        from pipeline_integrity.i18n import fake_gettext

        assert fake_gettext('xxx') == 'xxx'
