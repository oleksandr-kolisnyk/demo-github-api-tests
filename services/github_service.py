from urllib.parse import urljoin

import requests

from configs import GH_PAT, GH_API_VER, GH_URI
from utils.logger import logger


class GitHubRestApi:

    BASE_URI = GH_URI

    def __init__(self, token=GH_PAT):
        self._token = token
        self._auth_headers = {"Authorization": f"Bearer {self._token}"}
        self._common_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GH_API_VER
        }

    def _create_headers(self):
        headers = self._auth_headers.copy()
        headers.update(self._common_headers)
        return headers

    def _make_request(self, method, url, body=None):
        logger.info(f"{method.__name__.upper()} {url} . Body: {body}")
        res = method(urljoin(self.BASE_URI, url), json=body, headers=self._create_headers())
        logger.info(f"Response status {res.status_code}. Response body: {res.text}")
        return res

    def _make_get(self, url):
        return self._make_request(requests.get, url)

    def _make_post(self, url, body):
        return self._make_request(requests.post, url, body)

    def _make_put(self, url, body):
        return self._make_request(requests.put, url, body)

    def _make_patch(self, url, body):
        return self._make_request(requests.patch, url, body)

    def _make_delete(self, url):
        return self._make_request(requests.delete, url)

    def get_user_data(self):
        return self._make_get("user")

    def create_repository(self, name, description, has_issues, auto_init=False):
        body = {"name": name, "description": description, "has_issues": has_issues, "auto_init": auto_init}
        return self._make_post("/user/repos", body)

    def delete_repository(self, owner, repo_name):
        return self._make_delete(f"/repos/{owner}/{repo_name}")

    def list_repositories(self):
        return self._make_get("user/repos")

    def list_branches(self, owner, repo_name):
        return self._make_get(f"/repos/{owner}/{repo_name}/branches")

    def create_reference(self, owner, repo_name, ref_name, sha1_value):
        body = {"ref": ref_name, "sha": sha1_value}
        url = f"/repos/{owner}/{repo_name}/git/refs"
        return self._make_post(url, body)

    def create_content(self, owner, repo_name, file_path, message, content, branch):
        body = {"message": message, "content": content, "branch": branch}
        url = f"/repos/{owner}/{repo_name}/contents/{file_path}"
        return self._make_put(url, body)

    def create_pull_request(self, owner, repo_name, head, base, title=None):
        body = {"head": head, "base": base, "title": title}
        url = f"/repos/{owner}/{repo_name}/pulls"
        return self._make_post(url, body)

    def list_pull_requests(self, owner, repo_name):
        url = f"/repos/{owner}/{repo_name}/pulls"
        return self._make_get(url)

    def update_pull_request(self, owner, repo_name, pr_number, state):
        body = {"state": state}
        url = f"/repos/{owner}/{repo_name}/pulls/{pr_number}"
        return self._make_patch(url, body)


class GitHubRestApiGuest(GitHubRestApi):

    def __init__(self):
        super().__init__()
        self._auth_headers = {}
