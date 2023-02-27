# -*- coding: utf-8 -*-
"""Test b31g_2012.py module.

make test T=test_method/test_asme/test_b31g_2012.py
"""
import pytest
from . import TestAsme


class TestsReadme2012(TestAsme):
    """Code from readme files."""

    def test_en(self):
        """Code from README.md 2012."""
        pipe = self.pipe_en
        defect = self.defect_en

        from pipeline_integrity.method.asme.b31g_2012 import Context, ErrMaterialSMTSNotDefined

        with pytest.raises(ErrMaterialSMTSNotDefined) as err:
            Context(defect)
        assert 'SMTS not defined' in str(err.value)

        pipe.material.smts = 1.5 * pipe.material.smys
        asme = Context(defect)

        # defect depth less than 10% wall thickness, no danger.
        assert defect.depth == 0.039
        assert defect.length == 4
        assert pipe.wallthickness == 0.63

        # classic
        assert round(asme.erf(is_explain=True), 3) == 0.704
        # modified
        assert round(asme.erf(is_mod=True, is_explain=True), 3) == 0.704

        # the depth of the defect is more than 80% of the pipe wall thickness
        defect.depth = 0.6
        assert round(asme.erf(is_explain=True), 3) == 0.874

        # the depth of the defect is 50% of the pipe wall thickness
        defect.depth = 0.31
        assert defect.length == 4
        assert round(asme.erf(is_explain=True), 3) == 0.748

        # a defect with a length of 30 inches and a depth of 50% of the pipe wall thickness
        defect.length = 30
        assert round(asme.erf(is_explain=True), 3) == 1.377

        assert pipe.maop == 900
        assert round(asme.safe_pressure, 2) == 653.71
        pipe.maop = 650
        assert round(asme.erf(is_explain=True), 3) < 1
        # print('###')
        # print(asme.explain())


class Tests2012(TestAsme):
    """Class B31G_2012 methods."""

    def setUp(self):
        """Set up test data."""
        super(Tests2012, self).setUp()

        from pipeline_integrity.method.asme.b31g_2012 import Context

        self.defect_en.pipe.material.smts = 1.5 * self.defect_en.pipe.material.smys
        self.asme = Context(self.defect_en)

    def test_s_flow(self):
        """Method s_flow."""
        pipe = self.asme.anomaly.pipe
        pipe.material.smts = 1.01 * pipe.material.smys

        assert self.asme.s_flow() == pipe.material.smts

    def test_get_stress_fail_mod(self):
        """Method get_stress_fail_mod."""
        assert round(self.asme.z_param, 3) == 0.454
        self.asme.anomaly.length = 50
        assert round(self.asme.z_param, 3) == 70.862
        assert round(self.asme.get_stress_fail_mod(), 3) == 54707.228
