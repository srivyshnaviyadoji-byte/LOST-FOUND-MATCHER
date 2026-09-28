import json
import os
import re
from datetime import datetime


DATA_FILE = "data.json"


def load_data():
    """Load data from the JSON file."""

    if not os.path.exists(DATA_FILE):
        return {
            "lost": [],
            "found": []
        }

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    """Save data to the JSON file."""

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def normalize_text(text):
    """Convert text to lowercase and clean extra spaces."""

    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_keywords(text):
    """Convert description into a set of keywords."""

    text = normalize_text(text)

    words = re.findall(r"[a-zA-Z0-9]+", text)

    return set(words)


def validate_date(date_string):
    """Validate YYYY-MM-DD date format."""

    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True

    except ValueError:
        return False


def validate_report(report):
    """Validate required fields."""

    required_fields = [
        "category",
        "description",
        "location",
        "date"
    ]

    for field in required_fields:

        if not report.get(field):
            return False, f"{field} is required."

    if not validate_date(report["date"]):
        return False, "Date must be in YYYY-MM-DD format."

    return True, "Valid"


def generate_id(report_type, existing_reports):
    """Generate a unique report ID."""

    if report_type == "lost":
        prefix = "L"
    else:
        prefix = "F"

    numbers = []

    for report in existing_reports:

        report_id = report.get("id", "")

        if report_id.startswith(prefix):

            try:
                numbers.append(
                    int(report_id[1:])
                )

            except ValueError:
                pass

    next_number = max(numbers, default=100) + 1

    return f"{prefix}{next_number}"