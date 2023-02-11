"""Danger calculation methods."""
from .. import Error as ErrorBase


class ErrDefectTypeNotSupported(ErrorBase):
    """Given defect type not supported by method."""


class Context(object):
    """Base class for Context of the danger method."""

    name = "not defined"
    valid_defect_types = []

    def __init__(self, defect):
        """New context instance."""
        if defect.type not in self.valid_defect_types:
            raise ErrDefectTypeNotSupported("Defect type '{}' not supported by method '{}'".format(
              defect.type, self.name
            ))

        self.anomaly = defect
        self.explain_text = []
        self.is_explain = False

    def explain(self):
        """Return text with explanation for calculation."""
        return '\n'.join(self.explain_text)
