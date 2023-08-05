# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

import pytest

from nauth.tests.fixtures.fixtures import MockResponse


def test_register_user(auth0_client, send_register_user_request,
                       send_update_user_request, send_identity_request,
                       test_user, test_tenant):
    """
    register_user() shall run without raising exception if responses
     from Auth0 are correct.
    """
    password = 'potato'
    auth0_client.register_user(test_user, password, test_tenant)


def test_register_user_failure(auth0_client,
                               send_register_user_request_failure,
                               send_update_user_request,
                               send_identity_request,
                               test_user, test_tenant):
    """
    register_user() shall raise exception when one of Auth0 responses fails.
    """
    password = 'potato'
    with pytest.raises(RuntimeError):
        auth0_client.register_user(test_user, password, test_tenant)


@pytest.mark.parametrize(
    "value", [MockResponse({'ticket': 'http://fake-url.com'}, 200)]
)
def test_send_register_user_request(auth0_client_patch, rpost, auth0_client,
                                    test_tenant):

    expected_request_json = {'email': 'fake@fake.com',
                             'email_verified': True,
                             'connection': 'fake_connection',
                             'password': 'fake_pass',
                             'user_metadata': {'tenant': test_tenant.name}}

    auth0_client._send_register_user_request(
        username=expected_request_json['email'],
        connection=expected_request_json['connection'],
        password=expected_request_json['password'],
        tenant=test_tenant)

    assert expected_request_json == rpost.json


@pytest.mark.parametrize(
    "value", [MockResponse({'ticket': 'http://fake-url.com'}, 200)]
)
def test_get_password_reset_url(auth0_client_patch, rpost, auth0_client):

    expected_url = 'http://fake-url.com'

    assert expected_url == auth0_client.get_password_reset_url(user_id='',
                                                               email='',
                                                               url='')


@pytest.mark.parametrize(
    "value", [MockResponse([{'user_id': 'tomato'}], 200)]
)
def test_get_user_id(auth0_client_patch, rget, auth0_client, test_user):
    """
    get_user_id() should create a GET /api/v2/users
    request with proper query and
    return id of found user.
    """

    found_id = auth0_client.get_user_id(email=test_user.email)

    expected_query = 'q=' + quote('email:"{}"'.format(test_user.email))
    assert expected_query in rget.url
    assert test_user.name == found_id


@pytest.mark.parametrize("value", [MockResponse(None, 204)])
def test_delete_user(auth0_client_patch, rdelete, auth0_client, test_user):

    auth0_client_patch.setattr(
        'nauth.clients.auth0_client.Auth0Client.get_user_id',
        lambda x, y: test_user.name
    )

    auth0_client.delete_user(email=test_user.email)

    expected = "{}/{}".format(
        auth0_client.user_management_endpoint,
        test_user.name
    )

    assert expected == rdelete.url


@pytest.mark.parametrize("value", [MockResponse(None, 200)])
def test_delete_user_no_user_id(auth0_client_patch, rdelete, auth0_client,
                                test_user):
    """
    delete_user() should raise a RuntimeError when user_id was not obtained.
    """

    auth0_client_patch.setattr(
        'nauth.clients.auth0_client.Auth0Client.get_user_id',
        lambda x, y: None
    )

    with pytest.raises(RuntimeError):
        auth0_client.delete_user(email=test_user.email)


@pytest.mark.parametrize("value", [MockResponse(None, 404)])
def test_delete_user_failure(auth0_client_patch, rdelete, auth0_client,
                             test_user):
    """
    delete_user() should raise a RuntimeError when Auth0 returns status code
    different than 200.
    """

    auth0_client_patch.setattr(
        'nauth.clients.auth0_client.Auth0Client.get_user_id',
        lambda x, y: test_user.name
    )

    with pytest.raises(RuntimeError):
        auth0_client.delete_user(email=test_user.email)
