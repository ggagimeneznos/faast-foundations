"""Tests for the cleaning module"""
from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import load_data, clean_data, main

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "pt_life_expectancy.csv"

def test_clean_data(pt_life_expectancy_expected):
    """Run the clean_data function and compare the output to the expected output"""
    raw_file = Path(__file__).parent.parent / "data" / "eu_life_expectancy_raw.tsv"
    df = load_data(raw_file)
    df_cleaned = clean_data(df, country="PT")
    pd.testing.assert_frame_equal(df_cleaned, pt_life_expectancy_expected)

def test_main_runs():
    """Test that the main function runs without errors"""
    main(country="PT")
