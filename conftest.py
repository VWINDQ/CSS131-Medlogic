"""
conftest.py — Pytest root configuration
========================================
Placing this file at the project root tells pytest two things:
  1. THIS directory is the root (rootdir)
  2. Add this directory to sys.path so `data`, `logic`, and
     `interface` are importable as top-level packages
 
Without this, pytest runs from inside tests/ and Python
can't find sibling packages like `data` or `logic`.
 
No imports needed — pytest handles path injection automatically
when it finds conftest.py at the root.
"""
import sys
import os
 
# Ensure the project root is always on sys.path,
# regardless of where pytest is invoked from.
sys.path.insert(0, os.path.dirname(__file__))
 