"""Test asme_b31g.py module.

make test T=test_method/test_asme_b31g.py
"""
# import pytest
from . import TestMethod


class TestsAsme(TestMethod):
    """Method asme b31g."""

    def test_name(self):
        """Method name."""
        from pipeline_danger.method import asme_b31g

        assert asme_b31g.NAME == "ASME B31G"
