# Test cases

Each row is one test function. Where a function runs with several inputs, the inputs are listed.

## Posts (`tests/test_posts.py`)

| Test | Group | What it checks | Expected |
|---|---|---|---|
| test_list_posts_returns_200_and_json | smoke | GET /posts | Status 200 and a JSON content type |
| test_response_time_is_under_five_seconds | smoke | GET /posts/1 | Responds in under 5 seconds |
| test_list_posts_returns_100_items | regression | GET /posts | 100 posts |
| test_every_post_matches_schema | contract | GET /posts | Every post has userId, id, title and body with the right types |
| test_get_post_by_id_returns_matching_post | regression | GET /posts/{id} for 1, 50, 100 | Status 200 and the same id back |
| test_filter_posts_by_user_id | regression | GET /posts?userId={id} for 1, 5, 10 | 10 posts, all with that userId |
| test_unknown_post_id_returns_404 | negative | GET /posts/{id} for 0, 101, 99999, -1, abc | Status 404 |
| test_create_post_returns_201_and_echoes_payload | regression | POST /posts | Status 201, same title, body and userId, and a numeric id |
| test_put_replaces_post_fields | regression | PUT /posts/1 | Status 200 and the body equals what was sent |
| test_patch_changes_only_the_given_field | regression | PATCH /posts/1 | Title changes, body and userId stay the same |
| test_delete_post_returns_200 | regression | DELETE /posts/1 | Status 200 |

## Users (`tests/test_users.py`)

| Test | Group | What it checks | Expected |
|---|---|---|---|
| test_list_users_returns_200 | smoke | GET /users | Status 200 |
| test_list_users_returns_10_items | regression | GET /users | 10 users |
| test_every_user_matches_schema | contract | GET /users | Every user has the required fields with the right types |
| test_get_user_by_id_returns_matching_user | regression | GET /users/{id} for 1, 2, 3 | Status 200 and the same id back |
| test_user_emails_have_a_valid_format | regression | GET /users | Every email looks like name@domain.tld |
| test_nested_user_posts_belong_to_that_user | regression | GET /users/1/posts | At least one post, each matching the post schema with userId 1 |
| test_unknown_user_returns_404 | negative | GET /users/99999 | Status 404 |

## Comments (`tests/test_comments.py`)

| Test | Group | What it checks | Expected |
|---|---|---|---|
| test_post_has_five_comments_that_point_back_to_it | regression | GET /posts/1/comments | 5 comments, each with postId 1 |
| test_every_comment_matches_schema | contract | GET /comments?postId=1 | Every comment has the required fields with the right types |
| test_filter_comments_by_post_id | regression | GET /comments?postId={id} for 1, 2 | Comments returned, all with that postId |
| test_comment_emails_have_a_valid_format | regression | GET /posts/1/comments | Every email looks like name@domain.tld |
