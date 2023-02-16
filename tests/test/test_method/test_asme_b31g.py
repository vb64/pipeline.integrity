# -*- coding: utf-8 -*-
"""Test asme_b31g.py module.

make test T=test_method/test_asme_b31g.py
"""
import pytest
from . import TestMethod


class TestsReadme(TestMethod):
    """Code from readme files."""

    @staticmethod
    def test_en():
        """Code from README.md."""
        from pipeline_integrity.material import Material
        from pipeline_integrity.pipe import Pipe

        pipe = Pipe(
          440,  # length inches
          56,  # diameter 56 inches
          0.63,  # wall thickness inches
          Material(  # pipe material
            "Steel",
            52000  # SMYS psi
          ),
          900  # pressure psi
        )

        defect = pipe.add_metal_loss(
          40,  # the defect starts at a distance of 40 inches from the beginning of the pipe
          4,  # defect length 4 inches
          10,  # along the circumference of the pipe, the defect begins
               # at 10 arc minutes from the top of the pipe
          20,  # the size of the defect along the circumference is 20 arc minutes
          0.039  # defect depth 0.039 inches
        )

        from pipeline_integrity.method.asme_b31g import Context, State

        asme = Context(defect)

        # defect depth less than 10% wall thickness, no danger.
        assert defect.depth == 0.039
        assert pipe.wallthickness == 0.63
        assert asme.pipe_state(is_explain=True) == State.Ok
        assert '10%' in asme.explain()

        # the depth of the defect is more than 80% of the pipe wall thickness,
        # repair or replacement of the pipe is necessary.
        defect.depth = 0.6
        assert asme.pipe_state(is_explain=True) == State.Replace
        assert '80%' in asme.explain()

        # the depth of the defect is 50% of the pipe wall thickness, but the length of the defect
        # does not exceed its maximum allowable length.
        # the defect is not dangerous.
        defect.depth = 0.31
        assert defect.length == 4
        assert round(asme.defect_max_length()) == 5
        assert asme.pipe_state() == State.Safe

        # a defect with a length of 20 inches and a depth of 50% of the pipe wall thickness
        # requires repair at the specified working pressure in the pipe.
        defect.length = 20
        assert asme.pipe_state() == State.Repair

        # when the operating pressure is reduced to a safe value, the defect does not require repair.
        assert pipe.maop == 900
        assert round(asme.safe_pressure, 2) == 700.68
        pipe.maop = 700
        assert asme.pipe_state(is_explain=True) == State.Defected
        assert 'defect is not dangerous' in asme.explain()

    @staticmethod
    def test_ru():
        """Code from READMEru.md."""
        from pipeline_integrity.material import Material
        from pipeline_integrity.pipe import Pipe

        pipe = Pipe(
          11200,  # длина 11.2 метра
          1420,  # диаметр 1420 мм
          16,  # толщина стенки 16 мм
          Material(  # материал трубы
            "Сталь",
            295  # предел текучести Мпа
          ),
          7  # рабочее давление Мпа
        )

        defect = pipe.add_metal_loss(
          1000,  # дефект начинается на расстоянии 1 метра от начала трубы
          100,  # длина дефекта 100 мм
          10,  # по окружности трубы дефект начинается на 10 угловых минут от верхней точки трубы
          20,  # размер дефекта по окружности составляет 20 угловых минут
          1  # глубина дефекта 1 мм
        )

        from pipeline_integrity.method.asme_b31g import Context, State

        asme = Context(defect)

        # глубина дефекта менее 10% толщины стенки трубы, опасности нет.
        assert defect.depth == 1
        assert pipe.wallthickness == 16
        assert asme.pipe_state() == State.Ok

        # глубина дефекта более 80% толщины стенки трубы, необходим ремонт или замена трубы.
        defect.depth = 15
        assert asme.pipe_state() == State.Replace

        # глубина дефекта 50% от толщины стенки трубы, но длина дефекта не превышает его
        # максимально допустимую длину.
        # дефект не представляет опасности.
        defect.depth = 8
        assert defect.length == 100
        assert round(asme.defect_max_length()) == 127
        assert asme.pipe_state() == State.Safe

        # дефект длиной 500 мм и глубиной 50% от толщины стенки трубы
        # требует ремонта при указанном рабочем давлении в трубе.
        defect.length = 500
        assert asme.pipe_state() == State.Repair

        # при снижении рабочего давления до безопасной величины дефект не требует ремонта.
        assert pipe.maop == 7
        assert round(asme.safe_pressure, 2) == 3.96
        pipe.maop = 3.95
        assert asme.pipe_state(is_explain=True) == State.Defected
        assert 'defect is not dangerous' in asme.explain()


