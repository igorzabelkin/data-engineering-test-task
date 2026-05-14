import pandas as pd
from pathlib import Path

PROCESSED_DATA_PATH = Path("data/processed/sales_prepared.csv")


def load_prepared_data():
    return pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["date"])


def check_null_values(df):
    print("\nNULL values:")
    print(df.isnull().sum())


def check_exact_duplicates(df):
    duplicate_count = df.duplicated().sum()

    print("\nExact duplicates:")
    print(duplicate_count)


def check_anomalies(df):
    print("\nAnomaly checks:")

    print("Rows with quantity <= 0:")
    print((df["quantity"] <= 0).sum())

    print("Rows with price < 0:")
    print((df["price"] < 0).sum())

    print("Rows with line_total < 0:")
    print((df["line_total"] < 0).sum())


def check_line_total_consistency(df):
    df["expected_line_total"] = df["quantity"] * df["price"]

    inconsistent_rows = df[
        (df["line_total"] - df["expected_line_total"]).abs() > 0.01
    ]

    print("\nLine total consistency check:")
    print(f"Inconsistent rows: {len(inconsistent_rows)}")


def run_quality_checks():
    df = load_prepared_data()

    print("=" * 80)
    print("DATA QUALITY CHECKS")
    print("=" * 80)

    check_null_values(df)
    check_exact_duplicates(df)
    check_anomalies(df)
    check_line_total_consistency(df)


if __name__ == "__main__":
    run_quality_checks()