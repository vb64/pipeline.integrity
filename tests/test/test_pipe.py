"""Test Pipe class.

make test T=test_pipe.py
"""
import pytest
from . import TestBase


class TestsPipe(TestBase):
    """Pipe class."""

    def test_add_metal_loss(self):
        """Method add_metal_loss."""
        from pipeline_integrity.defect import Type
        from pipeline_integrity.pipe import (
          CIRCLE_MINUTES, ErrDefectSize, ErrDefectDepth, ErrDefectOrientStart, ErrDefectOrientLength,
        )

        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 5)
        assert len(self.pipe.metal_loss) == 1
        assert defect.type == Type.MetalLoss
        assert 'Steel smys' in str(self.pipe)

        with pytest.raises(ErrDefectSize) as err:
            self.pipe.add_metal_loss(self.pipe.length, 1, 10, 20, 5)
        assert 'Defect border outside pipe:' in str(err.value)

        with pytest.raises(ErrDefectOrientStart) as err:
            self.pipe.add_metal_loss(10, 100, CIRCLE_MINUTES + 1, 20, 5)
        assert 'Defect start orientdtion ' in str(err.value)

        with pytest.raises(ErrDefectOrientLength) as err:
            self.pipe.add_metal_loss(10, 100, 10, CIRCLE_MINUTES + 1, 5)
        assert 'Defect orientdtion length ' in str(err.value)

        with pytest.raises(ErrDefectDepth) as err:
            self.pipe.add_metal_loss(10, 100, 10, 20, self.pipe.wallthickness + 1)
        assert 'Defect depth ' in str(err.value)
