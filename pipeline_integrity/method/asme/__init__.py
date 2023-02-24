"""ASME B31G method for metal loss defects.

https://pypi.org/project/pyintegrity/
https://github.com/novanumeric/WebIntegrity
https://edu.truboprovod.ru/kbase/doc/start/WebHelp_ru/ASMEB31G.htm
"""
import os

from .. import Context as ContextBase
from ...defect import Type
from ...i18n import load_po


class Context(ContextBase):
    """Context of the ASME B31G method."""

    valid_defect_types = [Type.MetalLoss]

    @classmethod
    def lang(cls, lang_code):
        """Load language dict for localize explain text."""
        name = os.path.join(os.path.dirname(__file__), 'locale', lang_code, 'LC_MESSAGES', 'messages.po')
        return load_po(name)
