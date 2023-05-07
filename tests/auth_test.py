from services.github_service import GitHubRestApiGuest, GitHubRestApi
from utils.faker import random_str


def test_no_auth_header():
    gh_guest = GitHubRestApiGuest()
    res = gh_guest.get_user_data()

    assert res.status_code == 401


def test_fake_token():
    gh_service = GitHubRestApi(random_str(50))
    res = gh_service.get_user_data()

    assert res.status_code == 401
