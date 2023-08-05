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

import pytest

from nauth.tests.fixtures.fixtures import MockResponse
from nauth.errors import RefreshTokenExpiredError, AccessTokenRefreshError, \
    UaaAuthorizationError


class TestToken(object):

    @pytest.mark.parametrize(
        "value", [MockResponse({"email": "Test"}, 200)]
    )
    def test_get_check_token_response_returns_tenant(self, monkeypatch, rpost,
                                                     uaa_client, test_user):
        """
        get_check_token_response() should return proper tenant for an user
        """
        fake_tenant = 'fake tenant'
        fake_user_id = 'fake id'
        monkeypatch.setattr('nauth.clients.uaa_client.UaaClient.get_user_id',
                            lambda *args, **kwargs: fake_user_id)
        monkeypatch.setattr('nauth.clients.uaa_client.UaaClient.get_tenant',
                            lambda x, y: fake_tenant)

        token_payload = uaa_client.get_check_token_response("")

        assert fake_tenant == token_payload.tenant

    @pytest.mark.parametrize(
        "value", [MockResponse({"access_token": "t"}, 200)]
    )
    def test_get_id_token_request(self, rpost, uaa_client):
        """
        get_id_token() should set response_type to id_token
        """
        data = {}
        uaa_client.get_id_token(data)
        expected = {
            "client_id": "test",
            "client_secret": "test",
            "scope": "openid",
            "grant_type": "password",
            "response_type": "id_token",
        }

        assert (rpost.data == expected)

    @pytest.mark.parametrize("value", [MockResponse("", 401)])
    def test_get_id_token_error(self, rpost, uaa_client):
        with pytest.raises(UaaAuthorizationError):
            uaa_client.get_id_token({})

    @pytest.mark.parametrize(
        "value", [MockResponse({"access_token": "t"}, 200)]
    )
    def test_get_refreshed_id_token_request(self, rpost, uaa_client):
        """
        get_refreshed_id_token() should set response_type to access_token
        """
        data = {}
        uaa_client.get_refreshed_id_token(data)
        expected = {
            "client_id": "test",
            "client_secret": "test",
            "grant_type": "refresh_token",
        }

        assert (rpost.data == expected)

    @pytest.mark.parametrize(
        "value, exception", [
            (
                    MockResponse("Refresh token expired", 401),
                    RefreshTokenExpiredError
            ),
            (
                    MockResponse("Error", 500),
                    AccessTokenRefreshError
            )
        ]
    )
    def test_refreshed_id_token_negative(self, rpost, uaa_client, exception):
        with pytest.raises(exception):
            uaa_client.get_refreshed_id_token({})


