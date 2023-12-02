"""Defects of pipeline."""


class Type:
    """Type of defect."""

    MetalLoss = "metalloss"
    Dent = "dent"
    Crack = "crack"


class Base(object):
    """Base class for different defect types."""

    def __init__(self, defect_type, pipe):
        """Create new defect at the pipe."""
        self.type = defect_type
        self.pipe = pipe

    def __str__(self):
        """Return as text."""
        return self.type
