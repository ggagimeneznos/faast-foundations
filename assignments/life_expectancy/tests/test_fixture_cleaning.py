"""Tests for the fixture cleaning module"""
import argparse
from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import load_data, clean_data, main

COUNTRY = "PT"
INPUT_FILE = Path(__file__).parent.parent / "tests" / "fixtures" / "eu_life_expectancy_raw.tsv"
print(f"INPUT_FILE: {INPUT_FILE}")
OUTPUT_FILE = Path(__file__).parent.parent / "tests" / "fixtures" / f"{COUNTRY.lower()}_life_expectancy_expected.csv"
print(f"OUTPUT_FILE: {OUTPUT_FILE}")

def test_clean_data_fixture():
    """Run the clean_data function with expected output"""
    # df = load_data(raw_file)
    df = pd.read_csv(INPUT_FILE, sep="\t")
    df_cleaned = clean_data(df, country=COUNTRY)
    df_cleaned.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__": # pragma: no cover
    test_clean_data_fixture()