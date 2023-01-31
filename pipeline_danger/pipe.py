"""Single pipe from the pipeline."""


class Error(Exception):
    """Pipe dunger error."""


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
        from defect.metal_loss import Item

        self.metal_loss.append(Item(self, start, length, orient_start, orient_length, depth))
        return self.metal_loss[-1]
