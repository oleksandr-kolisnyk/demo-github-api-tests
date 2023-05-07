import base64

import pytest

from configs import MAIN_BRANCH
from services.github_service import GitHubRestApi
from utils.faker import random_str


@pytest.fixture(scope="function")
def branch_for_repo(repository, user_data):
    gh_service = GitHubRestApi()
    branches = gh_service.list_branches(user_data["login"], repository["name"]).json()
    sha_value = [branch["commit"]["sha"] for branch in branches if branch["name"] == MAIN_BRANCH][0]

    res = gh_service.create_reference(user_data["login"], repository["name"], f"refs/heads/{random_str()}", sha_value)
    assert res.status_code == 201
    return res.json()


@pytest.fixture(scope="function")
def branch_for_repo_with_commit(repository, user_data):
    gh_service = GitHubRestApi()
    branches = gh_service.list_branches(user_data["login"], repository["name"]).json()
    sha_value = branches[0]["commit"]["sha"]

    branch_name = random_str()
    res = gh_service.create_reference(user_data["login"], repository["name"], f"refs/heads/{branch_name}", sha_value)
    assert res.status_code == 201

    contents = base64.b64encode(bytes(random_str(150), "utf-8")).decode("utf-8")
    res_commit = gh_service.create_content(user_data["login"], repository["name"], random_str(), random_str(15),
                                           contents, branch_name)

    assert res_commit.status_code == 201
    return res.json(), res_commit.json()
