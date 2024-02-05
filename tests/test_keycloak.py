import unittest
from unittest import mock

import requests
from argo_probe_keycloak.keycloak import fetch_keycloak_token

mock_data = {
    'access_token': 'mock-access-token',
    'expires_in': 600,
    'refresh_expires_in': 14400,
    'refresh_token': 'mock-refresh-token',
    'token_type': 'bearer',
    'not-before-policy': 0
}


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

        if str(self.status_code).startswith("2"):
            self.reason = "OK"

        else:
            self.reason = "SERVER ERROR"

    def raise_for_status(self):
        if not str(self.status_code).startswith("2"):
            raise requests.exceptions.RequestException(
                f"{self.status_code} {self.reason}"
            )

    def json(self):
        return self.data


class KeycloakTests(unittest.TestCase):
    def setUp(self):
        self.args = {
            "endpoint": "https://mock.keycloak.url/openid-connect/token/",
            "client_id": "mock-client-id",
            "client_secret": "mock-client-secret",
            "timeout": 60
        }

    @mock.patch("argo_probe_keycloak.keycloak.requests.post")
    def test_fetch_keycloak_token_successfully(self, mock_post):
        mock_post.return_value = MockResponse(data=mock_data, status_code=200)
        status = fetch_keycloak_token(
            endpoint=self.args["endpoint"],
            client_id=self.args["client_id"],
            client_secret=self.args["client_secret"],
            timeout=self.args["timeout"]
        )
        mock_post.assert_called_once_with(
            "https://mock.keycloak.url/openid-connect/token/",
            auth=("mock-client-id", "mock-client-secret"),
            data={
                "client_id": "mock-client-id",
                "client_secret": "mock-client-secret",
                "grant_type": "client_credentials"
            },
            timeout=60
        )
        self.assertEqual(
            status["message"], "Access token fetched successfully."
        )
        self.assertEqual(status["code"], 0)

    @mock.patch("argo_probe_keycloak.keycloak.requests.post")
    def test_fetch_keycloak_token_if_request_exception(self, mock_post):
        mock_post.return_value = MockResponse(data=None, status_code=500)
        status = fetch_keycloak_token(
            endpoint=self.args["endpoint"],
            client_id=self.args["client_id"],
            client_secret=self.args["client_secret"],
            timeout=self.args["timeout"]
        )
        mock_post.assert_called_once_with(
            "https://mock.keycloak.url/openid-connect/token/",
            auth=("mock-client-id", "mock-client-secret"),
            data={
                "client_id": "mock-client-id",
                "client_secret": "mock-client-secret",
                "grant_type": "client_credentials"
            },
            timeout=60
        )
        self.assertEqual(status["message"], "500 SERVER ERROR")
        self.assertEqual(status["code"], 2)

    @mock.patch("argo_probe_keycloak.keycloak.requests.post")
    def test_fetch_keycloak_token_if_emtpy_access_token(self, mock_post):
        mock_data_copy = mock_data.copy()
        mock_data_copy["access_token"] = ""
        mock_post.return_value = MockResponse(
            data=mock_data_copy, status_code=200
        )
        status = fetch_keycloak_token(
            endpoint=self.args["endpoint"],
            client_id=self.args["client_id"],
            client_secret=self.args["client_secret"],
            timeout=self.args["timeout"]
        )
        mock_post.assert_called_once_with(
            "https://mock.keycloak.url/openid-connect/token/",
            auth=("mock-client-id", "mock-client-secret"),
            data={
                "client_id": "mock-client-id",
                "client_secret": "mock-client-secret",
                "grant_type": "client_credentials"
            },
            timeout=60
        )
        self.assertEqual(
            status["message"],
            "Access token not fetched - not defined in response json"
        )
        self.assertEqual(status["code"], 2)

    @mock.patch("argo_probe_keycloak.keycloak.requests.post")
    def test_fetch_keycloak_token_if_no_key_in_json(self, mock_post):
        mock_data_copy = mock_data.copy()
        del mock_data_copy["access_token"]
        mock_post.return_value = MockResponse(
            data=mock_data_copy, status_code=200
        )
        status = fetch_keycloak_token(
            endpoint=self.args["endpoint"],
            client_id=self.args["client_id"],
            client_secret=self.args["client_secret"],
            timeout=self.args["timeout"]
        )
        mock_post.assert_called_once_with(
            "https://mock.keycloak.url/openid-connect/token/",
            auth=("mock-client-id", "mock-client-secret"),
            data={
                "client_id": "mock-client-id",
                "client_secret": "mock-client-secret",
                "grant_type": "client_credentials"
            },
            timeout=60
        )
        self.assertEqual(
            status["message"],
            "Access token not fetched - key 'access_token' not defined in "
            "response json"
        )
        self.assertEqual(status["code"], 2)
