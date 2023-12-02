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

При создании контекста для вычисления степени опасности дефекта по методике ASME B31G
нужно задать предел прочности на растяжение материала трубы.

```python
from pipeline_integrity.method.asme.b31g_2012 import Context

pipe.material.smts = 420
asme = Context(defect)
```

Глубина дефекта менее 10% толщины стенки трубы, рассчитанный КБД (ERF) дефекта менее 1, опасности нет.

```python
assert defect.depth == 1
assert pipe.wallthickness == 16
assert 0.95 < asme.erf() < 0.97
assert asme.years() > 1
```

Для случаев очень низкого давления ремонт не требуется никогда (специальное значение REPAIR_NOT_REQUIRED=777).

```python
pipe.maop = 0.01
assert asme.years() == asme.REPAIR_NOT_REQUIRED
```

Глубина дефекта 50% от толщины стенки трубы требует ремонта при указанном рабочем давлении в трубе (КБД > 1).

```python
pipe.maop = 7
defect.depth = 8
defect.length = 200
assert asme.years() == 0
assert asme.erf() > 1
```

При снижении рабочего давления до безопасной величины дефект не требует ремонта.

```python
assert pipe.maop == 7
assert round(asme.safe_pressure, 2) > 6
pipe.maop = asme.safe_pressure - 0.1

from pipeline_integrity.i18n import Lang

asme.is_explain = asme.lang(Lang.Ru)
assert asme.years() > 0
```

Если в свойстве контекста `is_explain` задать словарь перевода,
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
Z = 200^2 / (1420 * 16) = 1.761.
Параметр M = sqrt(1 + 0.8 * Z).
M = sqrt(1 + 0.8 * 1.761) = 1.552.
Параметр Z = 1.761 <= 20.
Напряжение разрыва = Sflow * (1 - 2/3 * (глубина / толщина)) / (1 - 2/3 * (глубина / толщина) / M).
stress_fail = 324.5 * (1 - 2/3 * (8 / 16)) / (1 - 2/3 * (8 / 16 / 1.552)) = 275.509.
Давление разрыва = 2 * stress_fail * толщина / диаметр.
press_fail = 2 * 275.509 * 16 / 1420 = 6.209.
КБД = рабочее_давление / давление_разрыва.
ERF = 6.108663279971968 / 6.209 = 0.984

На данный момент ремонт не требуется, вычисляем время до ремонта.
При скорости коррозии 0.4 мм/год, толщине стенки 16 и глубине дефекта 8, сквозной дефект образуется через лет: 21.
Вычисляем через сколько лет дефект потребует ремонта при заданной скорости коррозии.
Года: 1 КБД: 0.995.
Года: 2 КБД: 1.007.
Дефект нужно будет отремонтировать через лет: 1.
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

## Пример

Рабочая версия примера онлайн-калькулятора опасности дефекта с использованием этой библиотеки [находится здесь](https://wot-online-hours.appspot.com/).
Исходный код примера содержится в [каталоге example](example/web/gae ) репозитария.