"""Module for reading data from different file formats."""
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod
import json
import pandas as pd

class DataReader(ABC):
    """Abstract base class for reading data."""

    @abstractmethod
    def read(self, file_path: str) -> pd.DataFrame:
        """Reads data from a given file path."""

class TSVReader(DataReader):
    """Concrete reader for TSV files."""

    def read(self, file_path: str) -> pd.DataFrame:
        """Reads a TSV file and returns a DataFrame."""
        return pd.read_csv(file_path, sep="\t")

class JSONReader(DataReader):
    """Concrete reader for JSON files."""

    def read(self, file_path: str) -> pd.DataFrame:
        """Reads a JSON file and returns a DataFrame."""
        # Read JSON data and convert to DataFrame
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        # Rename columns to match expected schema
        df = df.rename(columns={
            "country": "region",
            "life_expectancy": "value"
        })

        # Keep only necessary columns
        df = df[["unit", "sex", "age", "region", "year", "value"]]

        # Ensure correct data types
        df["year"] = df["year"].astype(int)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        # Remove rows with missing values
        df = df.dropna(subset=["value"])
        return df
