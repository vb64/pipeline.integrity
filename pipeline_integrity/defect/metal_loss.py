"""Metal loss defect."""
from . import Type, Base


class Item(Base):
    """Metal loss defect class."""

    def __init__(
      self, pipe, start, length, orient_start, orient_length, depth,
      max_depth_start=None, max_depth_orient=None
    ):
        """Create new defect."""
        super(Item, self).__init__(Type.MetalLoss, pipe)
        self.start = start  # mm
        self.length = length  # mm
        self.orient_start = orient_start  # minutes
        self.orient_length = orient_length  # minutes
        self.depth = depth  # mm
        self.max_depth_start = max_depth_start
        self.max_depth_orient = max_depth_orient

    def __str__(self):
        """Return as text."""
        return "{} len {} depth {}".format(
          super(Item, self).__str__(),
          self.length,
          self.depth
        )
