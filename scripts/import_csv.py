import argparse
import csv
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/courserec",
)


SUPPORTED_TABLES = {
    "courses": {
        "columns": [
            "title",
            "domain",
            "difficulty",
            "duration",
            "description",
            "url"
        ],
        "required": [
            "title",
            "domain",
            "difficulty",
            "description",
        ],
    },
    "students": {
        "columns": [
            "name",
            "email",
            "interests",
            "preferred_difficulty",
        ],
        "required": [
            "name",
            "email",
        ],
    },
}


def clean_value(value: str | None):
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def convert_course_row(row: dict) -> dict:
    duration = clean_value(row.get("duration"))

    if duration is not None:
        try:
            duration = float(duration)

            if duration.is_integer():
                duration = int(duration)

        except ValueError:
            raise ValueError(
                f"Invalid duration value: {duration!r}"
            )

    return {
        "title": clean_value(row.get("title")),
        "domain": clean_value(row.get("domain")),
        "difficulty": clean_value(row.get("difficulty")),
        "duration": duration,
        "description": clean_value(row.get("description")),
        "url": clean_value(row.get("url")),
    }


def convert_student_row(row: dict) -> dict:
    return {
        "name": clean_value(row.get("name")),
        "email": clean_value(row.get("email")),
        "interests": clean_value(row.get("interests")),
        "preferred_difficulty": clean_value(
            row.get("preferred_difficulty")
        ),
    }


def validate_columns(
    csv_columns: list[str],
    table_name: str,
) -> None:
    config = SUPPORTED_TABLES[table_name]

    missing_columns = [
        column
        for column in config["required"]
        if column not in csv_columns
    ]

    if missing_columns:
        raise ValueError(
            "CSV is missing required columns: "
            + ", ".join(missing_columns)
        )


def import_courses(connection, rows: list[dict]) -> tuple[int, int]:
    inserted = 0
    skipped = 0

    statement = text(
        """
        INSERT INTO courses (
            title,
            domain,
            difficulty,
            duration,
            description,
            url
        )
        SELECT
            :title,
            :domain,
            :difficulty,
            :duration,
            :description,
            :url
        WHERE NOT EXISTS (
            SELECT 1
            FROM courses
            WHERE LOWER(title) = LOWER(:title)
        )
        """
    )

    for row in rows:
        result = connection.execute(statement, row)

        if result.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

    return inserted, skipped


def import_students(connection, rows: list[dict]) -> tuple[int, int]:
    inserted = 0
    skipped = 0

    statement = text(
        """
        INSERT INTO students (
            name,
            email,
            interests,
            preferred_difficulty
        )
        SELECT
            :name,
            :email,
            :interests,
            :preferred_difficulty
        WHERE NOT EXISTS (
            SELECT 1
            FROM students
            WHERE LOWER(email) = LOWER(:email)
        )
        """
    )

    for row in rows:
        result = connection.execute(statement, row)

        if result.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

    return inserted, skipped


def load_csv(csv_path: Path, table_name: str) -> list[dict]:
    with csv_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError("The CSV file has no header row.")

        normalized_headers = [
            header.strip()
            for header in reader.fieldnames
        ]

        reader.fieldnames = normalized_headers

        validate_columns(normalized_headers, table_name)

        rows = []

        for line_number, raw_row in enumerate(reader, start=2):
            try:
                if table_name == "courses":
                    row = convert_course_row(raw_row)
                else:
                    row = convert_student_row(raw_row)

                missing_values = [
                    column
                    for column in SUPPORTED_TABLES[table_name]["required"]
                    if row.get(column) is None
                ]

                if missing_values:
                    print(
                        f"Skipping row {line_number}: "
                        f"missing {', '.join(missing_values)}"
                    )
                    continue

                rows.append(row)

            except ValueError as error:
                print(
                    f"Skipping row {line_number}: {error}"
                )

        return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import CSV data into CourseRec PostgreSQL."
    )

    parser.add_argument(
        "--table",
        required=True,
        choices=SUPPORTED_TABLES.keys(),
        help="Database table to populate.",
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to the CSV file.",
    )

    args = parser.parse_args()

    csv_path = Path(args.file)

    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        sys.exit(1)

    try:
        rows = load_csv(csv_path, args.table)

        if not rows:
            print("No valid rows were found in the CSV.")
            return

        engine = create_engine(DATABASE_URL)

        with engine.begin() as connection:
            if args.table == "courses":
                inserted, skipped = import_courses(
                    connection,
                    rows,
                )
            else:
                inserted, skipped = import_students(
                    connection,
                    rows,
                )

        print("\nImport completed.")
        print(f"Valid CSV rows: {len(rows)}")
        print(f"Inserted: {inserted}")
        print(f"Duplicates skipped: {skipped}")

    except SQLAlchemyError as error:
        print(f"Database error: {error}")
        sys.exit(1)

    except ValueError as error:
        print(f"CSV error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()