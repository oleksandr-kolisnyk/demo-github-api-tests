import pytest

from configs import MAIN_BRANCH
from services.github_service import GitHubRestApi
from utils.faker import random_str


@pytest.fixture()
def open_pull_request(user_data, repository, branch_for_repo_with_commit):
    branch, _ = branch_for_repo_with_commit
    gh_service = GitHubRestApi()

    res = gh_service.create_pull_request(user_data["login"], repository["name"], branch["ref"], MAIN_BRANCH,
                                         random_str())

    assert res.status_code == 201
    return res.json()
