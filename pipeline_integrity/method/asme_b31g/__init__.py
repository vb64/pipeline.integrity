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
        """New defect."""
        super().__init__(defect)
        self.safe_pressure = None

    @property
    def relative_depth(self):
        """Return defect depth as percent from pipe wall thickness."""
        return 100.0 * self.anomaly.depth / self.anomaly.pipe.wallthickness

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
            if self.defect_max_length() > self.anomaly.length:
                result = State.Safe
            else:
                self.safe_pressure = self.get_safe_pressure(self.anomaly.length)
                if self.safe_pressure > self.anomaly.pipe.maop:
                    result = State.Defected

        return result

    def get_b(self):
        """Parameter B from method description."""
        b_max = 4.0
        if self.relative_depth < 17.5:
            return b_max

        rel = self.relative_depth / 100.0
        b_val = math.sqrt(math.pow(rel / (1.1 * rel - 0.15), 2) - 1)
        # if b_val > b_max:
        #     return b_max

        return b_val

    def get_a(self, max_length):
        """Parameter A from method description."""
        return 0.823 * max_length / self.diam_wall

    @property
    def diam_wall(self):
        """Intermediate parameter."""
        pipe = self.anomaly.pipe
        return math.sqrt(pipe.diameter * pipe.wallthickness)

    def defect_max_length(self):
        """Return maximum allowable longitudinal extent of corrosion."""
        return 1.12 * self.get_b() * self.diam_wall

    def get_design_pressure(self):
        """Return design pressure."""
        pipe = self.anomaly.pipe
        smys = pipe.material.yield_strength

        return 2.0 * smys * pipe.wallthickness * self.design_factor * self.temperature_factor / pipe.diameter

    def get_safe_pressure(self, max_length):
        """Return acceptable pressure level."""
        a_val = self.get_a(max_length)
        p_val = self.get_design_pressure()
        d_t = self.relative_depth / 100.0
        tmp = 1.1 * p_val

        if a_val > 4.0:
            p_s = tmp * (1 - d_t)
        else:
            v23 = 2.0 / 3.0
            a_pow = math.sqrt(math.pow(a_val, 2) + 1)
            p_s = tmp * ((1 - v23 * d_t) / (1 - v23 * d_t / a_pow))

        if p_s > p_val:
            return p_val

        return p_s
