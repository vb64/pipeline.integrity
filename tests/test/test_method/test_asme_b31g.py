"""Test asme_b31g.py module.

make test T=test_method/test_asme_b31g.py
"""
import pytest
from . import TestMethod


class TestsAsme(TestMethod):
    """Method asme b31g."""

    def test_context(self):
        """Method context."""
        from pipeline_danger.method.asme_b31g import Context as AsmeB31g
        from pipeline_danger.method import ErrDefectTypeNotSupported

        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 5)
        asme_b31g = AsmeB31g(defect)
        assert asme_b31g.name == "ASME B31G"

        from pipeline_danger.defect import Type
        defect.type = Type.Dent

        with pytest.raises(ErrDefectTypeNotSupported) as err:
            AsmeB31g(defect)
        assert 'not supported by method' in str(err.value)
