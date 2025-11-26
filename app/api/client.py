import os
import httpx
from dotenv import load_dotenv
from app.api.auth import AuthCredentials

load_dotenv()


class APIClient:
    def __init__(self, use_auth: bool = False):
        base_url = os.getenv("BASE_URL")
        if not base_url:
            raise ValueError("BASE_URL missing in .env")

        self.use_auth = use_auth
        self.auth = AuthCredentials() if use_auth else None

        self.client = httpx.Client(
            base_url=base_url, headers={"Content-Type": "application/json"}
        )

    def _auth_headers(self):
        if self.use_auth and self.auth:
            token = self.auth.get_token()
            return {"Authorization": f"Bearer {token}"}
        return {}

    def get(self, path, **kwargs):
        headers = kwargs.pop("headers", {})
        headers = {**self._auth_headers(), **headers}
        return self.client.get(path, headers=headers, **kwargs)

    def post(self, path, **kwargs):
        headers = kwargs.pop("headers", {})
        headers = {**self._auth_headers(), **headers}
        return self.client.post(path, headers=headers, **kwargs)

    def put(self, path, **kwargs):
        headers = kwargs.pop("headers", {})
        headers = {**self._auth_headers(), **headers}
        return self.client.put(path, headers=headers, **kwargs)

    def delete(self, path, **kwargs):
        headers = kwargs.pop("headers", {})
        headers = {**self._auth_headers(), **headers}
        return self.client.delete(path, headers=headers, **kwargs)
