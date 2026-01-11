"""Function to clean EU life expectancy data and filter Portugal data """
from pathlib import Path
import argparse
import pandas as pd

def clean_data(country):
    """Load raw TSV data, clean and save only Portugal life expectancy in CSV format """

    # Get path to the data file
    print(f"Path this file: {Path(__file__)}")
    print(f"Parent path: {Path(__file__).parent}")
    data_path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    print(f"Full data path: {data_path}")

    # Read the dataset, for TSV data (tab separated values)
    df = pd.read_csv(data_path, sep="\t")

    # Slipt the first column into 4 new columns
    first_column = df.columns[0]
    df[['unit', 'sex', 'age', 'region']] = df[first_column].str.split(',', expand=True)

    # Transform data from wide format to long format
    year_columns = df.columns[1:-4]  # seleciona apenas as colunas de ano
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

    # Keeps only data from PT (Portugal)
    df_pt = df_long[df_long['region'] == country]

    # Save the final processed file, containing only country data
    output_path = Path(__file__).parent / "data" / f"{country.lower()}_life_expectancy.csv"
    print(f"Output CSV path: {output_path}")
    df_pt.to_csv(output_path, index=False) # Without the index column



if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("country", nargs="?", default="PT")
    args = parser.parse_args()
    clean_data(country=args.country)
