import pytest
from jsonschema import validate

from tests.schemas import POST_SCHEMA

NEW_POST = {"title": "qa test post", "body": "created by an automated test", "userId": 1}


@pytest.mark.smoke
def test_list_posts_returns_200_and_json(api):
    response = api.get("/posts")
    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]


@pytest.mark.smoke
def test_response_time_is_under_five_seconds(api):
    response = api.get("/posts/1")
    assert response.elapsed.total_seconds() < 5


@pytest.mark.regression
def test_list_posts_returns_100_items(api):
    assert len(api.get("/posts").json()) == 100


@pytest.mark.contract
def test_every_post_matches_schema(api):
    for post in api.get("/posts").json():
        validate(instance=post, schema=POST_SCHEMA)


@pytest.mark.regression
@pytest.mark.parametrize("post_id", [1, 50, 100])
def test_get_post_by_id_returns_matching_post(api, post_id):
    response = api.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id


@pytest.mark.regression
@pytest.mark.parametrize("user_id", [1, 5, 10])
def test_filter_posts_by_user_id(api, user_id):
    posts = api.get("/posts", params={"userId": user_id}).json()
    assert len(posts) == 10
    assert all(post["userId"] == user_id for post in posts)


@pytest.mark.negative
@pytest.mark.parametrize("post_id", [0, 101, 99999, -1, "abc"])
def test_unknown_post_id_returns_404(api, post_id):
    assert api.get(f"/posts/{post_id}").status_code == 404


@pytest.mark.regression
def test_create_post_returns_201_and_echoes_payload(api):
    response = api.post("/posts", json=NEW_POST)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == NEW_POST["title"]
    assert body["body"] == NEW_POST["body"]
    assert body["userId"] == NEW_POST["userId"]
    assert isinstance(body["id"], int)


@pytest.mark.regression
def test_put_replaces_post_fields(api):
    payload = {"id": 1, "title": "replaced title", "body": "replaced body", "userId": 1}
    response = api.put("/posts/1", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


@pytest.mark.regression
def test_patch_changes_only_the_given_field(api):
    original = api.get("/posts/1").json()
    response = api.patch("/posts/1", json={"title": "patched title"})
    assert response.status_code == 200
    patched = response.json()
    assert patched["title"] == "patched title"
    assert patched["body"] == original["body"]
    assert patched["userId"] == original["userId"]


@pytest.mark.regression
def test_delete_post_returns_200(api):
    assert api.delete("/posts/1").status_code == 200
