"""ASME B31G method for metal loss defects.

https://pypi.org/project/pyintegrity/
https://github.com/novanumeric/WebIntegrity
https://edu.truboprovod.ru/kbase/doc/start/WebHelp_ru/ASMEB31G.htm
"""
from .. import Context as ContextBase
from ...defect import Type

DEPTH_OK_PERCENT = 10
DEPTH_CRITICAL_PERCENT = 80


class State:
    """State of pipe with defect."""

    Ok = 0
    Replace = 1
    Defected = 2


class Context(ContextBase):
    """Context of the ASME B31G method."""

    valid_defect_types = [Type.MetalLoss]
    name = "ASME B31G"
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
