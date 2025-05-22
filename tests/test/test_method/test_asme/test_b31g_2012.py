# -*- coding: utf-8 -*-
"""Test b31g_2012.py module.

make test T=test_method/test_asme/test_b31g_2012.py
"""
import pytest
from . import TestAsme


class TestsReadme2012(TestAsme):
    """Code from readme files."""

    def test_ru(self):
        """Code from READMEru.md 2012."""
        pipe = self.pipe_ru
        defect = self.defect_ru

        from pipeline_integrity.method.asme.b31g_2012 import Context

        assert pipe.material.smys == 295
        pipe.material.smts = 420

        asme = Context(defect)

        assert defect.depth == 1
        assert pipe.wallthickness == 16

        assert asme.years() > 1
        assert 0.95 < asme.erf() < 0.97

        pipe.maop = 0.01
        assert asme.years() == Context.REPAIR_NOT_REQUIRED
        pipe.maop = 7

        defect.depth = 8
        defect.length = 200
        assert asme.years() == 0
        assert asme.erf() > 1

        assert pipe.maop == 7
        assert round(asme.safe_pressure, 2) > 6
        pipe.maop = asme.safe_pressure - 0.1

        from pipeline_integrity.i18n import Lang

        asme.is_explain = asme.lang(Lang.Ru)
        assert asme.years() > 0

        assert round(asme.erf(), 3) == 0.984
        assert round(asme.safe_pressure, 1) == 6.2

        Context.design_factor = 0.72
        asme = Context(defect)

        assert round(asme.erf(), 3) == 1.367
        assert round(asme.safe_pressure, 1) == 4.5
        assert asme.years() == 0

    def test_en(self):
        """Code from README.md 2012."""
        pipe = self.pipe_en
        defect = self.defect_en

        from pipeline_integrity.method.asme.b31g_2012 import Context, ErrMaterialSMTSNotDefined

        with pytest.raises(ErrMaterialSMTSNotDefined) as err:
            Context(defect)
        assert 'SMTS not defined' in str(err.value)

        pipe.material.smts = 1.5 * pipe.material.smys
        # to inches
        Context.corrosion_rate = Context.corrosion_rate / 25.4

        asme = Context(defect)

        # defect depth less than 10% wall thickness, no danger.
        assert defect.depth == 0.039
        assert defect.length == 4
        assert pipe.wallthickness == 0.63

        assert asme.years() > 0
        # classic
        assert 0.7 < asme.erf() < 0.71
        # modified
        assert round(asme.erf(is_mod=True), 3) == 0.704

        pipe.maop = 1
        assert asme.years() == Context.REPAIR_NOT_REQUIRED
        pipe.maop = 900

        # the depth of the defect is more than 80% of the pipe wall thickness
        defect.depth = 0.6
        assert round(asme.erf(), 3) == 0.874

        # the depth of the defect is 50% of the pipe wall thickness
        defect.depth = 0.31
        assert defect.length == 4
        assert 0.74 < asme.erf() < 0.75

        # a defect with a length of 30 inches and a depth of 50% of the pipe wall thickness
        defect.length = 30
        assert asme.years() == 0
        assert asme.erf() > 1.3

        assert pipe.maop == 900
        assert round(asme.safe_pressure, 2) == 653.71
        pipe.maop = 500
        asme.is_explain = True
        assert asme.years() > 0


class Tests2012(TestAsme):
    """Class B31G_2012 methods."""

    def setUp(self):
        """Set up test data."""
        super(Tests2012, self).setUp()

        from pipeline_integrity.method.asme.b31g_2012 import Context

        self.defect_en.pipe.material.smts = 1.5 * self.defect_en.pipe.material.smys
        self.asme = Context(self.defect_en)

    def test_str(self):
        """Method str."""
        assert 'ASME B31G' in str(self.asme)

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

    def test_safe_pressure_zero(self):
        """Method safe_pressure zero case."""
        save = self.asme.get_press_fail
        self.asme.get_press_fail = lambda is_mod: 0
        assert self.asme.erf() == 1
        self.asme.get_press_fail = save
