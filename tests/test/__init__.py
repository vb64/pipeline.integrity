"""Root class for testing."""
from unittest import TestCase


class TestBase(TestCase):
    """Base class for tests."""

    def setUp(self):
        """Set up test data."""
        super().setUp()
        from pipeline_danger.material import Material
        from pipeline_danger.pipe import Pipe

        self.material = Material("Steel", 20000)
        self.pipe = Pipe(11200, 1420, 10, self.material, 1000)
