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

    def _make_delete(self, url):
        return self._make_request(requests.delete, url)

    def get_user_data(self):
        return self._make_get("user")

    def create_repository(self, name, description, has_issues):
        body = {"name": name, "description": description, "has_issues": has_issues}
        return self._make_post("/user/repos", body)

    def delete_repository(self, owner, repo_name):
        return self._make_delete(f"/repos/{owner}/{repo_name}")

    def list_repositories(self):
        return self._make_get("user/repos")


class GitHubRestApiGuest(GitHubRestApi):

    def __init__(self):
        super().__init__()
        self._auth_headers = {}