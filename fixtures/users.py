import pytest

from services.github_service import GitHubRestApi


@pytest.fixture(scope="session")
def user_data():
    gh_service = GitHubRestApi()
    res = gh_service.get_user_data()
    assert res.status_code == 200
    return res.json()
