"""Root class for testing."""
from unittest import TestCase
from py23 import super23


class TestBase(TestCase):
    """Base class for tests."""

    def setUp(self):
        """Set up test data."""
        super23(self).setUp()
        from pipeline_integrity.material import Material
        from pipeline_integrity.pipe import Pipe

        self.material = Material("Steel", 20000)
        self.pipe = Pipe(11200, 1420, 10, self.material, 1000)
