"""ASME B31G method for metal loss defects edition 2012."""
import math

from ... import Error as ErrorBase
from . import Context as ContextBase


class ErrMaterialSMTSNotDefined(ErrorBase):
    """SMTS not defined for material of the pipe."""


class Context(ContextBase):
    """Context of the ASME B31G method edition 2012."""

    name = "ASME B31G 2012"

    def __init__(self, defect):
        """Check for defined material SMTS."""
        if defect.pipe.material.smts is None:
            raise ErrMaterialSMTSNotDefined("SMTS not defined for material of the pipe.")

        super(Context, self).__init__(defect)

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

    def s_flow(self):
        """Return S_flow."""
        material = self.anomaly.pipe.material
        s_f = 1.1 * material.smys
        if s_f > material.smts:
            return material.smts

        return s_f

    def get_stress_fail(self):
        """Return estimated failure stress level."""
        s_f = self.s_flow()

        if self.z_param <= 20:
            v23 = 2.0 / 3.0
            tmp1 = 1 - v23 * self.relative_depth
            tmp2 = 1 - v23 * self.relative_depth / self.m_param
            s_p = s_f * (tmp1 / tmp2)
            return s_p

        s_p = s_f * (1 - self.relative_depth)
        return s_p

    def get_press_fail(self):
        """Return estimated failure pressure."""
        s_f = self.get_stress_fail()
        p_f = 2 * s_f * self.relative_depth
        return p_f

    def erf(self):
        """Return estimated repair factor."""
        return self.get_press_fail() / self.anomaly.pipe.maop
