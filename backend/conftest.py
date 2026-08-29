"""
conftest.py — pytest root configuration for the MemoryLens backend.

Adds the backend/ directory to sys.path so that `from app.xxx import yyy`
works correctly when running pytest from the backend/ folder.
"""
import sys
import os

# Ensure the backend directory is on sys.path
sys.path.insert(0, os.path.dirname(__file__))
