"""ASME B31G method edition 1991."""
import math

from ...i18n import fake_gettext as _
from . import Context as ContextBase, EXPL_ROUND

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
    """Context of the ASME B31G  edition 1991."""

    name = "ASME B31G 1991"
    design_factor = 0.72  # DesignFactors.md
    temperature_factor = 1

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

        self.add_explain([
          _("The relative defect depth == defect depth / pipe wall thickness * 100%.", self),
          '\n', "{} / {} * 100 = {}".format(
            self.anomaly.depth, self.anomaly.pipe.wallthickness, round(self.relative_depth, EXPL_ROUND)
          ),
        ])

        if self.is_ok:

            self.add_explain([
              '\n', _("The relative defect depth less than {}% from wall thickness.", self).format(
                DEPTH_OK_PERCENT
              ),
              '\n', _("The defect is not dangerous.", self),
            ])
            result = State.Ok

        elif self.is_replace:

            self.add_explain([
              '\n', _("The relative defect depth greater than {}% from wall thickness.", self).format(
                DEPTH_CRITICAL_PERCENT
              ),
              '\n', _("The defect needs to be repaired.", self),
            ])
            result = State.Replace

        else:

            max_length = self.defect_max_length()
            if max_length > self.anomaly.length:
                self.add_explain([
                  '\n',
                  _("The length of the defect {} does not exceed the maximum allowable length {}.", self).format(
                    self.anomaly.length, round(max_length, EXPL_ROUND)
                  ),
                  '\n', _("The defect is not dangerous.", self),
                ])

                result = State.Safe

            else:

                self.add_explain([
                  '\n',
                  _("The length of the defect {} exceed the maximum allowable length {}.", self).format(
                    self.anomaly.length, round(max_length, EXPL_ROUND)
                  ),
                  '\n', _("It is necessary to calculate the allowable pressure for defect.", self),
                ])

                self.safe_pressure = self.get_safe_pressure()
                if self.safe_pressure > self.anomaly.pipe.maop:
                    self.add_explain([
                      '\n',
                      _("The working pressure {} does not exceed the allowable pressure {}.", self).format(
                        self.anomaly.pipe.maop, round(self.safe_pressure, EXPL_ROUND)
                      ),
                      '\n', _("The defect is not dangerous.", self),
                    ])
                    result = State.Defected
                else:
                    self.add_explain([
                      '\n',
                      _("Repair or pressure reduction to {} required.", self).format(
                        round(self.safe_pressure, EXPL_ROUND)
                      ),
                    ])

        return result

    def get_b(self):
        """Parameter B from method description."""
        self.add_explain([
          '\n', _("Parameter B.", self),
        ])

        b_max = 4.0
        border = 17.5
        if self.relative_depth < border:
            self.add_explain([
              '\n',
              _("The relative defect depth {} less than {}%.", self).format(
                round(self.relative_depth, EXPL_ROUND), border
              ),
              '\n', _("Set Parameter B value to {}.", self).format(b_max),
            ])
            return b_max

        self.add_explain([
          '\n',
          _("The relative defect depth {} more than {}%.", self).format(
            round(self.relative_depth, EXPL_ROUND), border
          ),
        ])

        rel = self.relative_depth / 100.0
        b_val = math.sqrt(math.pow(rel / (1.1 * rel - 0.15), 2) - 1)

        self.add_explain([
          '\n',
          "B = sqrt(pow({} / (1.1 * {} - 0.15), 2) - 1) = {}".format(
            round(rel, EXPL_ROUND), round(rel, EXPL_ROUND), round(b_val, EXPL_ROUND)
          ),
        ])

        return b_val

    def get_a(self, max_length):
        """Parameter A from method description."""
        a_val = 0.823 * max_length / self.diam_wall

        pipe = self.anomaly.pipe
        self.add_explain([
          '\n', "A = 0.823 * defect_length / sqrt(diameter * wallthickness)",
          '\n', "A = 0.823 * {} / sqrt({} * {}) = {}".format(
            max_length, pipe.diameter, pipe.wallthickness, round(a_val, EXPL_ROUND)
          ),
        ])

        return a_val

    @property
    def diam_wall(self):
        """Intermediate parameter."""
        pipe = self.anomaly.pipe
        return math.sqrt(pipe.diameter * pipe.wallthickness)

    def defect_max_length(self):
        """Return maximum allowable longitudinal extent of corrosion."""
        self.add_explain([
          '\n',
          _("Calculation of the maximum allowable defect length.", self),
        ])
        b_val = self.get_b()
        length = 1.12 * b_val * self.diam_wall
        pipe = self.anomaly.pipe

        self.add_explain([
          '\n',
          "L = 1.12 * B * sqrt(diameter * wallthickness)",
          "L = 1.12 * {} * sqrt({} * {}) = {}".format(
            round(b_val, EXPL_ROUND), pipe.diameter, pipe.wallthickness, round(length, EXPL_ROUND)
          ),
        ])

        return length

    def get_design_pressure(self):
        """Return design pressure."""
        pipe = self.anomaly.pipe
        smys = pipe.material.smys
        p_v = 2.0 * smys * pipe.wallthickness * self.design_factor * self.temperature_factor / pipe.diameter

        self.add_explain([
          '\n',
          "Design_press = 2 * material_smys * wallthickness * design_factor * temperature_factor / diam.",
          '\n',
          "Design_press = 2 * {} * {} * {} * {} / {} = {}.".format(
            smys, pipe.wallthickness, self.design_factor, self.temperature_factor,
            pipe.diameter, round(p_v, EXPL_ROUND)
          ),
        ])

        return p_v

    def get_safe_pressure(self):
        """Return acceptable pressure level."""
        self.add_explain([
          '\n',
          _("Calculation of the maximum allowable pressure.", self),
          '\n', _("Parameter A for defect length {}.", self).format(self.anomaly.length),
        ])
        a_val = self.get_a(self.anomaly.length)

        self.add_explain([
          '\n', _("Design pressure.", self),
        ])
        p_val = self.get_design_pressure()

        d_t = self.relative_depth / 100.0
        tmp = 1.1 * p_val

        if a_val > 4.0:
            p_s = tmp * (1 - d_t)
            self.add_explain([
              '\n', _("Parameter A more than 4.", self),
              '\n', "Safe_press = 1.1 * design_press * (1 - rel_depth).",
              '\n', "Safe_press = 1.1 * {} * (1 - {}) = {}.".format(
                round(p_val, EXPL_ROUND), round(d_t, EXPL_ROUND), round(p_s, EXPL_ROUND)
              ),
            ])
        else:
            v23 = 2.0 / 3.0
            a_pow = math.sqrt(math.pow(a_val, 2) + 1)
            p_s = tmp * ((1 - v23 * d_t) / (1 - v23 * d_t / a_pow))
            self.add_explain([
              '\n', _("Parameter A less than 4.", self),
              '\n', "a_pow = sqrt(pow(a_param, 2) + 1).",
              '\n', "a_pow = sqrt(pow({}, 2) + 1) = {}.".format(
                round(a_val, EXPL_ROUND), round(a_pow, EXPL_ROUND)
              ),
              '\n',
              "Safe_press = 1.1 * design_press * ((1 - 2/3 * rel_depth) / (1 - 2/3 * rel_depth / a_pow)).",
              '\n', "Safe_press = 1.1 * {} * ((1 - 2/3 * {}) / (1 - 2/3 * {} / {})) = {}.".format(
                round(p_val, EXPL_ROUND), round(d_t, EXPL_ROUND), round(d_t, EXPL_ROUND),
                round(a_pow, EXPL_ROUND), round(p_s, EXPL_ROUND)
              ),
            ])

        if p_s > p_val:
            self.add_explain([
              '\n', _("Safe pressure {} more than design pressure {}.", self).format(
                round(p_s, EXPL_ROUND), round(p_val, EXPL_ROUND)
              ),
              '\n',
              _("Use design pressure {} as maximum allowable pressure.", self).format(round(p_val, EXPL_ROUND)),
            ])
            return p_val

        self.add_explain([
          '\n', _("Use safe pressure {} as maximum allowable pressure.", self).format(round(p_s, EXPL_ROUND)),
        ])
        return p_s
