import pytest

from services.github_service import GitHubRestApi
from utils.faker import random_str


@pytest.fixture(scope="session")
def repository(user_data):
    gh_service = GitHubRestApi()
    res = gh_service.create_repository(random_str(), random_str(20), True)
    assert res.status_code == 201
    res = res.json()
    yield res
    res = gh_service.delete_repository(user_data["login"], res["name"])
    assert res.status_code == 204
