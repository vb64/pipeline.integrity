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
assert asme.pipe_state(is_explain=True) == State.Defected
```

Если метод `pipe_state` вызван с параметром `is_explain=True`,
то вы можете получить объяснение сделанного расчета в текстовом виде (на английском).

```python
asme.explain()
```

```text
The relative defect depth == defect depth / pipe wall thickness * 100%.
8 / 16 * 100 = 50.0
Calculation of the maximum allowable defect length.
Parameter B.
The relative defect depth 50.0 more than 17.5%.
B = sqrt(pow(0.5 / (1.1 * 0.5 - 0.15), 2) - 1) = 0.75
L = 1.12 * B * sqrt(diameter * wallthickness)L = 1.12 * 0.75 * sqrt(1420 * 16) = 126.615
The length of the defect 500 exceed the maximum allowable length 126.615.
It is necessary to calculate the allowable pressure for defect.
Calculation of the maximum allowable pressure.
Parameter A for defect length 500.
A = 0.823 * defect_length / sqrt(diameter * wallthickness)
A = 0.823 * 500 / sqrt(1420 * 16) = 2.73
Design pressure.
Design_press = 2 * material_smys * wallthickness * design_factor * temperature_factor / diam.
Design_press = 2 * 295 * 16 * 0.72 * 1 / 1420 = 4.786.
Parameter A less than 4.
a_pow = sqrt(pow(a_param, 2) + 1).
a_pow = sqrt(pow(2.73, 2) + 1) = 2.907.
Safe_press = 1.1 * design_press * ((1 - 2/3 * rel_depth) / (1 - 2/3 * rel_depth / a_pow)).
Safe_press = 1.1 * 4.786 * ((1 - 2/3 * 0.5) / (1 - 2/3 * 0.5 / 2.907)) = 3.965.
Use safe pressure 3.965 as maximum allowable pressure.
The working pressure 3.95 does not exceed the allowable pressure 3.965.
The defect is not dangerous.
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
