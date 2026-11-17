import os

import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com").rstrip("/")
TIMEOUT_SECONDS = 10


class ApiClient:
    """Small wrapper so every test uses the same base URL, headers and timeout."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "api-test-automation-pytest/1.0"})

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", TIMEOUT_SECONDS)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)


@pytest.fixture(scope="session")
def api() -> ApiClient:
    return ApiClient(BASE_URL)
