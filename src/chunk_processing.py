import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")
OUTPUT_PATH = Path("data/processed/chunk_aggregated_sales.csv")

CHUNK_SIZE = 50000


def process_large_file():

    purchases_file = next(
        RAW_DATA_PATH.glob("purchases*.csv")
    )

    total_raw_rows = 0
    total_processed_rows = 0
    total_removed_duplicates = 0

    aggregated_chunks = []

    print("=" * 80)
    print("CHUNK PROCESSING STARTED")
    print("=" * 80)

    for chunk_number, chunk in enumerate(
        pd.read_csv(purchases_file, chunksize=CHUNK_SIZE),
        start=1
    ):

        print(f"\nProcessing chunk #{chunk_number}")
        print(f"Chunk shape before cleaning: {chunk.shape}")

        raw_rows = len(chunk)
        total_raw_rows += raw_rows

        chunk = chunk.drop_duplicates()

        processed_rows = len(chunk)
        removed_duplicates = raw_rows - processed_rows

        total_processed_rows += processed_rows
        total_removed_duplicates += removed_duplicates

        print(f"Removed duplicates: {removed_duplicates}")
        print(f"Chunk shape after cleaning: {chunk.shape}")

        chunk_agg = (
            chunk.groupby("product_id", as_index=False)["quantity"]
            .sum()
        )

        aggregated_chunks.append(chunk_agg)

    print("\nCombining chunk aggregations...")

    final_result = pd.concat(aggregated_chunks)

    final_result = (
        final_result.groupby("product_id", as_index=False)["quantity"]
        .sum()
        .sort_values("quantity", ascending=False)
    )

    final_result.to_csv(OUTPUT_PATH, index=False)

    print("\nProcessing completed")
    print(f"Total raw rows: {total_raw_rows}")
    print(f"Total processed rows: {total_processed_rows}")
    print(f"Total removed duplicates: {total_removed_duplicates}")
    print(f"Saved result to: {OUTPUT_PATH}")

    print("\nFinal result sample:")
    print(final_result.head())


if __name__ == "__main__":
    process_large_file()