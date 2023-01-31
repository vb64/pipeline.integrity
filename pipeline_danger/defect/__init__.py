"""Defects of pipeline."""


class Type:
    """Type of defect."""

    MetalLoss = "metalloss"
    Dent = "dent"
    Crack = "crack"


class Base:
    """Base class for different defect types."""

    def __init__(self, defect_type):
        """New defect."""
        self.type = defect_type
