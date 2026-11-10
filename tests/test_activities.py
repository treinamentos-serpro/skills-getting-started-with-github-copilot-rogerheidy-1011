def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_count = 9

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == expected_count


def test_get_activities_includes_expected_fields(client):
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    for name, details in response.json().items():
        assert expected_fields <= details.keys(), name
        assert isinstance(details["participants"], list), name


def test_get_activities_includes_seeded_participants(client):
    # Arrange
    activity_name = "Chess Club"
    expected_participant = "michael@mergington.edu"

    # Act
    response = client.get("/activities")

    # Assert
    assert expected_participant in response.json()[activity_name]["participants"]
