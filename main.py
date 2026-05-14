from src.transform import run_transformation_pipeline
from src.quality_checks import run_quality_checks
from src.analytics import run_analytics


def run_pipeline():

    print("=" * 80)
    print("PIPELINE STARTED")
    print("=" * 80)

    print("\nSTEP 1: DATA TRANSFORMATION")
    run_transformation_pipeline()

    print("\nSTEP 2: DATA QUALITY CHECKS")
    run_quality_checks()

    print("\nSTEP 3: ANALYTICS")
    run_analytics()

    print("\n" + "=" * 80)
    print("PIPELINE FINISHED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()