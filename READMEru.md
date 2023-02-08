# Библиотека PipelineIntegrity

[На английском](README.md)

Бесплатная, с открытым исходным кодом библиотека PipelineIntegrity
предназначена для расчета степени опасности дефектов потери металла трубопровода
по методике ASME B31G.

## Установка

```bash
pip install pipeline-integrity
```

## Использование

Материал с указанным пределом текучести.

```python
from pipeline_integrity.material import Material

material = Material("Сталь", 52000)
```

Труба из указанного материала под давлением, с длиной, диаметром и толщиной стенки.

```python
from pipeline_integrity.pipe import Pipe

length = 11200
diameter = 1420
wall_thickness = 16
work_pressure = 900

pipe = Pipe(length, diameter, wall_thickness, material, work_pressure)
```

Дефект потери металла с указанным положением на трубе и заданной глубиной.

```python
start = 1000  # дефект начинается на расстоянии 1 метра от начала трубы
length = 100  # длина дефекта 100 мм
orient_start = 10  # по окружности трубы дефект начинается на 10 угловых минут от верхней точки трубы
orient_length = 20  # размер дефекта по окружности составляет 20 угловых минут
depth = 1  # глубина дефекта 1 мм

defect = pipe.add_metal_loss(start, length, orient_start, orient_length, depth)
```

Контекст для вычисления степени опасности дефекта по методике ASME B31G.

```python
from pipeline_integrity.method.asme_b31g import Context

asme = Context(defect)
```
