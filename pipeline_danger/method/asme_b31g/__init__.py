"""ASME B31G method for metal loss defects.

https://pypi.org/project/pyintegrity/
https://github.com/novanumeric/WebIntegrity
https://edu.truboprovod.ru/kbase/doc/start/WebHelp_ru/ASMEB31G.htm
"""
import math

from .. import Context as ContextBase
from ...defect import Type

DEPTH_OK_PERCENT = 10
DEPTH_CRITICAL_PERCENT = 80


class State:
    """State of pipe with defect."""

    Ok = 0
    Safe = 1
    Defected = 2
    Repair = 3
    Replace = 100


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
    def is_ok(self):
        """Return True if state is ok."""
        return self.relative_depth <= DEPTH_OK_PERCENT

    @property
    def is_replace(self):
        """Return True if state is replace."""
        return self.relative_depth >= DEPTH_CRITICAL_PERCENT

    def pipe_state(self, is_explain=False):
        """Return state for defected pipe."""
        self.is_explain = is_explain
        self.explain_text = []

        result = State.Repair

        if self.is_ok:
            result = State.Ok
        elif self.is_replace:
            result = State.Replace
        else:
            length = self.defect_max_length()
            if length <= self.anomaly.length:
                result = State.Safe
            else:
                p_s = 666
                if p_s < self.anomaly.pipe.maop:
                    result = State.Defected

        return result

    def get_b(self):
        """Parameter B from method description."""
        if self.relative_depth < 17.5:
            return 4.0

        rel = self.relative_depth / 100.0

        return math.sqrt(math.pow(rel / (1.1 * rel - 0.15), 2) - 1)

    def defect_max_length(self):
        """Return maximum allowable longitudinal extent of corrosion."""
        pipe = self.anomaly.pipe
        return 1.12 * self.get_b() * math.sqrt(pipe.diameter * pipe.wallthickness)
