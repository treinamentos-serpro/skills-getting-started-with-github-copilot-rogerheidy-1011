import pytest


def get_participants(client, activity_name):
    return client.get("/activities").json()[activity_name]["participants"]


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Art Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in get_participants(client, activity_name)


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Underwater Basket Weaving"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_when_student_already_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    participants_before = list(get_participants(client, activity_name))

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    assert get_participants(client, activity_name) == participants_before


def test_signup_allows_same_student_in_different_activities(client):
    # Arrange
    first_activity = "Art Club"
    second_activity = "Drama Club"
    email = "new.student@mergington.edu"
    client.post(f"/activities/{first_activity}/signup", params={"email": email})

    # Act
    response = client.post(f"/activities/{second_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in get_participants(client, second_activity)


def test_signup_returns_422_when_email_is_missing(client):
    # Arrange
    activity_name = "Art Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


@pytest.mark.xfail(reason="API does not enforce max_participants yet", strict=True)
def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    max_participants = client.get("/activities").json()[activity_name]["max_participants"]
    for i in range(max_participants - len(get_participants(client, activity_name))):
        client.post(f"/activities/{activity_name}/signup", params={"email": f"filler{i}@mergington.edu"})

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "late.student@mergington.edu"}
    )

    # Assert
    assert response.status_code == 400
