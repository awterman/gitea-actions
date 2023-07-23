import requests

class Gitea:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token

    def request(self, method: str, path: str, **kwargs):
        return requests.request(
            method,
            f"{self.url}{path}",
            headers={"Authorization": f"token {self.token}"},
            **kwargs,
        )

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def create_release(self, repo: str, tag_name: str, name: str):
        body = f"Release for version {tag_name}"
        resp = self.post(
            f"/repos/{repo}/releases",
            json={
                "tag_name": tag_name,
                "name": name,
                "body": body,
            },
        )
        resp.raise_for_status()
        return resp.json()["id"]

    def upload_asset(self, repo: str, release_id: int, file_path: str):
        resp = self.post(
            f"/repos/{repo}/releases/{release_id}/assets",
            files={"attachment": open(file_path, "rb")},
        )
        resp.raise_for_status()

    def delete_release(self, repo: str, tag_name: str):
        resp = self.request(
            "DELETE",
            f"/repos/{repo}/releases/tags/{tag_name}",
        )
        resp.raise_for_status()