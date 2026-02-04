"""Pytest configuration file"""
import pandas as pd
import pytest
from pathlib import Path

# from . import FIXTURES_DIR, OUTPUT_DIR
FIXTURES_DIR = Path(__file__).parent / "fixtures" 
OUTPUT_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture(scope="session")
def eu_life_expectancy_raw() -> pd.DataFrame:
    """Fixture to load the expected INPUT of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep="\t")

@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected OUTPUT of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")