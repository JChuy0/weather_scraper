# Created by Jason Chuy
"""This module is a context manager for the database functions."""

import sqlite3

class DBCM:
    """Context manager for database functions."""

    def __init__(self):
        """Initializes context manager."""
        
        super().__init__()
        self.conn = ""

    def __enter__(self):
        """Creates connection to database and returns a cursor."""

        self.conn = sqlite3.connect("weather.sqlite")
        cur = self.conn.cursor()

        return cur

    def __exit__(self, exc_type, exc_value, exc_trace):
        """Commits changes to database and closes connection."""

        self.conn.commit()

        if not self.conn.close:
            self.conn.close()
        
        return False