import pandas as pd
from pathlib import Path

PROCESSED_DATA_PATH = Path("data/processed/sales_prepared.csv")

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    return pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["date"])


def top_products(df, top_n=10):

    print("\n" + "=" * 80)
    print(f"TOP {top_n} PRODUCTS BY REVENUE")
    print("=" * 80)

    result = (
        df.groupby("item", as_index=False)["line_total"]
        .sum()
        .sort_values("line_total", ascending=False)
        .head(top_n)
    )

    result["line_total"] = result["line_total"].round(2)

    print(result)

    output_path = OUTPUT_DIR / "top_products.csv"

    result.to_csv(output_path, index=False)

    print(f"\nSaved to: {output_path}")


def monthly_revenue(df):

    print("\n" + "=" * 80)
    print("MONTHLY REVENUE")
    print("=" * 80)

    df["year_month"] = df["date"].dt.to_period("M")

    result = (
        df.groupby("year_month", as_index=False)["line_total"]
        .sum()
        .sort_values("year_month")
    )

    result["line_total"] = result["line_total"].round(2)

    output_path = OUTPUT_DIR / "monthly_revenue.csv"

    result.to_csv(output_path, index=False)

    print(f"\nSaved to: {output_path}")


def category_revenue_share(df):

    print("\n" + "=" * 80)
    print("CATEGORY REVENUE SHARE")
    print("=" * 80)

    category_sales = (
        df.groupby("category")["line_total"]
        .sum()
        .reset_index()
    )

    total_sales = category_sales["line_total"].sum()

    category_sales["revenue_share_pct"] = (
        category_sales["line_total"] / total_sales * 100
    ).round(2)

    category_sales = category_sales.sort_values(
        "revenue_share_pct",
        ascending=False
    )

    print(category_sales)

    output_path = OUTPUT_DIR / "category_revenue_share.csv"

    category_sales.to_csv(output_path, index=False)

    print(f"\nSaved to: {output_path}")


def cumulative_monthly_revenue(df):

    print("\n" + "=" * 80)
    print("CUMULATIVE MONTHLY REVENUE")
    print("=" * 80)

    df["year_month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby("year_month")["line_total"]
        .sum()
        .sort_index()
        .reset_index()
    )

    monthly["cumulative_revenue"] = monthly["line_total"].cumsum()

    print(monthly)


def month_over_month_growth(df):

    print("\n" + "=" * 80)
    print("MONTH-OVER-MONTH GROWTH")
    print("=" * 80)

    df["year_month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby("year_month")["line_total"]
        .sum()
        .sort_index()
        .reset_index()
    )

    monthly["previous_month"] = monthly["line_total"].shift(1)

    monthly["growth_pct"] = (
        (
            monthly["line_total"] - monthly["previous_month"]
        )
        / monthly["previous_month"] * 100
    ).round(2)

    print(monthly)


def run_analytics():

    df = load_data()

    top_products(df)
    monthly_revenue(df)
    category_revenue_share(df)
    cumulative_monthly_revenue(df)
    month_over_month_growth(df)


if __name__ == "__main__":
    run_analytics()