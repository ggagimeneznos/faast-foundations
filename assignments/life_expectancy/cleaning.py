"""Function to clean EU life expectancy data and filter Portugal data """
from pathlib import Path
import argparse
import pandas as pd
from life_expectancy.region import Region
from life_expectancy.data_reader import TSVReader, JSONReader


# Define constant base path for loading and saving data functions
DATA_DIR = Path(__file__).parent / "data"

def load_data(data_path: Path) -> pd.DataFrame:
    """Load raw data into a DataFrame using the given reader"""
    # Get path to the data file
    file_name = data_path.name.strip().upper()

    if file_name.endswith(".TSV"):
        reader = TSVReader()
    elif file_name.endswith(".JSON"):
        reader = JSONReader()
    else:
        raise ValueError("Unsupported file format")
    return reader.read(data_path)

def clean_data(df: pd.DataFrame, country: Region) -> pd.DataFrame:
    """Clean life expectancy data and filter by Region"""

    # If dataset is still in wide format (TSV case)
    if "year" not in df.columns:
        # Slipt the first column into 4 new columns data
        first_column = df.columns[0]
        df[['unit', 'sex', 'age', 'region']] = df[first_column].str.split(',', expand=True)

        # Transform data from wide format to long format
        year_columns = df.columns[1:-4]
        df = df.melt(
            id_vars=['unit','sex','age','region'],  # columns to keep fixed
            value_vars=year_columns,
            var_name='year',                        # new column with year
            value_name='value'                      # new column with life expectancy
        )

    # -- Data cleansing --
    # Convert year to int
    df['year'] = df['year'].astype(int)

    # Remove spaces from value column
    df['value'] = (
        df['value']
        .astype(str)
        .str.strip()
        .str.replace(r'[^0-9.]', '', regex=True)
    )

    # Convert value to float
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    # Remove lines with NaN on value column
    df = df.dropna(subset=['value'])

    # Keeps only data from the country
    df_country = df[df['region'] == country.value]
    return df_country.reset_index(drop=True)

def save_data(df_country: pd.DataFrame, country: Region) -> None:
    """Save cleaned data for the specified country to a CSV file"""
    df_country.to_csv(DATA_DIR / f"{country.value.lower()}_life_expectancy.csv", index=False)

def main(country: Region = Region.PT, file_name: str = "eu_life_expectancy_raw.tsv"):
    """Main pipeline to load, clean and save life expectancy data"""
    data_path = DATA_DIR / file_name

    # Load, clean and save
    df = load_data(data_path)
    cleaned_df = clean_data(df, country)
    save_data(cleaned_df, country)


if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("country", nargs="?", default="PT")
    parser.add_argument(
        "--file",
        default="eu_life_expectancy_raw.tsv",
        help="Input data file name"
    )
    args = parser.parse_args()
    main(country=Region(args.country), file_name=args.file)
