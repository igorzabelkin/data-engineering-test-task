import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")


def load_csv_files():
    files = list(DATA_DIR.glob("*.csv"))

    if not files:
        raise FileNotFoundError(f"No CSV files found in {DATA_DIR}")

    dataframes = {}

    for file in files:
        table_name = file.stem.split("_")[0]
        df = pd.read_csv(file)

        dataframes[table_name] = df

        print("\n" + "=" * 80)
        print(f"FILE: {file.name}")
        print(f"TABLE NAME: {table_name}")
        print("=" * 80)

        print("\nShape:")
        print(df.shape)

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nData types:")
        print(df.dtypes)

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nNULL values:")
        print(df.isnull().sum())

        print("\nDuplicated rows:")
        print(df.duplicated().sum())

    return dataframes


def check_business_keys(dataframes):

    purchases = dataframes["purchases"]
    invoice = dataframes["invoice"]

    print("\n" + "=" * 80)
    print("BUSINESS KEY CHECKS")
    print("=" * 80)

    purchase_duplicates = purchases.duplicated(
        subset=["InvoiceID", "product_id"]
    ).sum()

    print("\nPurchases duplicate business keys:")
    print(purchase_duplicates)

    invoice_duplicates = invoice.duplicated(
        subset=["InvoiceID", "product_id"]
    ).sum()

    print("\nInvoice duplicate business keys:")
    print(invoice_duplicates)


def inspect_duplicates(dataframes):

    purchases = dataframes["purchases"]

    duplicate_rows = purchases[
        purchases.duplicated(
            subset=["InvoiceID", "product_id"],
            keep=False
        )
    ]

    print("\n" + "=" * 80)
    print("DUPLICATE SAMPLE")
    print("=" * 80)

    print(
        duplicate_rows
        .sort_values(["InvoiceID", "product_id"])
        .head(20)
    )

def check_exact_duplicates(dataframes):

    purchases = dataframes["purchases"]

    exact_duplicates = purchases[
        purchases.duplicated(keep=False)
    ]

    print("\n" + "=" * 80)
    print("EXACT DUPLICATES")
    print("=" * 80)

    print(f"\nTotal exact duplicates: {exact_duplicates.shape[0]}")

    print("\nSample:")
    print(exact_duplicates.head(20))

def check_referential_integrity(dataframes):

    purchases = dataframes["purchases"]
    customers = dataframes["customers"]
    products = dataframes["products"]

    print("\n" + "=" * 80)
    print("REFERENTIAL INTEGRITY CHECKS")
    print("=" * 80)

    missing_customers = purchases[
        ~purchases["CustomerID"].isin(customers["CustomerID"])
    ]

    print("\nMissing customers:")
    print(missing_customers.shape[0])

    missing_products = purchases[
        ~purchases["product_id"].isin(products["product_id"])
    ]

    print("\nMissing products:")
    print(missing_products.shape[0])

if __name__ == "__main__":
    dataframes = load_csv_files()
    
    check_referential_integrity(dataframes)
    #check_exact_duplicates(dataframes)
    #check_business_keys(dataframes)
    #inspect_duplicates(dataframes)