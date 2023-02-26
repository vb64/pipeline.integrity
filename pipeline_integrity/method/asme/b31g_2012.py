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
        return float(self.anomaly.depth) / self.anomaly.pipe.wallthickness

    @property
    def z_param(self):
        """Parameter z."""
        pipe = self.anomaly.pipe
        z_val = pow(self.anomaly.length, 2) / (pipe.diameter * pipe.wallthickness)

        self.add_explain([
          '\n', _("Parameter Z = length^2 / (diameter * wallthickness).", self),
          '\n', _("Z = {}^2 / ({} * {}) = {}.", self).format(
            round(self.anomaly.length, EXPL_ROUND),
            round(pipe.diameter, EXPL_ROUND),
            round(pipe.wallthickness, EXPL_ROUND),
            round(z_val, EXPL_ROUND),
          ),
        ])

        return z_val

    @property
    def m_param(self):
        """Parameter M."""
        z_val = self.z_param
        m_val = math.sqrt(1 + 0.8 * z_val)

        self.add_explain([
          '\n', _("Parameter M = sqrt(1 + 0.8 * Z).", self),
          '\n', _("M = sqrt(1 + 0.8 * {}) = {}.", self).format(
            round(z_val, EXPL_ROUND),
            round(m_val, EXPL_ROUND),
          ),
        ])

        return m_val

    def s_flow(self):
        """Return S_flow."""
        material = self.anomaly.pipe.material
        s_f = 1.1 * material.smys

        self.add_explain([
          '\n', _("Parameter Sflow = 1.1 * material_smys.", self),
          '\n', _("Sflow = 1.1 * {} = {}.", self).format(
            round(material.smys, EXPL_ROUND),
            round(s_f, EXPL_ROUND),
          ),
        ])

        if s_f > material.smts:

            self.add_explain([
              '\n', _("Parameter Sflow > material SMTS.", self),
              '\n', _("Use material SMTS as Sflow = {}.", self).format(
                round(material.smts, EXPL_ROUND),
              ),
            ])

            return material.smts

        return s_f

    def get_stress_fail(self):
        """Return estimated failure stress level."""
        self.add_explain([
          '\n', _("Calculate failure stress level by the classic way.", self),
        ])

        s_f = self.s_flow()
        d_t = self.relative_depth
        z_val = self.z_param

        if z_val <= 20:
            v23 = 2.0 / 3.0
            m_val = self.m_param
            s_p = s_f * (1 - v23 * d_t) / (1 - v23 * d_t / m_val)

            self.add_explain([
              '\n', _("Parameter Z = {} <= 20.", self).format(round(z_val, EXPL_ROUND)),
              '\n', _(
                "Failure stress level = Sflow * "
                "(1 - 2/3 * (depth / wallthickness)) / "
                "(1 - 2/3 * (depth / wallthickness) / M).",
                self
              ),
              '\n', _("stress_fail = {} * (1 - 2/3 * ({} / {})) / (1 - 2/3 * ({} / {} / {})) = {}.", self).format(
                round(s_f, EXPL_ROUND),
                round(self.anomaly.depth, EXPL_ROUND),
                round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
                round(self.anomaly.depth, EXPL_ROUND),
                round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
                round(m_val, EXPL_ROUND),
                round(s_p, EXPL_ROUND),
              ),
            ])

            return s_p

        s_p = s_f * (1 - d_t)

        self.add_explain([
          '\n', _("Parameter Z = {} > 20.", self).format(round(z_val, EXPL_ROUND)),
          '\n', _("Failure stress level = Sflow * (1 - depth / wallthickness).", self),
          '\n', _("stress_fail = {} * (1 - {} / {}) = {}.", self).format(
            round(s_f, EXPL_ROUND),
            round(self.anomaly.depth, EXPL_ROUND),
            round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
            round(s_p, EXPL_ROUND),
          ),
        ])

        return s_p

    def get_stress_fail_mod(self):
        """Return estimated failure stress level by modified method."""
        self.add_explain([
          '\n', _("Calculate failure stress level by the modified way.", self),
        ])

        s_f = self.s_flow()
        d_t = self.relative_depth
        z_val = self.z_param

        if z_val <= 50:
            m_val = math.sqrt(1 + 0.6275 * z_val - 0.003375 * pow(z_val, 2))
            self.add_explain([
              '\n', _("Parameter Z = {} <= 50.", self).format(round(z_val, EXPL_ROUND)),
              '\n', _("Parameter M = sqrt(1 + 0.6275 * Z - 0.003375 * Z^2)", self),
              '\n', _("M = sqrt(1 + 0.6275 * {} - 0.003375 * {}^2) = {}", self).format(
                round(z_val, EXPL_ROUND),
                round(z_val, EXPL_ROUND),
                round(m_val, EXPL_ROUND),
              ),
            ])
        else:
            m_val = 0.032 * z_val + 3.3
            self.add_explain([
              '\n', _("Parameter Z = {} > 50.", self).format(round(z_val, EXPL_ROUND)),
              '\n', _("Parameter M = 0.032 * Z + 3.3", self),
              '\n', _("M = 0.032 * {} + 3.3 = {}", self).format(
                round(z_val, EXPL_ROUND),
                round(m_val, EXPL_ROUND),
              ),
            ])

        s_p = s_f * (1 - 0.85 * d_t) / (1 - 0.85 * d_t / m_val)

        self.add_explain([
          '\n', _(
            "Failure stress level = Sflow * "
            "(1 - 0.85 * (depth / wallthickness)) / "
            "(1 - 0.85 * (depth / wallthickness) / M).",
            self
          ),
          '\n', _("stress_fail = {} * (1 - 0.85 * ({} / {})) / (1 - 0.85 * ({} / {}) / {}) = {}.", self).format(
            round(s_f, EXPL_ROUND),
            round(self.anomaly.depth, EXPL_ROUND),
            round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
            round(self.anomaly.depth, EXPL_ROUND),
            round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
            round(m_val, EXPL_ROUND),
            round(s_p, EXPL_ROUND),
          ),
        ])

        return s_p

    def get_press_fail(self, is_mod=False):
        """Return estimated failure pressure."""
        if is_mod:
            s_f = self.get_stress_fail_mod()
        else:
            s_f = self.get_stress_fail()

        p_f = 2 * s_f * self.relative_depth

        self.add_explain([
          '\n', _("Failure pressure = 2 * stress_fail * depth / wallthickness.", self),
          '\n', _("press_fail = 2 * {} * {} / {} = {}.", self).format(
            round(s_f, EXPL_ROUND),
            round(self.anomaly.depth, EXPL_ROUND),
            round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
            round(p_f, EXPL_ROUND),
          ),
        ])

        return p_f

    def erf(self, is_mod=False, is_explain=False):
        """Return estimated repair factor."""
        self.is_explain = is_explain
        self.explain_text = []

        modname = _("modified", self) if is_mod else _("classic", self)

        self.add_explain([
          _("Calculate ERF by {} {}.", self).format(self.name, modname),
        ])

        self.safe_pressure = self.get_press_fail(is_mod=is_mod)
        erf_val = self.anomaly.pipe.maop / self.safe_pressure

        self.add_explain([
          '\n', _("ERF = pipe_maop / press_fail.", self),
          '\n', "{} / {} = {}".format(
            self.anomaly.pipe.maop, round(self.safe_pressure, EXPL_ROUND), round(erf_val, EXPL_ROUND)
          ),
        ])

        return erf_val
