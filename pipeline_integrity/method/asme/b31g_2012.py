"""ASME B31G method for metal loss defects edition 2012."""
import os
import math

from ...defect import Type
from ...i18n import load_po
from .. import Context as ContextBase


class Context(ContextBase):
    """Context of the ASME B31G method edition 2012."""

    name = "ASME B31G 2012"
    valid_defect_types = [Type.MetalLoss]

    @classmethod
    def lang(cls, lang_code):
        """Load language dict for localize explain text for 2012 edition."""
        name = os.path.join(os.path.dirname(__file__), 'locale', lang_code, 'LC_MESSAGES', 'messages.po')
        return load_po(name)

    @property
    def z_param(self):
        """Parameter z."""
        pipe = self.anomaly.pipe
        return math.pow(self.anomaly.length, 2) / (pipe.diameter * pipe.wallthickness)
