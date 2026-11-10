def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_static_index_is_served(client):
    # Arrange
    path = "/static/index.html"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
