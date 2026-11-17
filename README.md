# API Test Automation with pytest

[![API tests](https://github.com/SidhanthChavan/api-test-automation-pytest/actions/workflows/tests.yml/badge.svg)](https://github.com/SidhanthChavan/api-test-automation-pytest/actions/workflows/tests.yml)

This repository holds a set of automated tests for a public REST API. They are written in Python with pytest and requests, and GitHub Actions runs them every time the code changes.

I built it to practise testing an API the way a QA team would. That means checking that good requests work, that bad requests fail the way they should, and that the shape of every response stays the same. It also means the checks run on their own, so nobody has to remember to run them.

The API under test is [JSONPlaceholder](https://jsonplaceholder.typicode.com), a free service made for practice and prototypes.

## What the tests cover

There are 33 tests in four groups, marked so you can run any group on its own.

| Marker | What it is for | Example |
|---|---|---|
| `smoke` | Quick check that the API is up | `/posts` returns 200 and JSON |
| `regression` | Behaviour that should not change | Creating a post returns 201 and echoes the data back |
| `negative` | Bad input and error responses | Post ids 0, 101, 99999, -1 and "abc" all return 404 |
| `contract` | The structure of responses | Every post, comment and user matches a JSON schema |

The tests also check filtering (`/posts?userId=1`), nested routes (`/users/1/posts`), email formats, and that related ids such as `postId` and `userId` point to the right parent.

The full list of cases is in [docs/test-cases.md](docs/test-cases.md), and the reasoning behind them is in [docs/test-plan.md](docs/test-plan.md).

## Running the tests

You need Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                           # everything
pytest -m smoke                  # only the quick checks
pytest -m "negative or contract" # pick groups with markers
```

To get an HTML report you can open in a browser:

```bash
pytest --html=report.html --self-contained-html
```

To point the tests at a different server, set `BASE_URL`:

```bash
BASE_URL=http://localhost:8000 pytest
```

## What happens on GitHub

The workflow in `.github/workflows/tests.yml` runs on every push to `main`, on every pull request, and on demand. It does four things in order:

1. Checks the code style with ruff.
2. Runs the smoke tests, so a broken API fails fast.
3. Runs the full suite and builds the HTML report.
4. Saves the report as a downloadable file on the run page, even when a test fails.

## Project layout

```
tests/
  conftest.py         API client shared by every test
  schemas.py          JSON schemas used by the contract tests
  test_posts.py       posts: smoke, create/update/delete, negative cases, filtering
  test_users.py       users: schema, lookups, email format, nested posts
  test_comments.py    comments: parent ids, filtering, email format
docs/
  test-plan.md        scope, approach, risks
  test-cases.md       every test case in plain words
.github/workflows/
  tests.yml           the pipeline described above
```

## Things to know

- JSONPlaceholder accepts POST, PUT, PATCH and DELETE but does not save anything. The tests for those requests check the response only. They cannot check that data was stored, because it never is.
- The tests talk to a real server over the internet, so a slow connection or an outage on the other side can fail a run. A failed run with connection errors usually means the API was unreachable, not that the tests are wrong.
- This is a practice project. It shows how I structure and automate API checks, and it is not a test suite for a production system.

## Licence

MIT. See [LICENSE](LICENSE).
