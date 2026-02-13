"""Tests for the cleaning module"""
from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import load_data, clean_data, main
from . import OUTPUT_DIR
from life_expectancy.region import Region

# OUTPUT_FILE = Path(__file__).parent.parent / "data" / "pt_life_expectancy.csv"
OUTPUT_FILE = OUTPUT_DIR / "pt_life_expectancy_expected.csv"

def test_clean_data(pt_life_expectancy_expected, eu_life_expectancy_raw):
    """Run the clean_data function and compare the output to the expected output"""
    # df = load_data(OUTPUT_FILE)
    df_cleaned = clean_data(eu_life_expectancy_raw, country=Region.PT)
    pd.testing.assert_frame_equal(df_cleaned, pt_life_expectancy_expected)

def test_main_runs():
    """Test that the main function runs without errors"""
    main(country=Region.PT)