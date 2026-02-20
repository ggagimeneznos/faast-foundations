"""Tests for the fixture cleaning module"""
from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region

COUNTRY = Region.PT
BASE_FILE = Path(__file__).parent.parent / "tests" / "fixtures"
INPUT_FILE = BASE_FILE / "eu_life_expectancy_raw.tsv"
OUTPUT_FILE = BASE_FILE / f"{COUNTRY.value.lower()}_life_expectancy_expected.csv"

def test_clean_data_fixture():
    """Run the clean_data function with expected output"""
    # df = load_data(raw_file)
    df = pd.read_csv(INPUT_FILE, sep="\t")
    df_cleaned = clean_data(df, country=COUNTRY)
    df_cleaned.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__": # pragma: no cover
    test_clean_data_fixture()
