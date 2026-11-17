import re

import pytest
from jsonschema import validate

from tests.schemas import COMMENT_SCHEMA

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@pytest.mark.regression
def test_post_has_five_comments_that_point_back_to_it(api):
    comments = api.get("/posts/1/comments").json()
    assert len(comments) == 5
    assert all(comment["postId"] == 1 for comment in comments)


@pytest.mark.contract
def test_every_comment_matches_schema(api):
    for comment in api.get("/comments", params={"postId": 1}).json():
        validate(instance=comment, schema=COMMENT_SCHEMA)


@pytest.mark.regression
@pytest.mark.parametrize("post_id", [1, 2])
def test_filter_comments_by_post_id(api, post_id):
    comments = api.get("/comments", params={"postId": post_id}).json()
    assert comments
    assert all(comment["postId"] == post_id for comment in comments)


@pytest.mark.regression
def test_comment_emails_have_a_valid_format(api):
    for comment in api.get("/posts/1/comments").json():
        assert EMAIL_PATTERN.match(comment["email"]), comment["email"]
