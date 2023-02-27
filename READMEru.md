# Библиотека PipelineIntegrity

[На английском](README.md)

Бесплатная, с открытым исходным кодом библиотека PipelineIntegrity
предназначена для расчета степени опасности дефектов потери металла трубопровода
по методике ASME B31G.

![методика ASME B31G](docs/asme/img/fig_1_1.png)

## Установка

```bash
pip install pipeline-integrity
```

## Использование

Труба под давлением, с длиной, диаметром и толщиной стенки из указанного материала.

```python
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
```

Дефект потери металла с указанным положением на трубе и заданной глубиной.

```python
defect = pipe.add_metal_loss(
  1000,  # дефект начинается на расстоянии 1 метра от начала трубы
  100,  # длина дефекта 100 мм
  10,  # по окружности трубы дефект начинается на 10 угловых минут от верхней точки трубы
  20,  # размер дефекта по окружности составляет 20 угловых минут
  1  # глубина дефекта 1 мм
)
```

Нужно задать предел прочности на растяжение материала трубы.

```python
pipe.material.smts = 420
```

Контекст для вычисления степени опасности дефекта по методике ASME B31G.

```python
from pipeline_integrity.method.asme.b31g_2012 import Context

asme = Context(defect)
```

Глубина дефекта менее 10% толщины стенки трубы, рассчитанный КБД (ERF) дефекта менее 1, опасности нет.

```python
assert defect.depth == 1
assert pipe.wallthickness == 16
assert 0.96 < asme.erf() < 0.97
```

Глубина дефекта 50% от толщины стенки трубы требует ремонта при указанном рабочем давлении в трубе (КБД > 1).

```python
defect.depth = 8
assert defect.length == 100
assert asme.erf() > 1
```

При снижении рабочего давления до безопасной величины дефект не требует ремонта.

```python
assert pipe.maop == 7
assert round(asme.safe_pressure, 2) == 6.83
pipe.maop = 6.8

from pipeline_integrity.i18n import Lang

lang_ru = asme.lang(Lang.Ru)

assert asme.erf(is_explain=lang_ru) < 1
```

Если метод `erf` вызван с параметром `is_explain`, задающим словарь перевода,
то вы можете получить объяснение сделанного расчета в текстовом виде на русском языке.

```python
asme.explain()
```

```text
Вычисляем КБД по ASME B31G 2012 классический.
Вычисляем величину напряжения разрыва классическим методом.
Параметр Sflow = 1.1 * предел_текучести.
Sflow = 1.1 * 295 = 324.5.
Параметр Z = длина^2 / (диаметр * толщина).
Z = 100^2 / (1420 * 16) = 0.44.
Параметр M = sqrt(1 + 0.8 * Z).
M = sqrt(1 + 0.8 * 0.44) = 1.163.
Параметр Z = 0.44 <= 20.
Напряжение разрыва = Sflow * (1 - 2/3 * (глубина / толщина)) / (1 - 2/3 * (глубина / толщина) / M).
stress_fail = 324.5 * (1 - 2/3 * (8 / 16)) / (1 - 2/3 * (8 / 16 / 1.163)) = 303.27.
Давление разрыва = 2 * stress_fail * толщина / диаметр.
press_fail = 2 * 303.27 * 16 / 1420 = 6.834.
КБД = рабочее_давление / давление_разрыва.
ERF = 6.8 / 6.834 = 0.995
```

## Разработка

```
$ git clone git@github.com:vb64/pipeline.integrity.git
$ cd pipeline.integrity
```
С Python 3:
```
$ make setup PYTHON_BIN=/path/to/python3
$ make tests
```
С Python 2:
```
$ make setup2 PYTHON_BIN=/path/to/python2
$ make tests2
```
