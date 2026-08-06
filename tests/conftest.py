from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
CATALOG_ROOT = FIXTURES_DIR / "catalog"
CYCLE_CATALOG_ROOT = FIXTURES_DIR / "cycle_catalog"


@pytest.fixture
def catalog_root() -> Path:
    return CATALOG_ROOT


@pytest.fixture
def cycle_catalog_root() -> Path:
    return CYCLE_CATALOG_ROOT
