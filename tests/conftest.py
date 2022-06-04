"""
    Dummy conftest.py for structural_analysis.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

# import pytest

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(1, f'{BASE_DIR}')
