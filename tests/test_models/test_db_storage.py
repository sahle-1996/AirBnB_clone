#!/usr/bin/python3
"""
Database storage tests
"""

import unittest
import MySQLdb
import os

class DBStorageTestCase(unittest.TestCase):
    """Unit tests for database storage functionality"""

    def setUp(self):
        """Set up database connection for each test."""
        self.connection = MySQLdb.connect(
            host="localhost",
            port=3306,
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        self.cur = self.connection.cursor()

    def tearDown(self):
        """Close cursor and database connection after each test."""
        self.cur.close()
        self.connection.close()

    def test_add_state(self):
        """Test adding a state entry to the database."""
        self.cur.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cur.fetchone()[0]

        self.cur.execute("INSERT INTO states (name) VALUES ('Nevada')")
        self.connection.commit()

        self.cur.execute("SELECT COUNT(*) FROM states")
        final_count = self.cur.fetchone()[0]

        self.assertEqual(final_count, initial_count + 1)

if __name__ == "__main__":
    unittest.main()
