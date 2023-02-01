"""ASME B31G method for metal loss defects."""
from .. import Context as ContextBase
from ...defect import Type


class Context(ContextBase):
    """Context of the ASME B31G method."""

    valid_defect_types = [Type.MetalLoss]
    name = "ASME B31G"
