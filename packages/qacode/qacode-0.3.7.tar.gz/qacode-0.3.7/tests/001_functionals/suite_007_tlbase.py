# -*- coding: utf-8 -*-
"""Package testing.testlink"""


from qacode.core.testing.test_info_base import TestInfoBase


class TestTlBase(TestInfoBase):
    """TODO"""

    # properties

    def __init__(self, method_name="TestTlBase", logger_manager=None,
                 test_config=None):
        """TODO"""
        super(TestTlBase, self).__init__(method_name, logger_manager, test_config)



    def test_000_instance(self):
        """TODO"""
        # TODO: need to wait for qatestlink module be completed
        pass
