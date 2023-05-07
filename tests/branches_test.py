from services.github_service import GitHubRestApi


def test_list_branches(user_data, repository, branch_for_repo):
    gh_service = GitHubRestApi()
    res = gh_service.list_branches(user_data["login"], repository["name"])

    assert res.status_code == 200
    assert len(res.json()) > 0

    names = [b["name"] for b in res.json()]
    exp_branch_name = branch_for_repo["ref"].split("/")[-1]
    assert exp_branch_name in names


def test_list_branches_no_result(user_data, repository_no_init):
    gh_service = GitHubRestApi()
    res = gh_service.list_branches(user_data["login"], repository_no_init["name"])

    assert res.status_code == 200
    assert len(res.json()) == 0
