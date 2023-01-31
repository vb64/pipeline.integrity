"""Single pipe from the pipeline."""
from . import Error as ErrorBase

CIRCLE_MINUTES = 60.0


class Error(ErrorBase):
    """Pipe error."""


class Pipe:
    """Single pipe."""

    def __init__(self, length, diameter, wallthickness, material):
        """New pipe."""
        self.length = length  # mm
        self.diameter = diameter  # mm
        self.wallthickness = wallthickness  # mm
        self.material = material
        self.metal_loss = []

    def add_metal_loss(self, start, length, orient_start, orient_length, depth):
        """Add and return metal loss defect at the pipe."""
        from .defect.metal_loss import Item

        if (start + length) > self.length:
            raise Error(
              "Defect border outside pipe: start {} + length {} = {} > pipe length {}.".format(
                start, length, start + length, self.length
              )
            )

        if depth > self.wallthickness:
            raise Error("Defect depth {} > pipe wall thickness {}.".format(depth, self.wallthickness))

        if not (-CIRCLE_MINUTES <= orient_start <= CIRCLE_MINUTES):
            raise Error(
              "Defect start orientdtion {} must be from {} to {} angle minutes.".format(
                orient_start, -CIRCLE_MINUTES, CIRCLE_MINUTES
              )
            )

        if not (0 < orient_length <= CIRCLE_MINUTES):
            raise Error(
              "Defect orientdtion length {} must be from 0 to {} angle minutes.".format(
                orient_length, CIRCLE_MINUTES
              )
            )

        self.metal_loss.append(Item(self, start, length, orient_start, orient_length, depth))
        return self.metal_loss[-1]
