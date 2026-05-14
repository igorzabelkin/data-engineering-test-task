from pathlib import Path

OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_processed_data(sales):

    output_path = OUTPUT_DIR / "sales_prepared.csv"

    sales.to_csv(output_path, index=False)

    print(f"Processed dataset saved to: {output_path}")
    print(f"Final dataset shape: {sales.shape}")