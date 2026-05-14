import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():

    customers = pd.read_csv(next(DATA_DIR.glob("customers*.csv")))
    products = pd.read_csv(next(DATA_DIR.glob("products*.csv")))
    purchases = pd.read_csv(next(DATA_DIR.glob("purchases*.csv")))
    invoice_items = pd.read_csv(next(DATA_DIR.glob("invoice_items*.csv")))

    return customers, products, purchases, invoice_items


def clean_purchases(purchases):

    purchases["date"] = pd.to_datetime(purchases["date"])

    before = len(purchases)

    purchases = purchases.drop_duplicates()

    after = len(purchases)

    print(f"Removed exact duplicates: {before - after}")

    return purchases

def clean_invoice_items(invoice_items):

    before = len(invoice_items)

    invoice_items = invoice_items.drop_duplicates()

    after = len(invoice_items)

    print(f"Removed exact invoice_items duplicates: {before - after}")

    return invoice_items


def build_sales_dataset(customers, products, purchases, invoice_items):

    sales = purchases.merge(
        invoice_items,
        on=["InvoiceID", "product_id", "quantity"],
        how="left"
    )

    sales = sales.merge(
        customers,
        on="CustomerID",
        how="left"
    )

    sales = sales.merge(
        products[["product_id", "item", "category"]],
        on="product_id",
        how="left"
    )

    return sales


def save_processed_data(sales):

    output_path = OUTPUT_DIR / "sales_prepared.csv"

    sales.to_csv(output_path, index=False)

    print(f"Processed dataset saved to: {output_path}")
    print(f"Final dataset shape: {sales.shape}")


def validate_sales_dataset(sales):

    print("\nValidation checks:")

    print("Rows with missing price:")
    print(sales["price"].isnull().sum())

    print("Rows with missing line_total:")
    print(sales["line_total"].isnull().sum())

    print("Rows with missing customer_type:")
    print(sales["customer_type"].isnull().sum())

    print("Rows with missing item/category:")
    print(sales[["item", "category"]].isnull().sum())

    print("\nDate range:")
    print(sales["date"].min(), "->", sales["date"].max())

    print("\nTotal revenue:")
    print(sales["line_total"].sum())


if __name__ == "__main__":

    customers, products, purchases, invoice_items = load_data()

    purchases = clean_purchases(purchases)
    invoice_items = clean_invoice_items(invoice_items)

    sales = build_sales_dataset(
        customers,
        products,
        purchases,
        invoice_items
    )

    validate_sales_dataset(sales)

    save_processed_data(sales)

    print("\nFinal dataset columns:")
    print(sales.columns.tolist())

    print("\nSample:")
    print(sales.head())