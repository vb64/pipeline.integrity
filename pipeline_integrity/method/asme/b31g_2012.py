"""ASME B31G method for metal loss defects edition 2012."""
import math

from . import Context as ContextBase


class Context(ContextBase):
    """Context of the ASME B31G method edition 2012."""

    name = "ASME B31G 2012"

    @property
    def relative_depth(self):
        """Return relative depth to wall thickness."""
        r_d = float(self.anomaly.depth) / self.anomaly.pipe.wallthickness
        return r_d

    @property
    def z_param(self):
        """Parameter z."""
        pipe = self.anomaly.pipe
        z_val = math.pow(self.anomaly.length, 2) / (pipe.diameter * pipe.wallthickness)
        return z_val

    @property
    def m_param(self):
        """Parameter M."""
        m_val = math.sqrt((1 + 0.8 * self.z_param))
        return m_val

    def get_safe_pressure(self):
        """Return acceptable pressure level."""
        press_flow = 1.1 * self.anomaly.pipe.material.yield_strength
        v23 = 2.0 / 3.0

        if self.z_param <= 20:
            tmp1 = 1 - v23 * self.relative_depth
            tmp2 = 1 - v23 * self.relative_depth / self.m_param
            s_p = press_flow * (tmp1 / tmp2)
            return s_p

        s_p = press_flow * (1 - self.relative_depth)
        return s_p
