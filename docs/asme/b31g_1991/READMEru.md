# Методика ASME B31G редакция 1991 года

[На английском](README.md)

Контекст для вычисления степени опасности дефекта по методике ASME B31G 1991.

```python
from pipeline_integrity.method.asme.b31g_1991 import Context

asme = Context(defect)
```

Глубина дефекта менее 10% толщины стенки трубы, опасности нет.

```python
from pipeline_integrity.method.asme.b31g_1991 import State

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

from pipeline_integrity.i18n import Lang

lang_ru = asme.lang(Lang.Ru)
assert asme.pipe_state(is_explain=lang_ru) == State.Defected
```

Если метод `pipe_state` вызван с параметром `is_explain`, задающим словарь перевода,
то вы можете получить объяснение сделанного расчета в текстовом виде на русском языке.

```python
asme.explain()
```

```text
Относительная глубина дефекта == глубина / толщина стенки  * 100%.
8 / 16 * 100 = 50.0
Расчет максимально допустимой длины дефекта.
Параметр B.
Относительная глубина дефекта 50.0 больше 17.5%.
B = sqrt(pow(0.5 / (1.1 * 0.5 - 0.15), 2) - 1) = 0.75
L = 1.12 * B * sqrt(diameter * wallthickness)L = 1.12 * 0.75 * sqrt(1420 * 16) = 126.615
Длина дефекта 500 превышает максимально допустимую длину 126.615.
Необходимо рассчитать допустимое давление для дефекта.
Расчет максимально допустимого давления.
Параметр A для дефекта длиной 500.
A = 0.823 * defect_length / sqrt(diameter * wallthickness)
A = 0.823 * 500 / sqrt(1420 * 16) = 2.73
Расчетное давление.
Design_press = 2 * material_smys * wallthickness * design_factor * temperature_factor / diam.
Design_press = 2 * 295 * 16 * 0.72 * 1 / 1420 = 4.786.
Параметр A меньше 4.
a_pow = sqrt(pow(a_param, 2) + 1).
a_pow = sqrt(pow(2.73, 2) + 1) = 2.907.
Safe_press = 1.1 * design_press * ((1 - 2/3 * rel_depth) / (1 - 2/3 * rel_depth / a_pow)).
Safe_press = 1.1 * 4.786 * ((1 - 2/3 * 0.5) / (1 - 2/3 * 0.5 / 2.907)) = 3.965.
Используем безопасное давление как максимально допустимое давление.
Рабочее давление 3.95 не превышает допустимое давление 3.965.
Дефект не опасен.
```
