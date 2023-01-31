"""Root class for testing."""
from unittest import TestCase


class TestBase(TestCase):
    """Base class for tests."""

    def setUp(self):
        """Set up test data."""
        super().setUp()
        from pipeline_danger.material import Material

        self.material = Material("Steel", 20000)
