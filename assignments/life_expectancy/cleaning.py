"""Function to clean EU life expectancy data and filter Portugal data """
from pathlib import Path
import argparse
import pandas as pd

# Define constant base path for loading and saving data functions
DATA_DIR = Path(__file__).parent / "data"

def load_data(data_path: Path = DATA_DIR / "eu_life_expectancy_raw.tsv") -> pd.DataFrame:
    """Load raw TSV data into a DataFrame"""
    # Get path to the data file
    return pd.read_csv(data_path, sep="\t")

def clean_data(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Clean life expectancy data and filter by country (PT by default)"""

    # Slipt the first column into 4 new columns data
    first_column = df.columns[0]
    df[['unit', 'sex', 'age', 'region']] = df[first_column].str.split(',', expand=True)

    # Transform data from wide format to long format
    year_columns = df.columns[1:-4]
    df_long = df.melt(
        id_vars=['unit','sex','age','region'],  # columns to keep fixed
        value_vars=year_columns,
        var_name='year',                        # new column with year
        value_name='value'                      # new column with life expectancy
    )

    # -- Data cleansing --
    # Convert year to int
    df_long['year'] = df_long['year'].astype(int)

    # Remove spaces from value column
    df_long['value'] = (
        df_long['value']
        .astype(str)
        .str.strip()
        .str.replace(r'[^0-9.]', '', regex=True)
    )

    # Convert value to float
    df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')

    # Remove lines with NaN on value column
    df_long = df_long.dropna(subset=['value'])

    # Keeps only data from the country
    df_country = df_long[df_long['region'] == country]
    return df_country.reset_index(drop=True)

def save_data(df_country: pd.DataFrame, country: str) -> None:
    """Save cleaned data for the specified country to a CSV file"""
    df_country.to_csv(DATA_DIR / f"{country.lower()}_life_expectancy.csv", index=False)

def main(country: str = "PT"):
    """Main pipeline to load, clean and save life expectancy data"""    
    # Load, clean and save data
    df = load_data()
    cleaned_df = clean_data(df, country)
    save_data(cleaned_df, country)


if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("country", nargs="?", default="PT")
    args = parser.parse_args()
    main(country=args.country)
