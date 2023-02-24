"""ASME B31G method for metal loss defects edition 2012."""
import math

from . import Context as ContextBase


class Context(ContextBase):
    """Context of the ASME B31G method edition 2012."""

    name = "ASME B31G 2012"

    @property
    def relative_depth(self):
        """Return relative depth to wall thickness."""
        return float(self.anomaly.depth) / self.anomaly.pipe.wallthickness

    @property
    def z_param(self):
        """Parameter z."""
        pipe = self.anomaly.pipe
        return math.pow(self.anomaly.length, 2) / (pipe.diameter * pipe.wallthickness)

    @property
    def m_param(self):
        """Parameter M."""
        return math.sqrt((1 + 0.8 * self.z_param))

    def get_safe_pressure(self):
        """Return acceptable pressure level."""
        press_flow = 1.1 * self.anomaly.pipe.material.yield_strength
        v23 = 2.0 / 3.0

        if self.z_param <= 20:
            tmp1 = 1 - v23 * self.relative_depth
            tmp2 = 1 - v23 * self.relative_depth / self.m_param
            return press_flow * (tmp1 / tmp2)

        return press_flow * (1 - self.relative_depth)