class TestUser(object):

    @pytest.mark.parametrize(
        "value", [MockResponse({'id': 'test-id'}, 201)]
    )
    def test_register_user(self, uaa_client_patch, rpost, rget, uaa_client,
                           uaa_test_user, test_tenant):

        created_user_id = uaa_client.register_user(user=uaa_test_user,
                                                   password='',
                                                   tenant=test_tenant)
        expected_id = 'test-id'

        assert expected_id == created_user_id

    @pytest.mark.parametrize(
        "value", [MockResponse({'id': 'test-id'}, 201)]
    )
    def test_register_user_tenant_exists(self, uaa_client_patch, rpost,
                                         rget, uaa_client, uaa_test_user,
                                         test_tenant):

        created_user_id = uaa_client.register_user(user=uaa_test_user,
                                                   password='',
                                                   tenant=test_tenant)
        expected_id = 'test-id'

        assert expected_id == created_user_id

    @pytest.mark.parametrize(
        "value", [MockResponse('Some error', 500)]
    )
    def test_require_password_change_fail(self, uaa_client_patch, rpatch,
                                          rget, rdelete, uaa_client):
        with pytest.raises(RuntimeError):
            uaa_client.require_password_change("unexisting_id")

    @pytest.mark.parametrize(
        "value", [MockResponse('OK', 200)]
    )
    def test_require_password_change_success(self, uaa_client_patch, rpatch,
                                             rget, uaa_client):
        try:
            uaa_client.require_password_change("some_id")
        except Exception:
            pytest.fail("No exception is expected in positive scenario")

    @pytest.mark.parametrize(
        "value", [MockResponse({'id': 'fake-id'}, 201)]
    )
    def test_register_user_group_creation_fails(self, uaa_client_patch,
                                                rpost, rget, uaa_client,
                                                uaa_test_user, test_tenant):

        def create_group_failure(*args, **kwargs):
            raise RuntimeError

        uaa_client_patch.setattr(
            'nauth.clients.uaa_client.UaaClient.create_group',
            create_group_failure
        )

        with pytest.raises(RuntimeError):
            uaa_client.register_user(user=uaa_test_user, password='',
                                     tenant=test_tenant)

    @pytest.mark.parametrize(
        "value", [MockResponse({'code': 'test-code'}, 201)]
    )
    def test_get_password_reset_url(self, rpost, uaa_client):
        """
        get_password_reset_url() should return a following URL:
         <reset_password_endpoint>/<reset_code>, where reset_code is obtained
        from UAA in _get_password_reset_code() method.
        """
        test_code = 'test-code'
        expected_url = '{reset_password_endpoint}?code={code}'.format(
            reset_password_endpoint=uaa_client.password_reset_endpoint,
            code=test_code)

        assert expected_url == uaa_client.get_password_reset_url()

    @pytest.mark.parametrize(
        "value", [MockResponse(None, 500)]
    )
    def test_get_password_reset_url_failure(self, rpost, uaa_client):
        """
        get_password_reset_url() should return a following URL:
         <reset_password_endpoint>/<reset_code>, where reset_code is obtained
        from UAA in _get_password_reset_code() method.
        """
        assert uaa_client.get_password_reset_url() is None

    @pytest.mark.parametrize(
        "value", [MockResponse({"resources": [{"id": "test-id"}]}, 200)]
    )
    def test_get_user_id(self, uaa_client_patch, rget, uaa_client,
                         uaa_test_user):
        """
        get_user_id() should create a GET /Users request with proper filter and
        return id of found user.
        """
        found_id = uaa_client.get_user_id(email=uaa_test_user.email)
        expected_params = {
            'filter': 'email eq "{}"'.format(uaa_test_user.email)
        }

        assert expected_params == rget.params
        assert "test-id" == found_id

    @pytest.mark.parametrize(
        "value", [MockResponse({"resources": [{"id": "test-id"}]}, 200)]
    )
    def test_get_user_list(self, uaa_client_patch, rget, uaa_client):
        """
        get_user_list() should create a GET /Users request
        and return list of found user.
        """
        max_results = 99
        expected_params = {'count': '{}'.format(str(max_results))}
        result = uaa_client.get_user_list(max_results)

        assert expected_params == rget.params
        assert result == {"resources": [{"id": "test-id"}]}

    @pytest.mark.parametrize("value", [MockResponse(None, 500)])
    def test_get_user_id_failure(self, uaa_client_patch, rget, uaa_client,
                                 uaa_test_user):
        found_id = uaa_client.get_user_id(email=uaa_test_user.email)
        assert found_id is None

    @pytest.mark.parametrize("value", [MockResponse(None, 200)])
    def test_delete_user(self, uaa_client_patch, rdelete, uaa_client,
                         uaa_test_user):
        """
        delete_user() should make a delete request on /Users/<user_id> path
        """
        test_user_id = 'test_id'
        uaa_client_patch.setattr(
            'nauth.clients.uaa_client.UaaClient.get_user_id',
            lambda *args, **kwargs: test_user_id
        )
        uaa_client.delete_user(email=uaa_test_user.email)

        assert "{}/{}".format(uaa_client.user_management_endpoint,
                              test_user_id) == rdelete.url

    @pytest.mark.parametrize("value", [MockResponse(None, 200)])
    def test_delete_user_no_user_id(self, uaa_client_patch, rdelete,
                                    uaa_client, uaa_test_user):
        """
        delete_user() should raise a RuntimeError when user_id was not obtained
        """
        uaa_client_patch.setattr(
            'nauth.clients.uaa_client.UaaClient.get_user_id',
            lambda *args, **kwargs: None
        )
        with pytest.raises(RuntimeError):
            uaa_client.delete_user(email=uaa_test_user.email)

    @pytest.mark.parametrize("value", [MockResponse(None, 404)])
    def test_delete_user_failure(self, uaa_client_patch, rdelete, uaa_client,
                                 uaa_test_user):
        """
        delete_user() should raise a RuntimeError when UAA returns status code
        different than 200.
        """
        test_id = 'test_id'
        uaa_client_patch.setattr(
            'nauth.clients.uaa_client.UaaClient.get_user_id',
            lambda *args, **kwargs: test_id
        )
        with pytest.raises(RuntimeError):
            uaa_client.delete_user(email=uaa_test_user)


