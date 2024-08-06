#!/usr/bin/python3
"""
Example of a test case that skips execution conditionally
"""

import unittest
from models import storage_type

class ConditionalSkipTest(unittest.TestCase):
    """Test cases for conditional skipping"""

    @unittest.skipIf(storage_type == 'file', "Skip for file storage type")
    def test_conditional_skip(self):
        """This test is skipped for file storage type"""
        pass

if __name__ == "__main__":
    unittest.main()
