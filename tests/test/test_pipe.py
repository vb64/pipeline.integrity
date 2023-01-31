"""Test Pipe class.

make test T=test_pipe.py
"""
# import pytest
from . import TestBase


class TestsPipe(TestBase):
    """Pipe class."""

    def test_add_metal_loss(self):
        """Method add_metal_loss."""
        from pipeline_danger.defect import Type

        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 5)
        assert len(self.pipe.metal_loss) == 1
        assert defect.type == Type.MetalLoss
