# Библиотека PipelineIntegrity

[На английском](README.md)

Бесплатная, с открытым исходным кодом библиотека PipelineIntegrity
предназначена для расчета степени опасности дефектов потери металла трубопровода
по [методике ASME B31G](https://law.resource.org/pub/us/cfr/ibr/002/asme.b31g.1991.pdf).

![методика ASME B31G](pipeline_integrity/method/asme_b31g/img/fig_1_1.png)

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

Контекст для вычисления степени опасности дефекта по методике ASME B31G.

```python
from pipeline_integrity.method.asme_b31g import Context

asme = Context(defect)
```

Глубина дефекта менее 10% толщины стенки трубы, опасности нет.

```python
from pipeline_integrity.method.asme_b31g import State

assert defect.depth == 1
assert pipe.wallthickness == 16
assert asme.pipe_state() == State.Ok
```

Глубина дефекта более 80% толщины стенки трубы, необходим ремонт или замена трубы.

```python
defect.depth = 15
assert asme.pipe_state() == State.Replace
```

Глубина дефекта 50% от толщины стенки трубы, но длина дефекта не превышает его максимально допустимую длину.
Дефект не представляет опасности.

```python
defect.depth = 8
assert defect.length == 100
assert round(asme.defect_max_length()) == 127
assert asme.pipe_state() == State.Safe
```

Дефект длиной 500 мм и глубиной 50% от толщины стенки трубы требует ремонта при указанном рабочем давлении в трубе.

```python
defect.length = 500
assert asme.pipe_state() == State.Repair
```

При снижении рабочего давления до безопасной величины дефект не требует ремонта.

```python
assert pipe.maop == 7
assert round(asme.safe_pressure, 2) == 3.96
pipe.maop = 3.95
assert asme.pipe_state() == State.Defected
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