class TestTenant(object):

    @pytest.mark.parametrize(
        "value", [MockResponse({
            'groups': [
                {'display': 'scim.read'},
                {'display': 'scim.write'},
                {'display': 'Test tenant.tenant'}
            ]}, 200)]
    )
    def test_get_tenant(self, uaa_client_patch, rget, uaa_client):
        user_id = 'test-id'
        test_tenant_name = 'Test tenant'
        found_tenant = uaa_client.get_tenant(user_id)

        expected_url = '{}/{}'.format(uaa_client.user_management_endpoint,
                                      user_id)
        assert expected_url == rget.url
        assert test_tenant_name == found_tenant

    @pytest.mark.parametrize("value", [MockResponse(None, 500)])
    def test_get_tenant_failure(self, uaa_client_patch, rget, uaa_client):
        found_tenant = uaa_client.get_tenant('')
        assert found_tenant is None


class TestGroup(object):

    @pytest.mark.parametrize(
        "value", [MockResponse({"resources": [{"id": "test-id"}]}, 200)]
    )
    def test_get_group_id(self, monkeypatch, rget, uaa_client):
        monkeypatch.setattr(
            'nauth.clients.uaa_client.UaaClient._get_auth_header',
            lambda *args, **kwargs: None
        )
        test_group_id = 'test-id'
        test_group_name = 'test-group'
        found_group_id = uaa_client.get_group_id(test_group_name)
        expected_params = {
            'filter': 'displayName eq "{}"'.format(test_group_name)
        }

        assert expected_params == rget.params
        assert test_group_id == found_group_id

    @pytest.mark.parametrize("value", [MockResponse({"id": "test-id"}, 201)])
    def test_create_group(self, rpost, uaa_client):
        expected_group_id = 'test-id'
        created_group_id = uaa_client.create_group(name='', members=[])

        assert expected_group_id == created_group_id

    @pytest.mark.parametrize("value", [MockResponse(None, 500)])
    def test_create_group_failure(self, rpost, uaa_client):

        with pytest.raises(RuntimeError):
            uaa_client.create_group(name='', members=['test_member'])

    @pytest.mark.parametrize("value", [MockResponse(None, 201)])
    def test_add_user_to_group(self, rpost, uaa_client):
        group_id = 'test-group-id'
        user_id = 'test-user-id'
        expected_post_json = {'origin': 'uaa',
                              'type': 'USER',
                              'value': user_id}
        uaa_client.add_user_to_group(group_id=group_id, user_id=user_id)

        assert expected_post_json == rpost.json

    @pytest.mark.parametrize("value", [MockResponse(None, 500)])
    def test_add_user_to_group_failure(self, rpost, uaa_client):
        group_id = 'test-group-id'
        user_id = 'test-user-id'

        with pytest.raises(RuntimeError):
            uaa_client.add_user_to_group(group_id=group_id, user_id=user_id)
