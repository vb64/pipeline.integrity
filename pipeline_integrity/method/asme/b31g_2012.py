"""ASME B31G method for metal loss defects edition 2012."""
import math

from . import Context as ContextBase


class Context(ContextBase):
    """Context of the ASME B31G method edition 2012."""

    name = "ASME B31G 2012"

    @property
    def z_param(self):
        """Parameter z."""
        pipe = self.anomaly.pipe
        return math.pow(self.anomaly.length, 2) / (pipe.diameter * pipe.wallthickness)
