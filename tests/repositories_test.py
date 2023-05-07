import pytest

from services.github_service import GitHubRestApi
from utils.faker import random_str


def test_list_repositories(repository):
    gh_service = GitHubRestApi()
    res = gh_service.list_repositories()

    assert res.status_code == 200
    res = res.json()

    repo = None
    for r in res:
        if r["name"] == repository["name"]:
            repo = r
            break

    assert repo
    assert repo["description"] == repository["description"]
    assert repo["has_issues"] == repository["has_issues"]


@pytest.fixture(scope="function")
def repository_func(user_data):
    gh_service = GitHubRestApi()
    res = gh_service.create_repository(random_str(), random_str(20), True)
    assert res.status_code == 201
    res = res.json()
    return res


def test_delete_repository(repository_func, user_data):
    gh_service = GitHubRestApi()
    res = gh_service.delete_repository(user_data["login"], repository_func["name"])

    assert res.status_code == 204

    # get repositories again and verify that deleted repo is not on the list
    res = gh_service.list_repositories().json()
    names = [r["name"] for r in res]
    assert repository_func["name"] not in names


def test_delete_non_existing_repo(user_data):
    gh_service = GitHubRestApi()
    res = gh_service.delete_repository(user_data["login"], random_str(15))

    assert res.status_code == 404
