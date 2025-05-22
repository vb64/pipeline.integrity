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
    REPAIR_NOT_REQUIRED = 777

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
          '\n', "Z = {}^2 / ({} * {}) = {}.".format(
            round(self.anomaly.length, EXPL_ROUND),
            round(pipe.diameter, EXPL_ROUND),
            round(pipe.wallthickness, EXPL_ROUND),
            round(z_val, EXPL_ROUND),
          ),
        ])

        return z_val

    def m_param(self, z_val):
        """Parameter M."""
        m_val = math.sqrt(1 + 0.8 * z_val)

        self.add_explain([
          '\n', _("Parameter M = sqrt(1 + 0.8 * Z).", self),
          '\n', "M = sqrt(1 + 0.8 * {}) = {}.".format(
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
          '\n', "Sflow = 1.1 * {} = {}.".format(
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
            m_val = self.m_param(z_val)
            s_p = s_f * (1 - v23 * d_t) / (1 - v23 * d_t / m_val)

            self.add_explain([
              '\n', _("Parameter Z = {} <= 20.", self).format(round(z_val, EXPL_ROUND)),
              '\n', _(
                "Failure stress level = Sflow * "
                "(1 - 2/3 * (depth / wallthickness)) / "
                "(1 - 2/3 * (depth / wallthickness) / M).",
                self
              ),

              '\n', self.explain_stress_fail(s_f, m_val, s_p),
            ])

            return s_p

        s_p = s_f * (1 - d_t)

        self.add_explain([
          '\n', _("Parameter Z = {} > 20.", self).format(round(z_val, EXPL_ROUND)),
          '\n', _("Failure stress level = Sflow * (1 - depth / wallthickness).", self),
          '\n', "stress_fail = {} * (1 - {} / {}) = {}.".format(
            round(s_f, EXPL_ROUND),
            round(self.anomaly.depth, EXPL_ROUND),
            round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
            round(s_p, EXPL_ROUND),
          ),
        ])

        return s_p

    def explain_stress_fail(self, s_f, m_val, s_p):
        """Return text that explain stress_fail calculation."""
        return "stress_fail = {} * (1 - 0.85 * ({} / {})) / (1 - 0.85 * ({} / {}) / {}) = {}.".format(
          round(s_f, EXPL_ROUND),
          round(self.anomaly.depth, EXPL_ROUND),
          round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
          round(self.anomaly.depth, EXPL_ROUND),
          round(self.anomaly.pipe.wallthickness, EXPL_ROUND),
          round(m_val, EXPL_ROUND),
          round(s_p, EXPL_ROUND),
        )

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
              '\n', "M = sqrt(1 + 0.6275 * {} - 0.003375 * {}^2) = {}".format(
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
              '\n', "M = 0.032 * {} + 3.3 = {}".format(
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
          '\n', self.explain_stress_fail(s_f, m_val, s_p),
        ])

        return s_p

    def get_press_fail(self, is_mod=False):
        """Return estimated failure pressure."""
        if is_mod:
            s_f = self.get_stress_fail_mod()
        else:
            s_f = self.get_stress_fail()

        pipe = self.anomaly.pipe
        p_f = 2 * s_f * pipe.wallthickness / pipe.diameter

        self.add_explain([
          '\n', _("Failure pressure = 2 * stress_fail * wallthickness / diameter.", self),
          '\n', "press_fail = 2 * {} * {} / {} = {}.".format(
            round(s_f, EXPL_ROUND),
            round(pipe.wallthickness, EXPL_ROUND),
            round(pipe.diameter, EXPL_ROUND),
            round(p_f, EXPL_ROUND),
          ),
        ])

        return p_f

    def erf(self, is_mod=False):
        """Return estimated repair factor."""
        modname = _("modified", self) if is_mod else _("classic", self)
        self.add_explain([
          _("Calculate ERF by {} {}.", self).format(self.name, modname),
        ])

        self.safe_pressure = self.get_press_fail(is_mod=is_mod) * self.design_factor
        erf_val = 1
        if self.safe_pressure > 0:
            erf_val = self.anomaly.pipe.maop / self.safe_pressure

        self.add_explain([
          '\n', _("ERF = pipe_maop / press_fail.", self),
          '\n', "ERF = {} / {} = {}".format(
            self.anomaly.pipe.maop,
            round(self.safe_pressure, EXPL_ROUND),
            round(erf_val, EXPL_ROUND)
          ),
        ])

        return erf_val

    def years(self, is_mod=False):
        """Return estimated years for repair."""
        is_explain = self.is_explain

        erf_l = self.erf(is_mod=is_mod)
        if erf_l >= 1:
            self.add_explain([
              '\n', _("Repair required immediately, years to repair: 0.", self),
            ])
            return 0

        depth_saved = self.anomaly.depth

        right = int((self.anomaly.pipe.wallthickness - self.anomaly.depth) / self.corrosion_rate) + 1
        self.anomaly.depth = self.anomaly.pipe.wallthickness - self.corrosion_rate / 12.0

        self.add_explain([
          '\n',
          '\n', _("Repair is not required at the moment, calculate the time before repair.", self),
          '\n',
          _(
            "With corrosion rate {} mm/year, pipe wall {} and depth {} "
            "a through hole is formed after years: {}.",
            self
          ).format(
            round(self.corrosion_rate, EXPL_ROUND),
            self.anomaly.pipe.wallthickness,
            depth_saved,
            right
          ),
        ])

        self.is_explain = False
        erf_r = self.erf(is_mod=is_mod)
        self.is_explain = is_explain

        if erf_r < 1:
            self.add_explain([
              '\n', _("But even a through defect does not require repair.", self),
              '\n', _("ERF = {}. Use special value for years: 777.", self).format(
                round(erf_r, EXPL_ROUND)
              ),
            ])

            self.anomaly.depth = depth_saved
            return self.REPAIR_NOT_REQUIRED

        self.add_explain([
          '\n',
          _("Calculating the year in which the corrosion growth of the defect will require repair.", self),
        ])

        self.is_explain = False
        left = 0

        while (right - left) > 1:
            years = left + int((right - left) / 2)
            self.anomaly.depth = depth_saved + self.corrosion_rate * years
            erf_val = self.erf(is_mod=is_mod)
            if erf_val < 1:
                erf_l = erf_val
                left = years
            else:
                erf_r = erf_val
                right = years

        self.is_explain = is_explain
        self.add_explain([
          '\n', _("Years: {} ERF: {}.", self).format(left, round(erf_l, EXPL_ROUND)),
          '\n', _("Years: {} ERF: {}.", self).format(right, round(erf_r, EXPL_ROUND)),
          '\n', _("Defect will require repair after years: {}.", self).format(left),
        ])

        self.anomaly.depth = depth_saved
        return left
