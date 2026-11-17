# Test plan

## Purpose
Check that the JSONPlaceholder REST API behaves as documented for posts, users and comments, and keep those checks running automatically.

## In scope
- Reading lists and single items for posts, users and comments
- Filtering with query strings and reading nested routes
- Creating, replacing, partly updating and deleting posts
- Error responses for ids that do not exist or are not valid
- The structure of response bodies
- Basic response time

## Out of scope
- Load and stress testing
- Security testing
- Checking that written data is stored, because the API does not store it
- Any browser or screen testing

## Approach
- Every test sends a real HTTP request and checks the status code, headers and body.
- Tests are grouped with markers (smoke, regression, negative, contract) so a group can run alone.
- Tests that need several inputs use pytest parametrisation, so one function covers many ids.
- Response structure is checked with JSON schemas, which catch a missing or retyped field.
- Each test is independent. None of them depends on another having run first.

## Environment
- Python 3.12 on GitHub Actions, any recent Python 3.10 or later on a laptop
- pytest, requests, jsonschema, pytest-html, ruff
- Target server set by the `BASE_URL` environment variable, default `https://jsonplaceholder.typicode.com`

## Entry and exit
- Start: the target API answers on the base URL.
- Finish: all smoke tests pass first, then the full suite passes, and the HTML report is saved.

## Risks
| Risk | Effect | How it is handled |
|---|---|---|
| The public API is slow or down | Runs fail for reasons unrelated to the tests | Ten second timeout on every request, and a smoke run first so the cause is obvious |
| The API changes its data | Count based tests such as "100 posts" fail | The expected numbers are written in one place per test, so they are easy to update |
| The API blocks automated clients | Requests return 403 in CI | A clear User-Agent is sent, and `BASE_URL` lets the suite point at another server |

## Reporting
A self contained HTML report is built on every run and saved as a build artifact on GitHub.
