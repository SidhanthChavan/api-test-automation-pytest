import re

import pytest
from jsonschema import validate

from tests.schemas import POST_SCHEMA, USER_SCHEMA

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@pytest.mark.smoke
def test_list_users_returns_200(api):
    assert api.get("/users").status_code == 200


@pytest.mark.regression
def test_list_users_returns_10_items(api):
    assert len(api.get("/users").json()) == 10


@pytest.mark.contract
def test_every_user_matches_schema(api):
    for user in api.get("/users").json():
        validate(instance=user, schema=USER_SCHEMA)


@pytest.mark.regression
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_by_id_returns_matching_user(api, user_id):
    response = api.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.regression
def test_user_emails_have_a_valid_format(api):
    for user in api.get("/users").json():
        assert EMAIL_PATTERN.match(user["email"]), user["email"]


@pytest.mark.regression
def test_nested_user_posts_belong_to_that_user(api):
    posts = api.get("/users/1/posts").json()
    assert posts, "expected at least one post for user 1"
    for post in posts:
        validate(instance=post, schema=POST_SCHEMA)
        assert post["userId"] == 1


@pytest.mark.negative
def test_unknown_user_returns_404(api):
    assert api.get("/users/99999").status_code == 404
