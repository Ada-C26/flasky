def test_get_all_cats_returns_empty_list_when_db_is_empty(client):
    # act
    response = client.get("/cats")

    # assert
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_all_cats_returns_one_cat_when_present(client, one_cat):
    # act
    response = client.get("/cats")
    cats = response.get_json()

    # assert
    assert response.status_code == 200
    assert len(cats) == 1

    cat = cats[0]
    assert cat["id"] == one_cat.id
    assert cat["name"] == one_cat.name
    assert cat["personality"] == one_cat.personality
    assert cat["color"] == one_cat.color

def test_get_one_cat_returns_one_cat_when_present(client, one_cat):
    # act
    response = client.get(f"/cats/{one_cat.id}")
    cat = response.get_json()

    # assert
    assert response.status_code == 200
    assert cat["id"] == one_cat.id
    assert cat["name"] == one_cat.name
    assert cat["personality"] == one_cat.personality
    assert cat["color"] == one_cat.color


def test_create_cat_successfully(client):
    # arrange
    EXPECTED_CAT = {
        "name": "Luna",
        "color": "black",
        "personality": "wise"
    }

    # act
    response = client.post("/cats", json=EXPECTED_CAT)
    response_body = response.get_json()

    # assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["name"] == EXPECTED_CAT["name"]
    assert response_body["color"] == EXPECTED_CAT["color"]
    assert response_body["personality"] == EXPECTED_CAT["personality"]

