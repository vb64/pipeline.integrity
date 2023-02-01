"""ASME B31G method for metal loss defects.

https://pypi.org/project/pyintegrity/
https://github.com/novanumeric/WebIntegrity
https://edu.truboprovod.ru/kbase/doc/start/WebHelp_ru/ASMEB31G.htm
"""
from .. import Context as ContextBase
from ...defect import Type


class Context(ContextBase):
    """Context of the ASME B31G method."""

    valid_defect_types = [Type.MetalLoss]
    name = "ASME B31G"