class TestsCrvlBas(TestMethod):
    """Examples from CRVL.BAS."""

    def setUp(self):
        """All units as inches."""
        super(TestsCrvlBas, self).setUp()
        from pipeline_integrity.material import Material
        from pipeline_integrity.pipe import Pipe
        from pipeline_integrity.method.asme_b31g import Context, State

        self.state = State

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
        assert round(self.asme.get_safe_pressure()) == 1093
        assert round(self.asme.defect_max_length(), 3) == 8.216
        assert self.asme.pipe_state() == self.state.Safe

        self.defect.depth = 0.249  # Inches
        assert round(self.asme.defect_max_length(), 3) == 2.663  # 7.5
        assert self.asme.pipe_state() == self.state.Defected

    def test_example2(self):
        """Example 2."""
        self.pipe.material.yield_strength = 35000
        self.pipe.diameter = 20
        self.pipe.wallthickness = 0.25
        self.pipe.maop = 400
        self.defect.depth = 0.18
        self.defect.length = 10.0
        self.asme.design_factor = 0.5

        assert not self.asme.is_ok
        assert not self.asme.is_replace
        assert round(self.asme.defect_max_length(), 3) == 1.271
        assert round(self.asme.get_a(self.defect.length), 3) == 3.681  # 3.993
        assert round(self.asme.get_design_pressure()) == 438
        assert round(self.asme.get_safe_pressure()) == 286  # 284
        assert self.asme.pipe_state() == self.state.Repair

        self.pipe.maop = 285
        assert self.asme.pipe_state() == self.state.Defected
        assert round(self.asme.safe_pressure) == 286  # 284

    def test_example3(self):
        """Example 3."""
        self.pipe.diameter = 24
        self.pipe.wallthickness = 0.432
        self.defect.depth = 0.13
        self.defect.length = 30.0
        self.pipe.maop = 910

        assert round(self.asme.get_a(self.defect.length), 3) == 7.668  # 8.320
        assert round(self.asme.get_design_pressure()) == 1348
        assert round(self.asme.get_safe_pressure()) == 1036  # 1037
        assert round(self.asme.defect_max_length(), 3) == 4.789  # INFINITY ?

        self.defect.depth = 0.167
        assert round(self.asme.defect_max_length(), 3) == 3.557  # 30.0

    def test_example4(self):
        """Example 4."""
        self.pipe.diameter = 24
        self.pipe.wallthickness = 0.432
        self.defect.depth = 0.3
        self.defect.length = 30.0
        self.pipe.maop = 910

        assert round(self.asme.get_a(self.defect.length), 3) == 7.668  # 8.320
        assert round(self.asme.get_design_pressure()) == 1348
        assert round(self.asme.get_safe_pressure()) == 453
        assert round(self.asme.defect_max_length(), 3) == 1.907  # 12.867

        assert self.asme.pipe_state() == self.state.Repair
        assert round(self.asme.safe_pressure) == 453

        self.pipe.maop = 452
        assert self.asme.pipe_state() == self.state.Defected

    def test_example5(self):
        """Example 5."""
        self.pipe.diameter = 24
        self.pipe.wallthickness = 0.281
        self.defect.depth = 0.08
        self.defect.length = 15.0
        self.pipe.maop = 731

        assert round(self.asme.get_a(self.defect.length), 3) == 4.754  # 5.158
        assert round(self.asme.get_design_pressure()) == 877
        assert round(self.asme.get_safe_pressure()) == 690

        assert self.asme.pipe_state() == self.state.Repair
        assert round(self.asme.safe_pressure) == 690

    def test_example6(self):
        """Example 6."""
        self.pipe.maop = 1000
        self.pipe.diameter = 36
        self.pipe.wallthickness = 0.5
        self.defect.depth = 0.41
        self.defect.length = 100.0

        assert self.asme.is_replace
        assert self.asme.pipe_state() == self.state.Replace

    def test_example7(self):
        """Example 7."""
        self.pipe.maop = 877
        self.pipe.diameter = 12.625
        self.pipe.wallthickness = 0.5
        self.pipe.material.yield_strength = 35000
        self.asme.design_factor = 0.4
        self.defect.depth = 0.035
        self.defect.length = 3.0

        assert self.asme.is_ok
        assert self.asme.pipe_state() == self.state.Ok

    def test_example8(self):
        """Example 8."""
        self.pipe.diameter = 24
        self.pipe.wallthickness = 0.5
        self.pipe.material.yield_strength = 42000
        self.asme.design_factor = 0.5
        self.defect.depth = 0.125
        self.defect.length = 12.0
        self.pipe.maop = 790

        assert round(self.asme.get_a(self.defect.length), 3) == 2.851  # 3.093


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
        assert asme_b31g.pipe_state() == State.Safe

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

    def test_lang(self):
        """Function defect_max_length."""
        from pipeline_integrity.i18n import Lang
        from pipeline_integrity.method.asme_b31g import Context

        asme = Context(self.pipe.add_metal_loss(10, 100, 10, 20, 1.5))
        assert len(asme.lang(Lang.Ru)) == 23
