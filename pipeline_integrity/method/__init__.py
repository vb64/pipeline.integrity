"""Danger calculation methods."""
from .. import Error as ErrorBase


class ErrDefectTypeNotSupported(ErrorBase):
    """Given defect type not supported by method."""


class Context(object):
    """Base class for Context of the danger method."""

    name = "not defined"
    valid_defect_types = []

    def __init__(self, defect):
        """Create new context instance."""
        if defect.type not in self.valid_defect_types:
            raise ErrDefectTypeNotSupported("Defect type '{}' not supported by method '{}'".format(
              defect.type, self.name
            ))

        self.anomaly = defect
        self.explain_text = []
        self.is_explain = False

    def __str__(self):
        """Return as text."""
        return "{}\nPipe {}\nDfct {}".format(
          self.name,
          str(self.anomaly.pipe),
          str(self.anomaly)
        )

    @classmethod
    def lang(cls, _lang_code):
        """Load language dict for localize explain text."""
        raise NotImplementedError("{}.lang".format(cls.__class__.__name__))

    def explain(self):
        """Return text with explanation for calculation."""
        return ''.join(self.explain_text)

    def add_explain(self, msg_list):
        """Add messages from the list to explain array."""
        if self.is_explain:
            self.explain_text.extend(msg_list)
