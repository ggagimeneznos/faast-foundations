"""Unit tests for cleaning module"""
from pathlib import Path
from unittest.mock import patch
import pandas as pd
from life_expectancy.cleaning import load_data, clean_data, save_data, main



# Function to test load_data
def test_load_data_reads_tsv(tmp_path, eu_life_expectancy_raw):
    """load_data should correctly read a TSV file"""
    input_file = tmp_path / "sample.tsv"
    eu_life_expectancy_raw.to_csv(input_file, sep="\t", index=False)
    df = load_data(input_file)
    pd.testing.assert_frame_equal(df, eu_life_expectancy_raw)

# Function to test clean_data
def test_clean_data_filters_country(eu_life_expectancy_raw):
    """clean_data should filter data by country and reshape correctly"""
    df_cleaned = clean_data(eu_life_expectancy_raw, country="PT")
    assert not df_cleaned.empty
    assert (df_cleaned["region"] == "PT").all()
    expected_columns = ["unit", "sex", "age", "region", "year", "value"]
    assert list(df_cleaned.columns) == expected_columns

# Function to test save_data
def test_save_data_calls_to_csv(pt_life_expectancy_expected):
    """save_data should call DataFrame.to_csv without writing files"""
    with patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        save_data(pt_life_expectancy_expected, country="PT")
        mock_to_csv.assert_called_once()

# Function to test tha main
def test_main_runs_and_saves_data():
    """main should run end-to-end and attempt to save output"""
    with patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        main(country="PT")
        assert mock_to_csv.called
