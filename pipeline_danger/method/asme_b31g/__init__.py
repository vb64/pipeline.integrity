"""ASME B31G method for metal loss defects.

https://pypi.org/project/pyintegrity/
https://github.com/novanumeric/WebIntegrity
https://edu.truboprovod.ru/kbase/doc/start/WebHelp_ru/ASMEB31G.htm
"""
import math

from .. import Context as ContextBase
from ...defect import Type
from ... import Error as ErrorBase

DEPTH_OK_PERCENT = 10
DEPTH_CRITICAL_PERCENT = 80


class ErrNotCalc(ErrorBase):
    """Defect not need calculation."""


class State:
    """State of pipe with defect."""

    Ok = 0
    Replace = 1
    Defected = 2


class Context(ContextBase):
    """Context of the ASME B31G method."""

    name = "ASME B31G"
    valid_defect_types = [Type.MetalLoss]
    design_factor = 0.72  # DesignFactors.md
    temperature_factor = 1

    def __init__(self, defect):
        """New context ASME B31G."""
        super().__init__(defect)
        self.relative_depth = 100.0 * self.anomaly.depth / self.anomaly.pipe.wallthickness

    @property
    def pipe_state(self):
        """Return state for defected pipe."""
        result = State.Defected
        if self.relative_depth <= DEPTH_OK_PERCENT:
            result = State.Ok
        elif self.relative_depth >= DEPTH_CRITICAL_PERCENT:
            result = State.Replace

        return result

    def get_b(self):
        """Parameter B from method description."""
        if self.relative_depth < 17.5:
            return 4.0

        rel = self.relative_depth / 100.0

        return math.sqrt(math.pow(rel / (1.1 * rel - 0.15), 2) - 1)

    def defect_max_length(self):
        """Return maximum allowable longitudinal extent of corrosion."""
        if self.pipe_state != State.Defected:
            raise ErrNotCalc("Maximum allowable longitudinal extent not applied.")

        pipe = self.anomaly.pipe

        return 1.12 * self.get_b() * math.sqrt(pipe.diameter * pipe.wallthickness)
