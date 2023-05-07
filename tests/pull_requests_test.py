import pytest

from configs import MAIN_BRANCH
from services.github_service import GitHubRestApi
from utils.faker import random_str


def test_create_pull_request(user_data, repository, branch_for_repo_with_commit):
    branch, _ = branch_for_repo_with_commit
    gh_service = GitHubRestApi()

    pr_title = random_str()
    res = gh_service.create_pull_request(user_data["login"], repository["name"], branch["ref"], MAIN_BRANCH, pr_title)

    assert res.status_code == 201
    res = res.json()

    assert res["title"] == pr_title
    assert res["base"]["ref"] == MAIN_BRANCH
    assert res["head"]["ref"] == branch["ref"].split("/")[-1]


def test_create_pull_request_same_tree(user_data, repository, branch_for_repo):
    gh_service = GitHubRestApi()

    pr_title = random_str()
    res = gh_service.create_pull_request(user_data["login"], repository["name"], branch_for_repo["ref"], MAIN_BRANCH,
                                         pr_title)

    assert res.status_code == 422


def test_list_pull_requests(user_data, repository, open_pull_request):
    gh_service = GitHubRestApi()
    res = gh_service.list_pull_requests(user_data["login"], repository["name"])

    assert res.status_code == 200

    act_pr = None
    for pr in res.json():
        if pr["title"] == open_pull_request["title"]:
            act_pr = pr
            break

    assert act_pr
    assert act_pr["base"]["ref"] == open_pull_request["base"]["ref"]
    assert act_pr["head"]["ref"] == open_pull_request["head"]["ref"]


def test_list_pull_requests_fake_repo(user_data):
    gh_service = GitHubRestApi()
    res = gh_service.list_pull_requests(user_data["login"], random_str())

    assert res.status_code == 404


def test_close_pull_request(user_data, repository, open_pull_request):
    gh_service = GitHubRestApi()

    new_state = "closed"
    res = gh_service.update_pull_request(user_data["login"], repository["name"], open_pull_request["number"], new_state)
    assert res.status_code == 200

    res = res.json()
    assert res["state"] == new_state


def test_update_pr_wrong_state(user_data, repository, open_pull_request):
    gh_service = GitHubRestApi()

    res = gh_service.update_pull_request(user_data["login"], repository["name"], open_pull_request["number"],
                                         random_str())
    assert res.status_code == 200
    assert res.json()["state"] == "open"


@pytest.mark.skip("TODO: currently failing because of 'cannot review own pull request' validation")
def test_approve_pull_request(user_data, repository, open_pull_request):
    gh_service = GitHubRestApi()

    result = "APPROVE"
    res = gh_service.create_pr_review(user_data["login"], repository["name"], open_pull_request["number"], result)
    assert res.status_code == 200
