"""Application configuration.

Reads the database URL from the ``CARGOREX_DB_URL`` environment variable so no
sensitive path or credential is hard-coded (constitution, Principle VI).
"""
import os

# Default: local SQLite file for the demonstration data.
DATABASE_URL = os.environ.get("CARGOREX_DB_URL", "sqlite:///./cargorex.db")
