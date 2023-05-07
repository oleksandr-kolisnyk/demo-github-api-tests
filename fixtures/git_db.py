import pytest

from services.github_service import GitHubRestApi
from utils.faker import random_str


@pytest.fixture(scope="function")
def branch_for_repo(repository, user_data):
    gh_service = GitHubRestApi()
    branches = gh_service.list_branches(user_data["login"], repository["name"]).json()
    sha_value = branches[0]["commit"]["sha"]

    res = gh_service.create_reference(user_data["login"], repository["name"], f"refs/heads/{random_str()}", sha_value)
    assert res.status_code == 201
    return res.json()
