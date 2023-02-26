"""ASME B31G method for metal loss defects edition 2012.

https://edu.truboprovod.ru/kbase/doc/start/WebHelp_ru/ASMEB31G.htm
"""
import math

from ...i18n import fake_gettext as _
from ... import Error as ErrorBase
from . import Context as ContextBase, EXPL_ROUND


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
        z_val = pow(self.anomaly.length, 2) / (pipe.diameter * pipe.wallthickness)
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
        d_t = self.relative_depth

        if self.z_param <= 20:
            v23 = 2.0 / 3.0
            m_val = self.m_param
            s_p = s_f * (1 - v23 * d_t) / (1 - v23 * d_t / m_val)
            return s_p

        s_p = s_f * (1 - d_t)
        return s_p

    def get_stress_fail_mod(self):
        """Return estimated failure stress level by modified method."""
        s_f = self.s_flow()
        d_t = self.relative_depth
        z_val = self.z_param

        if z_val <= 50:
            m_val = math.sqrt(1 + 0.6275 * z_val - 0.003375 * pow(z_val, 2))
        else:
            m_val = 0.032 * z_val + 3.3

        s_p = s_f * (1 - 0.85 * d_t) / (1 - 0.85 * d_t / m_val)
        return s_p

    def get_press_fail(self, is_mod=False):
        """Return estimated failure pressure."""
        if is_mod:
            s_f = self.get_stress_fail_mod()
        else:
            s_f = self.get_stress_fail()

        p_f = 2 * s_f * self.relative_depth
        return p_f

    def erf(self, is_mod=False, is_explain=False):
        """Return estimated repair factor."""
        self.is_explain = is_explain
        self.explain_text = []

        modname = _("modified", self) if is_mod else _("classic", self)

        self.add_explain([
          _("Calculate ERF by {} {}.", self).format(self.name, modname),
        ])

        press_fail = self.get_press_fail(is_mod=is_mod)
        erf_val = self.anomaly.pipe.maop / press_fail

        self.add_explain([
          '\n', _("ERF = pipe_maop / press_fail.", self),
          '\n', "{} / {} = {}".format(
             self.anomaly.pipe.maop, round(press_fail, EXPL_ROUND), round(erf_val, EXPL_ROUND)
          ),
        ])

        return erf_val
