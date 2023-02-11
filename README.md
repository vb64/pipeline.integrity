# PipelineIntegrity library
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/pipeline.integrity/pep257.yml?label=Pep257&style=plastic&branch=main)](https://github.com/vb64/pipeline.integrity/actions?query=workflow%3Apep257)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/pipeline.integrity/py2.yml?label=Python%202.7&style=plastic&branch=main)](https://github.com/vb64/pipeline.integrity/actions?query=workflow%3Apy2)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/pipeline.integrity/py3.yml?label=Python%203.7-3.10&style=plastic&branch=main)](https://github.com/vb64/pipeline.integrity/actions?query=workflow%3Apy3)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/73597c448da3417599eb3f21bcb7136b)](https://www.codacy.com/gh/vb64/pipeline.integrity/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/pipeline.integrity&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/73597c448da3417599eb3f21bcb7136b)](https://www.codacy.com/gh/vb64/pipeline.integrity/dashboard?utm_source=github.com&utm_medium=referral&utm_content=vb64/pipeline.integrity&utm_campaign=Badge_Coverage)

[In Russian](READMEru.md)

Free, open source PipelineIntegrity library designed to calculate the degree of danger
of pipeline metal loss defects according to the [ASME B31G method](https://law.resource.org/pub/us/cfr/ibr/002/asme.b31g.1991.pdf).

![ASME B31G method](pipeline_integrity/method/asme_b31g/img/fig_1_1.png)

## Installation

```bash
pip install pipeline-integrity
```

## Usage

A pipe under pressure, with a length, diameter and wall thickness from specified material.

```python
from pipeline_integrity.material import Material
from pipeline_integrity.pipe import Pipe

pipe = Pipe(
  440,  # length, inches
  56,  # diameter, inches
  0.63,  # wall thickness, inches
  Material(  # pipe material
    "Steel",
    52000  # SMYS, psi
  ),
  900  # pressure, psi
)
)
```

Metal loss defect with a specified position on the pipe and a specified depth.

```python
defect = pipe.add_metal_loss(
  40,  # the defect starts at a distance of 40 inches from the beginning of the pipe
  4,  # defect length 4 inches
  10,  # along the circumference of the pipe, the defect begins
       # at 10 arc minutes from the top of the pipe
  20,  # the size of the defect along the circumference is 20 arc minutes
  0.039  # defect depth 0.039 inches
)
```

Context for calculating the degree of severity of the defect according to the ASME B31G method

```python
from pipeline_integrity.method.asme_b31g import Context

asme = Context(defect)
```

Defect depth less than 10% wall thickness, no danger.

```python
from pipeline_integrity.method.asme_b31g import State

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
assert asme.pipe_state() == State.Defected
```

## Development

```
$ git clone git@github.com:vb64/pipeline.integrity.git
$ cd pipeline.integrity
```
With Python 3:
```
$ make setup PYTHON_BIN=/path/to/python3
$ make tests
```
With Python 2:
```
$ make setup2 PYTHON_BIN=/path/to/python2
$ make tests2
```
