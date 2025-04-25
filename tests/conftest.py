from pathlib import Path

import pytest


@pytest.fixture
# Provide an output directory under tests/output and clean it before each test
# ... existing code is setting up fixtures ...
def output() -> Path:
    """Return the output directory for pptx files under tests/output and clean it before each test."""
    out_dir = Path(__file__).parent / "output"
    if out_dir.exists():
        for file in out_dir.iterdir():
            if file.is_file():
                file.unlink()
    else:
        out_dir.mkdir(parents=True)
    return out_dir
