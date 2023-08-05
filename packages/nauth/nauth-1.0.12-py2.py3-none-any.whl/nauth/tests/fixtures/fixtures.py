import json
from collections import namedtuple

import pytest

from nauth.clients.auth_client import AuthClientConfig
from nauth.clients.auth0_client import Auth0Client
from nauth.clients.uaa_client import UaaClient


class MockResponse(object):
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.text = json.dumps(json_data)
        self.status_code = status_code

    def json(self):
        return self.json_data


@pytest.fixture
def test_tenant():
    Tenant = namedtuple('Tenant', ['name'])
    return Tenant('tenant')


@pytest.fixture
def test_user():
    User = namedtuple('User', ['name', 'email'])
    return User('tomato', 'tomato@potato.com')


@pytest.fixture
def uaa_test_user():
    User = namedtuple('User', ['email', 'first_name', 'last_name'])
    return User('tomato@potato.com', 'tomato', 'potato')


@pytest.fixture(scope='module')
def uaa_client():
    auth_config = AuthClientConfig(
        client_id="test",
        client_secret="test",
        auth_host="http://test")
    client = UaaClient(auth_config)
    return client


@pytest.fixture
def uaa_client_patch(monkeypatch):

    methods = [
        ['_get_auth_header', {}],
        ['get_group_id', None],
        ['add_user_to_group', None],
    ]

    def patch_method(method):
        return monkeypatch.setattr(
            'nauth.clients.uaa_client.UaaClient.{}'.format(method[0]),
            lambda *args, **kwargs: method[1]
        )

    map(patch_method, methods)
    return monkeypatch


@pytest.fixture
def auth0_client_patch(monkeypatch):
    monkeypatch.setattr('nauth.clients.auth0_client.'
                        'Auth0Client._get_auth_header',
                        lambda x: None)
    return monkeypatch


@pytest.fixture
def send_register_user_request(monkeypatch):
    def mock_register_user_request(*args, **kwargs):
        json_res = {"user_id": "fake_provider|fake_user_id"}
        res = MockResponse(json_res, 201)
        return res
    monkeypatch.setattr('nauth.clients.auth0_client.Auth0Client.'
                        '_send_register_user_request',
                        mock_register_user_request)


@pytest.fixture
def send_update_user_request(monkeypatch):
    def mock_update_user_request(*args, **kwargs):
        json_res = {}
        res = MockResponse(json_res, 200)
        return res
    monkeypatch.setattr('nauth.clients.auth0_client.Auth0Client.'
                        '_send_update_user_request', mock_update_user_request)


@pytest.fixture
def send_identity_request(monkeypatch):
    def mock_identity_request(*args, **kwargs):
        json_res = {}
        res = MockResponse(json_res, 201)
        return res
    monkeypatch.setattr('nauth.clients.auth0_client.Auth0Client.'
                        '_send_identity_request', mock_identity_request)


@pytest.fixture
def send_register_user_request_failure(monkeypatch):
    def mock_register_user_request(*args, **kwargs):
        json_res = {"user_id": "fake_provider|fake_user_id"}
        res = MockResponse(json_res, 500)
        return res
    monkeypatch.setattr('nauth.clients.auth0_client.Auth0Client.'
                        '_send_register_user_request',
                        mock_register_user_request)


@pytest.fixture(scope='module')
def auth0_client():
    auth_config = AuthClientConfig(
        client_id="test",
        client_secret="test",
        auth_host="http://test")
    client = Auth0Client(auth_config)
    return client
