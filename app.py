from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from utils import (
    load_data,
    save_data,
    validate_report,
    generate_id
)

from matcher import find_matches


app = Flask(__name__)


@app.route("/")
def index():

    data = load_data()

    return render_template(
        "index.html",
        data=data
    )


@app.route("/report/<report_type>", methods=["GET", "POST"])
def report(report_type):

    if report_type not in ["lost", "found"]:
        return "Invalid report type", 404

    error = None

    if request.method == "POST":

        data = load_data()

        item = {
            "category": request.form.get(
                "category",
                ""
            ).strip(),

            "description": request.form.get(
                "description",
                ""
            ).strip(),

            "location": request.form.get(
                "location",
                ""
            ).strip(),

            "date": request.form.get(
                "date",
                ""
            ).strip(),

            "status": "Open"
        }

        valid, message = validate_report(item)

        if not valid:

            error = message

        else:

            item["id"] = generate_id(
                report_type,
                data[report_type]
            )

            data[report_type].append(item)

            save_data(data)

            return redirect(
                url_for("index")
            )

    return render_template(
        "report.html",
        report_type=report_type,
        error=error
    )


@app.route("/search")
def search():

    data = load_data()

    category = request.args.get(
        "category",
        ""
    ).strip().lower()

    location = request.args.get(
        "location",
        ""
    ).strip().lower()

    results = []

    for report_type in ["lost", "found"]:

        for item in data[report_type]:

            category_match = (
                not category
                or item["category"].lower()
                == category
            )

            location_match = (
                not location
                or item["location"].lower()
                == location
            )

            if category_match and location_match:

                results.append({
                    "type": report_type,
                    "item": item
                })

    return render_template(
        "search.html",
        results=results,
        category=category,
        location=location
    )


@app.route("/matches/<lost_id>")
def matches(lost_id):

    data = load_data()

    lost_item = next(
        (
            item
            for item in data["lost"]
            if item["id"] == lost_id
        ),
        None
    )

    if not lost_item:
        return "Lost report not found", 404

    possible_matches = find_matches(
        lost_item,
        data["found"]
    )

    return render_template(
        "matches.html",
        lost_item=lost_item,
        matches=possible_matches
    )


@app.route("/status/<report_id>", methods=["POST"])
def update_status_web(report_id):

    status = request.form.get("status")

    allowed_statuses = [
        "Open",
        "Matched",
        "Returned"
    ]

    if status not in allowed_statuses:
        return "Invalid status", 400

    data = load_data()

    for report_type in ["lost", "found"]:

        for item in data[report_type]:

            if item["id"] == report_id:

                item["status"] = status

                save_data(data)

                return redirect(
                    url_for("index")
                )

    return "Report not found", 404


if __name__ == "__main__":
    app.run(
        debug=True
    )