#!/usr/bin/python3
"""
Unit tests for the State class.
"""

import unittest
from models.state import State
from models import storage

class StateTestCase(unittest.TestCase):
    """Test suite for the State model."""

    def setUp(self):
        """Set up for each test."""
        self.state_instance = State(name="New York")

    def tearDown(self):
        """Tear down after each test."""
        del self.state_instance

    def test_state_name(self):
        """Check if the state name is set correctly."""
        self.assertEqual(self.state_instance.name, "New York")

    def test_state_storage(self):
        """Ensure the state is saved in storage."""
        self.state_instance.save()
        self.assertIn(self.state_instance, storage.all().values())

if __name__ == "__main__":
    unittest.main()
