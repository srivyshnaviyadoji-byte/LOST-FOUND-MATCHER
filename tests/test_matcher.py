from matcher import calculate_match


def test_perfect_match():

    lost_item = {
        "id": "L101",
        "category": "Electronics",
        "description": "Black wireless earbuds",
        "location": "Metro Station",
        "date": "2026-09-15",
        "status": "Open"
    }

    found_item = {
        "id": "F205",
        "category": "Electronics",
        "description": "Black wireless earbuds",
        "location": "Metro Station",
        "date": "2026-09-15",
        "status": "Open"
    }

    result = calculate_match(
        lost_item,
        found_item
    )

    assert result["category_match"] is True
    assert result["location_match"] is True
    assert result["score"] == 100