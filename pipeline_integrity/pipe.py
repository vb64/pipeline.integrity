"""Single pipe from the pipeline."""
from . import Error as ErrorBase

CIRCLE_MINUTES = 60.0


class ErrDefectSize(ErrorBase):
    """Wrong defect size (outside pipe)."""


class ErrDefectDepth(ErrorBase):
    """Wrong defect depth."""


class ErrDefectOrientStart(ErrorBase):
    """Wrong defect start orientdtion."""


class ErrDefectOrientLength(ErrorBase):
    """Wrong defect orientdtion length."""


class Pipe:
    """Single pipe under pressure (maop)."""

    def __init__(self, length, diameter, wallthickness, material, maop):
        """Create new pipe."""
        self.length = length  # mm
        self.diameter = diameter  # mm
        self.wallthickness = wallthickness  # mm
        self.material = material
        self.maop = maop
        self.metal_loss = []

    def __str__(self):
        """Return as text."""
        return "{} diam {} wall {} maop {}".format(
          str(self.material),
          self.diameter,
          self.wallthickness,
          self.maop
        )

    def add_metal_loss(self, start, length, orient_start, orient_length, depth):
        """Add and return metal loss defect at the pipe."""
        from .defect.metal_loss import Item

        if (start + length) > self.length:
            raise ErrDefectSize(
              "Defect border outside pipe: start {} + length {} = {} > pipe length {}.".format(
                start, length, start + length, self.length
              )
            )

        if depth > self.wallthickness:
            raise ErrDefectDepth("Defect depth {} > pipe wall thickness {}.".format(depth, self.wallthickness))

        if not (-CIRCLE_MINUTES <= orient_start <= CIRCLE_MINUTES):
            raise ErrDefectOrientStart(
              "Defect start orientdtion {} must be from {} to {} angle minutes.".format(
                orient_start, -CIRCLE_MINUTES, CIRCLE_MINUTES
              )
            )

        if not (0 < orient_length <= CIRCLE_MINUTES):
            raise ErrDefectOrientLength(
              "Defect orientdtion length {} must be from 0 to {} angle minutes.".format(
                orient_length, CIRCLE_MINUTES
              )
            )

        self.metal_loss.append(Item(self, start, length, orient_start, orient_length, depth))
        return self.metal_loss[-1]
