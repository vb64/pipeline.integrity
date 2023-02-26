# -*- coding: utf-8 -*-
"""Root class for testing ASME methods."""
from .. import TestMethod


class TestAsme(TestMethod):
    """Base class for tests ASME methods."""

    def setUp(self):
        """Set up test data."""
        super(TestAsme, self).setUp()

        from pipeline_integrity.material import Material
        from pipeline_integrity.pipe import Pipe

        self.pipe_en = Pipe(
          440,  # length inches
          56,  # diameter 56 inches
          0.63,  # wall thickness inches
          Material(  # pipe material
            "Steel",
            52000  # SMYS psi
          ),
          900  # pressure psi
        )

        self.defect_en = self.pipe_en.add_metal_loss(
          40,  # the defect starts at a distance of 40 inches from the beginning of the pipe
          4,  # defect length 4 inches
          10,  # along the circumference of the pipe, the defect begins
               # at 10 arc minutes from the top of the pipe
          20,  # the size of the defect along the circumference is 20 arc minutes
          0.039  # defect depth 0.039 inches
        )

        self.pipe_ru = Pipe(
          11200,  # длина 11.2 метра
          1420,  # диаметр 1420 мм
          16,  # толщина стенки 16 мм
          Material(  # материал трубы
            "Сталь",
            295  # предел текучести Мпа
          ),
          7  # рабочее давление Мпа
        )

        self.defect_ru = self.pipe_ru.add_metal_loss(
          1000,  # дефект начинается на расстоянии 1 метра от начала трубы
          100,  # длина дефекта 100 мм
          10,  # по окружности трубы дефект начинается на 10 угловых минут от верхней точки трубы
          20,  # размер дефекта по окружности составляет 20 угловых минут
          1  # глубина дефекта 1 мм
        )
