# -*- coding: utf-8 -*-
"""Test b31g_2012.py module.

make test T=test_method/test_asme/test_b31g_2012.py
"""
import pytest
from . import TestAsme


class TestsReadme2012(TestAsme):
    """Code from readme files."""

    def test_en(self):
        """Code from README.md."""
        pipe = self.pipe_en
        defect = self.defect_en

        from pipeline_integrity.method.asme.b31g_2012 import Context, ErrMaterialSMTSNotDefined

        with pytest.raises(ErrMaterialSMTSNotDefined) as err:
            Context(defect)
        assert 'SMTS not defined' in str(err.value)

        pipe.material.smts = 60000
        asme = Context(defect)

        # defect depth less than 10% wall thickness, no danger.
        assert defect.depth == 0.039
        assert pipe.wallthickness == 0.63

        assert round(asme.erf(), 3) == 7.821
