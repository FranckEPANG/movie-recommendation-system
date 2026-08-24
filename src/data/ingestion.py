from pathlib import Path
from zipfile import ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
INTERIM_DATA_DIR = PROJECT_ROOT / "data" / "interim"

DATASET_ARCHIVE = RAW_DATA_DIR / "ml-32m.zip"

EXPECTED_FILES = {
    "ratings.csv",
    "movies.csv",
    "tags.csv",
    "links.csv",
    "README.txt",
}


def extract_dataset() -> Path:
    """Extract the MovieLens dataset into the interim data directory."""

    if not DATASET_ARCHIVE.exists():
        raise FileNotFoundError(
            f"Dataset archive not found: {DATASET_ARCHIVE}"
        )

    INTERIM_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with ZipFile(DATASET_ARCHIVE, "r") as zip_file:
        zip_file.extractall(INTERIM_DATA_DIR)

    return INTERIM_DATA_DIR


def validate_dataset(extracted_directory: Path) -> None:
    """Validate that all expected MovieLens files are available."""

    dataset_directory = extracted_directory / "ml-32m"

    if not dataset_directory.exists():
        raise FileNotFoundError(
            f"Expected dataset directory not found: {dataset_directory}"
        )

    missing_files = {
        file_name
        for file_name in EXPECTED_FILES
        if not (dataset_directory / file_name).exists()
    }

    if missing_files:
        raise FileNotFoundError(
            f"Missing expected files: {sorted(missing_files)}"
        )


def main() -> None:
    """Run the MovieLens ingestion pipeline."""

    print("Starting MovieLens dataset ingestion...")
    extracted_directory = extract_dataset()
    print(f"Dataset extracted to: {extracted_directory}")
    validate_dataset(extracted_directory)
    print("Dataset validation successful.")


if __name__ == "__main__":
    main()