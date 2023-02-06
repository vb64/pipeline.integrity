"""Test asme_b31g.py module.

make test T=test_method/test_asme_b31g.py
"""
import pytest
from . import TestMethod


class TestsCrvlBas(TestMethod):
    """Examples from CRVL.BAS."""

    def setUp(self):
        """All units as inches."""
        super().setUp()
        from pipeline_integrity.material import Material
        from pipeline_integrity.pipe import Pipe
        from pipeline_integrity.method.asme_b31g import Context

        maop = 910  # Lbs/sq.in.
        diam = 30  # Inches
        wallthick = 0.438  # Inches
        smys = 52000  # Lbs/sq.in.

        self.pipe = Pipe(50, diam, wallthick, Material("Steel", smys), maop)

        depth = 0.1  # Inches
        length = 7.5  # Inches

        self.defect = self.pipe.add_metal_loss(10, length, 10, 20, depth)
        self.asme = Context(self.defect)

    def test_example1(self):
        """Example 1."""
        assert not self.asme.is_ok
        assert not self.asme.is_replace
        assert round(self.asme.get_a(self.defect.length), 3) == 1.703  # 1.847
        assert round(self.asme.get_safe_pressure(self.defect.length)) == 1093
        assert round(self.asme.defect_max_length(), 3) == 8.216
        self.defect.depth = 0.249  # Inches
        assert round(self.asme.defect_max_length(), 3) == 2.663  # 7.5


class TestsAsme(TestMethod):
    """Method asme b31g."""

    def test_context(self):
        """Method context."""
        from pipeline_integrity.method.asme_b31g import Context as AsmeB31g
        from pipeline_integrity.method import ErrDefectTypeNotSupported

        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 5)
        asme_b31g = AsmeB31g(defect)
        assert asme_b31g.name == "ASME B31G"

        from pipeline_integrity.defect import Type
        defect.type = Type.Dent

        with pytest.raises(ErrDefectTypeNotSupported) as err:
            AsmeB31g(defect)
        assert 'not supported by method' in str(err.value)

    def test_pipe_state(self):
        """Property pipe_state."""
        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 1)
        assert defect.depth == 1
        assert defect.pipe.wallthickness == 10

        from pipeline_integrity.method.asme_b31g import Context, State

        asme_b31g = Context(defect)
        assert asme_b31g.pipe_state() == State.Ok

        defect.depth = 9
        assert asme_b31g.pipe_state() == State.Replace

        defect.depth = 5
        assert asme_b31g.pipe_state() == State.Defected

    def test_get_b(self):
        """Function get_b."""
        from pipeline_integrity.method.asme_b31g import Context

        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 1.5)
        asme_b31g = Context(defect)
        assert round(asme_b31g.relative_depth, 1) == 15.0
        assert round(asme_b31g.get_b(), 1) == 4.0

        defect.depth = 5
        assert round(asme_b31g.relative_depth, 1) == 50.0
        assert round(asme_b31g.get_b(), 1) == 0.8

    def test_defect_max_length(self):
        """Function defect_max_length."""
        from pipeline_integrity.method.asme_b31g import Context

        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 1.5)
        asme_b31g = Context(defect)

        assert round(asme_b31g.defect_max_length(), 1) == 533.9

        defect.depth = 5
        assert round(asme_b31g.defect_max_length(), 1) == 100.1

    def test_explain(self):
        """Function explain."""
        from pipeline_integrity.method.asme_b31g import Context

        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 1.5)
        asme_b31g = Context(defect)
        assert asme_b31g.explain() == ''
        asme_b31g.explain_text = ['xx', 'yy']
        assert asme_b31g.explain() == 'xx\nyy'
