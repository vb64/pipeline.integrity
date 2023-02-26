# ASME B31G edition 1991

[In Russian](READMEru.md)

Context for calculating the degree of severity of the defect according to the ASME B31G method edition 1991.

```python
from pipeline_integrity.method.asme.b31g_1991 import Context

asme = Context(defect)
```

Defect depth less than 10% wall thickness, no danger.

```python
from pipeline_integrity.method.asme.b31g_1991 import State

assert defect.depth == 0.039
assert pipe.wallthickness == 0.63
assert asme.pipe_state() == State.Ok
```

The depth of the defect is more than 80% of the pipe wall thickness, repair or replacement of the pipe is necessary.

```python
defect.depth = 0.6
assert asme.pipe_state() == State.Replace
```

The depth of the defect is 50% of the pipe wall thickness, but the length of the defect
does not exceed its maximum allowable length.
The defect is not dangerous.

```python
defect.depth = 0.31
assert defect.length == 4
assert round(asme.defect_max_length()) == 5
assert asme.pipe_state() == State.Safe
```

A defect with a length of 20 inches and a depth of 50% of the pipe wall thickness
requires repair at the specified working pressure in the pipe.

```python
defect.length = 20
assert asme.pipe_state() == State.Repair
```

When the operating pressure is reduced to a safe value, the defect does not require repair.

```python
assert pipe.maop == 900
assert round(asme.safe_pressure, 2) == 700.68
pipe.maop = 700
assert asme.pipe_state(is_explain=True) == State.Defected
```

If you call `pipe_state` method with parameter `is_explain=True`,
then you can get explanation in text form.

```python
asme.explain()
```

```text
The relative defect depth == defect depth / pipe wall thickness * 100%.
0.31 / 0.63 * 100 = 49.206
Calculation of the maximum allowable defect length.
Parameter B.
The relative defect depth 49.206 more than 17.5%.
B = sqrt(pow(0.492 / (1.1 * 0.492 - 0.15), 2) - 1) = 0.763
L = 1.12 * B * sqrt(diameter * wallthickness)L = 1.12 * 0.763 * sqrt(56 * 0.63) = 5.073
The length of the defect 20 exceed the maximum allowable length 5.073.
It is necessary to calculate the allowable pressure for defect.
Calculation of the maximum allowable pressure.
Parameter A for defect length 20.
A = 0.823 * defect_length / sqrt(diameter * wallthickness)
A = 0.823 * 20 / sqrt(56 * 0.63) = 2.771
Design pressure.
Design_press = 2 * material_smys * wallthickness * design_factor * temperature_factor / diam.
Design_press = 2 * 52000 * 0.63 * 0.72 * 1 / 56 = 842.4.
Parameter A less than 4.
a_pow = sqrt(pow(a_param, 2) + 1).
a_pow = sqrt(pow(2.771, 2) + 1) = 2.946.
Safe_press = 1.1 * design_press * ((1 - 2/3 * rel_depth) / (1 - 2/3 * rel_depth / a_pow)).
Safe_press = 1.1 * 842.4 * ((1 - 2/3 * 0.492) / (1 - 2/3 * 0.492 / 2.946)) = 700.683.
Use safe pressure 700.683 as maximum allowable pressure.
The working pressure 700 does not exceed the allowable pressure 700.683.
The defect is not dangerous.
```
