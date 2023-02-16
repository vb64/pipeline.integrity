"""Test method module.

make test T=test_method/test_init.py
"""
import pytest
from . import TestMethod


class TestsContext(TestMethod):
    """Class Context."""

    def test_explain(self):
        """Function explain."""
        from pipeline_integrity.defect import Type
        from pipeline_integrity.method import Context

        Context.valid_defect_types.append(Type.MetalLoss)

        defect = self.pipe.add_metal_loss(10, 100, 10, 20, 1.5)
        asme = Context(defect)
        assert asme.explain() == ''
        asme.explain_text = ['xx', 'yy']
        assert asme.explain() == 'xxyy'

        asme.add_explain(['zz'])
        assert asme.explain() == 'xxyy'

        asme.is_explain = True
        asme.add_explain(['zz'])
        assert asme.explain() == 'xxyyzz'

    @staticmethod
    def test_lang():
        """Method lang."""
        from pipeline_integrity.method import Context

        with pytest.raises(NotImplementedError) as err:
            Context.lang('xxx')
        assert '.lang' in str(err.value)
