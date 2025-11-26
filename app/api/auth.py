import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv()


class AuthCredentials:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.auth_url = os.getenv("AUTH_URL")

        if not all([self.client_id, self.client_secret, self.auth_url]):
            raise ValueError("Missing CLIENT_ID, CLIENT_SECRET, or AUTH_URL in .env")

        self.access_token = None
        self.expires_at = 0

    def _request_new_token(self):
        response = httpx.post(
            self.auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        response.raise_for_status()
        data = response.json()

        self.access_token = data["access_token"]
        self.expires_at = time.time() + data.get("expires_in", 1800) - 60

    def get_token(self):
        if not self.access_token or time.time() >= self.expires_at:
            self._request_new_token()
        return self.access_token
