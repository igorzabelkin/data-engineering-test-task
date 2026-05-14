import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")


def load_data():

    customers = pd.read_csv(next(DATA_DIR.glob("customers*.csv")))
    products = pd.read_csv(next(DATA_DIR.glob("products*.csv")))
    purchases = pd.read_csv(next(DATA_DIR.glob("purchases*.csv")))
    invoice_items = pd.read_csv(next(DATA_DIR.glob("invoice_items*.csv")))

    return customers, products, purchases, invoice_items