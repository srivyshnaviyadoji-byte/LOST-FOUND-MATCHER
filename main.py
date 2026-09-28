from utils import (
    load_data,
    save_data,
    validate_report,
    generate_id
)

from matcher import find_matches


def register_item(report_type):
    """Register a lost or found item."""

    data = load_data()

    print("\n-----------------------------")
    print(f" Register {report_type.upper()} Item")
    print("-----------------------------")

    category = input("Category: ").strip()
    description = input("Description: ").strip()
    location = input("Location: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()

    report = {
        "category": category,
        "description": description,
        "location": location,
        "date": date,
        "status": "Open"
    }

    valid, message = validate_report(report)

    if not valid:
        print(f"\nError: {message}")
        return

    report["id"] = generate_id(
        report_type,
        data[report_type]
    )

    data[report_type].append(report)

    save_data(data)

    print("\nItem registered successfully.")
    print(f"Report ID: {report['id']}")


def search_items():
    """Search lost and found items."""

    data = load_data()

    category = input(
        "Category (leave blank for all): "
    ).strip().lower()

    location = input(
        "Location (leave blank for all): "
    ).strip().lower()

    results = []

    for report_type in ["lost", "found"]:

        for item in data[report_type]:

            category_match = (
                not category
                or item["category"].lower() == category
            )

            location_match = (
                not location
                or item["location"].lower() == location
            )

            if category_match and location_match:
                results.append(
                    (report_type, item)
                )

    print("\n========== SEARCH RESULTS ==========")

    if not results:
        print("No matching records found.")
        return

    for report_type, item in results:

        print(
            f"\n[{report_type.upper()}]"
        )

        print(f"ID: {item['id']}")
        print(f"Category: {item['category']}")
        print(f"Description: {item['description']}")
        print(f"Location: {item['location']}")
        print(f"Date: {item['date']}")
        print(f"Status: {item['status']}")


def show_matches():
    """Display possible matches."""

    data = load_data()

    lost_items = [
        item
        for item in data["lost"]
        if item["status"] == "Open"
    ]

    if not lost_items:
        print("\nNo open lost reports.")
        return

    print("\n========== LOST ITEMS ==========")

    for item in lost_items:

        print(
            f"{item['id']} - "
            f"{item['category']} - "
            f"{item['description']}"
        )

    lost_id = input(
        "\nEnter Lost Report ID: "
    ).strip()

    lost_item = next(
        (
            item
            for item in lost_items
            if item["id"] == lost_id
        ),
        None
    )

    if not lost_item:
        print("Lost report not found.")
        return

    matches = find_matches(
        lost_item,
        data["found"]
    )

    print("\n========== POSSIBLE MATCHES ==========")

    if not matches:
        print("No possible matches found.")
        return

    for match in matches:

        print("\n-----------------------------")

        print(
            f"Lost Report: "
            f"{match['lost_id']}"
        )

        print(
            f"Found Report: "
            f"{match['found_id']}"
        )

        print(
            f"Category Match: "
            f"{'Yes' if match['category_match'] else 'No'}"
        )

        print(
            f"Location Match: "
            f"{'Yes' if match['location_match'] else 'No'}"
        )

        print(
            f"Common Keywords: "
            f"{', '.join(match['common_keywords'])}"
        )

        print(
            f"Confidence Score: "
            f"{match['score']}%"
        )

        print(
            f"Confidence: "
            f"{match['confidence']}"
        )


def update_status():
    """Update report status."""

    data = load_data()

    report_id = input(
        "\nEnter report ID: "
    ).strip()

    report = None

    for report_type in ["lost", "found"]:

        for item in data[report_type]:

            if item["id"] == report_id:
                report = item
                break

    if not report:
        print("Report not found.")
        return

    print("\nAvailable statuses:")

    print("1. Open")
    print("2. Matched")
    print("3. Returned")

    choice = input(
        "Choose status: "
    ).strip()

    statuses = {
        "1": "Open",
        "2": "Matched",
        "3": "Returned"
    }

    if choice not in statuses:
        print("Invalid status.")
        return

    report["status"] = statuses[choice]

    save_data(data)

    print(
        f"Status updated to {report['status']}."
    )


def show_open_reports():
    """Display all open reports."""

    data = load_data()

    print("\n========== OPEN REPORTS ==========")

    found_any = False

    for report_type in ["lost", "found"]:

        for item in data[report_type]:

            if item["status"] == "Open":

                found_any = True

                print(
                    f"\n[{report_type.upper()}]"
                )

                print(f"ID: {item['id']}")
                print(
                    f"Category: "
                    f"{item['category']}"
                )

                print(
                    f"Description: "
                    f"{item['description']}"
                )

                print(
                    f"Location: "
                    f"{item['location']}"
                )

                print(f"Date: {item['date']}")

    if not found_any:
        print("No open reports.")


def main():

    while True:

        print("\n")
        print("===================================")
        print("       LOST & FOUND MATCHER")
        print("===================================")

        print("1. Register Lost Item")
        print("2. Register Found Item")
        print("3. Search Items")
        print("4. Find Possible Matches")
        print("5. Update Status")
        print("6. Show Open Reports")
        print("7. Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            register_item("lost")

        elif choice == "2":
            register_item("found")

        elif choice == "3":
            search_items()

        elif choice == "4":
            show_matches()

        elif choice == "5":
            update_status()

        elif choice == "6":
            show_open_reports()

        elif choice == "7":
            print("eka selavu")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()