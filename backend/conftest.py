"""
conftest.py — pytest root configuration for the MemoryLens backend.

Adds the backend/ directory to sys.path so that `from app.xxx import yyy`
works correctly when running pytest from the backend/ folder.
"""
import os
import sys

# Must be set before app imports so Memory uses JSON rather than JSONB and the
# synthetic search dataset remains the active fallback during tests.
os.environ.setdefault("TESTING", "1")

# Ensure the backend directory is on sys.path
sys.path.insert(0, os.path.dirname(__file__))
