from utils import normalize_text, get_keywords


def calculate_match(lost_item, found_item):
    """
    Calculate a matching score.

    Category = 30 points
    Location = 30 points
    Keywords = 40 points
    """

    score = 0

    # Category matching
    lost_category = normalize_text(
        lost_item["category"]
    )

    found_category = normalize_text(
        found_item["category"]
    )

    category_match = (
        lost_category == found_category
    )

    if category_match:
        score += 30

    # Location matching
    lost_location = normalize_text(
        lost_item["location"]
    )

    found_location = normalize_text(
        found_item["location"]
    )

    location_match = (
        lost_location == found_location
    )

    if location_match:
        score += 30

    # Keyword matching
    lost_keywords = get_keywords(
        lost_item["description"]
    )

    found_keywords = get_keywords(
        found_item["description"]
    )

    common_keywords = (
        lost_keywords.intersection(
            found_keywords
        )
    )

    all_keywords = (
        lost_keywords.union(found_keywords)
    )

    if all_keywords:

        keyword_score = (
            len(common_keywords)
            / len(all_keywords)
        ) * 40

        score += keyword_score

    # Confidence level
    if score >= 75:
        confidence = "High"

    elif score >= 50:
        confidence = "Medium"

    elif score >= 25:
        confidence = "Low"

    else:
        confidence = "Very Low"

    return {
        "lost_id": lost_item["id"],
        "found_id": found_item["id"],
        "category_match": category_match,
        "location_match": location_match,
        "common_keywords": sorted(
            common_keywords
        ),
        "score": round(score, 2),
        "confidence": confidence
    }


def find_matches(lost_item, found_items):
    """Find possible matches."""

    matches = []

    for found_item in found_items:

        if found_item["status"] != "Open":
            continue

        result = calculate_match(
            lost_item,
            found_item
        )

        if result["score"] >= 25:
            matches.append(result)

    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return matches