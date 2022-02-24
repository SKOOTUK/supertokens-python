# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from uuid import UUID

import falcon
from falcon import App, testing

from pytest import fixture

from supertokens_python import init, SupertokensConfig, InputAppInfo
from supertokens_python.recipe import session
from supertokens_python.exceptions import SuperTokensError
from supertokens_python.framework.falcon import Middleware

from supertokens_python.recipe.session.framework.falcon import verify_session
from supertokens_python.recipe.session.syncio import (
    create_new_session,
    refresh_session,
    get_session,
    revoke_session
)
from tests.utils import (
    reset, setup_st,
    clean_st,
    start_st,
    extract_falcon_cookies,
    TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH,
    TEST_DRIVER_CONFIG_COOKIE_DOMAIN,
    TEST_DRIVER_CONFIG_COOKIE_SAME_SITE,
    TEST_DRIVER_CONFIG_REFRESH_TOKEN_PATH
)


def is_valid_uuid(value):
    try:
        UUID(value)
    except ValueError:
        return False
    else:
        return True


def setup_function(f):
    reset()
    clean_st()
    setup_st()


def teardown_function(f):
    reset()
    clean_st()


def apis_override_session(param):
    param.disable_refresh_post = True
    return param


def init_st():
    init(
        supertokens_config=SupertokensConfig('http://localhost:3567'),
        app_info=InputAppInfo(
            app_name="SuperTokens Demo",
            api_domain="http://api.supertokens.io",
            website_domain="http://supertokens.io",
            api_base_path="/auth"
        ),
        framework='falcon',
        recipe_list=[session.init(
            anti_csrf='VIA_TOKEN',
            cookie_domain='supertokens.io',
            override=session.InputOverrideConfig(
                apis=apis_override_session
            )
        )]
    )
    start_st()


class GenericResource:
    def on_get_login(self, req, resp):
        user_id = 'userId'
        create_new_session(req, user_id, {}, {})
        resp.media = {'userId': user_id}
        return resp

    def on_post_refresh(self, req, resp):
        refresh_session(req)
        resp.media = {}
        return resp

    def on_get_info(self, req, resp):
        get_session(req, True)
        resp.media = {}
        return resp

    def on_get_custom_info(self, req, resp):
        resp.media = {}
        return resp

    def on_options_custom_handle_options(self, req, resp):
        resp.media = {'method': 'option'}
        return resp

    def on_get_handle(self, req, resp):
        session = get_session(req, True)
        resp.media = {'s': session.get_handle()}
        return resp

    @falcon.before(verify_session)
    def on_post_custom_logout(self, req, resp):
        resp.media = {}
        session = get_session(req, False)
        revoke_session(session.get_handle())
        return resp


@fixture(scope='function')
def driver_config_client():
    resource = GenericResource()

    app = App(middleware=[Middleware()])
    app.add_error_handler(SuperTokensError, Middleware.error_handler)

    app.add_route("/login", resource, suffix="login")
    app.add_route("/refresh", resource, suffix="refresh")
    app.add_route("/info", resource, suffix="info")
    app.add_route("/custom/info", resource, suffix="custom_info")
    app.add_route("/custom/handle", resource, suffix="custom_handle_options")
    app.add_route("/handle", resource, suffix="handle")
    app.add_route("/logout", resource, suffix="custom_logout")

    return testing.TestClient(app)


def test_login_refresh(driver_config_client: testing.TestClient):
    init_st()

    response_1 = driver_config_client.simulate_get('/login')
    cookies_1 = extract_falcon_cookies(response_1)

    assert response_1.headers.get('anti-csrf') is not None
    assert cookies_1['sAccessToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sIdRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sAccessToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sRefreshToken']['path'] == TEST_DRIVER_CONFIG_REFRESH_TOKEN_PATH
    assert cookies_1['sIdRefreshToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sAccessToken']['http_only']
    assert cookies_1['sRefreshToken']['http_only']
    assert cookies_1['sIdRefreshToken']['http_only']
    assert cookies_1['sAccessToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sIdRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE

    response_2 = driver_config_client.simulate_post(
        '/refresh',
        headers={
            'anti-csrf': response_1.headers.get('anti-csrf')
        },
        cookies={
            'sRefreshToken': cookies_1['sRefreshToken']['value'],
            'sIdRefreshToken': cookies_1['sIdRefreshToken']['value'],
        }
    )
    cookies_2 = extract_falcon_cookies(response_2)

    assert response_2.headers.get('anti-csrf') is not None
    assert cookies_2['sAccessToken']['value'] != cookies_1['sAccessToken']['value']
    assert cookies_2['sRefreshToken']['value'] != cookies_1['sRefreshToken']['value']
    assert cookies_2['sIdRefreshToken']['value'] != cookies_1['sIdRefreshToken']['value']
    assert cookies_2['sAccessToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_2['sRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_2['sIdRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_2['sRefreshToken']['path'] == TEST_DRIVER_CONFIG_REFRESH_TOKEN_PATH
    assert cookies_2['sIdRefreshToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_2['sAccessToken']['http_only']
    assert cookies_2['sRefreshToken']['http_only']
    assert cookies_2['sIdRefreshToken']['http_only']
    assert cookies_2['sAccessToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_2['sRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_2['sIdRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE


def test_login_logout(driver_config_client: testing.TestClient):
    init_st()
    response_1 = driver_config_client.simulate_get('/login')
    cookies_1 = extract_falcon_cookies(response_1)

    assert response_1.headers.get('anti-csrf') is not None
    assert cookies_1['sAccessToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sIdRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sAccessToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sRefreshToken']['path'] == TEST_DRIVER_CONFIG_REFRESH_TOKEN_PATH
    assert cookies_1['sIdRefreshToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sAccessToken']['http_only']
    assert cookies_1['sRefreshToken']['http_only']
    assert cookies_1['sIdRefreshToken']['http_only']
    assert cookies_1['sAccessToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sIdRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sAccessToken']['secure'] is None
    assert cookies_1['sRefreshToken']['secure'] is None
    assert cookies_1['sIdRefreshToken']['secure'] is None

    response_2 = driver_config_client.simulate_post(
        '/logout',
        headers={
            'anti-csrf': response_1.headers.get('anti-csrf')
        },
        cookies={
            'sAccessToken': cookies_1['sAccessToken']['value'],
            'sIdRefreshToken': cookies_1['sIdRefreshToken']['value']
        }
    )

    cookies_2 = extract_falcon_cookies(response_2)
    assert cookies_2 == {}
    assert response_2.status_code == 200

    response_3 = driver_config_client.simulate_post(
        '/logout',
        headers={
            'anti-csrf': response_1.headers.get('anti-csrf')
        }
    )

    assert response_3.status_code == 401
    assert response_3.json == {
        'title': '401 Unauthorized',
        'description': 'Authorization data is incorrect or missing'
    }


def test_login_info(driver_config_client: testing.TestClient):
    init_st()

    response_1 = driver_config_client.simulate_get('/login')
    cookies_1 = extract_falcon_cookies(response_1)

    assert response_1.headers.get('anti-csrf') is not None
    assert cookies_1['sAccessToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sIdRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sAccessToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sRefreshToken']['path'] == TEST_DRIVER_CONFIG_REFRESH_TOKEN_PATH
    assert cookies_1['sIdRefreshToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sAccessToken']['http_only']
    assert cookies_1['sRefreshToken']['http_only']
    assert cookies_1['sIdRefreshToken']['http_only']
    assert cookies_1['sAccessToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sIdRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sAccessToken']['secure'] is None
    assert cookies_1['sRefreshToken']['secure'] is None
    assert cookies_1['sIdRefreshToken']['secure'] is None

    response_2 = driver_config_client.simulate_get(
        '/info',
        headers={
            'anti-csrf': response_1.headers.get('anti-csrf')
        },
        cookies={
            'sAccessToken': cookies_1['sAccessToken']['value'],
            'sIdRefreshToken': cookies_1['sIdRefreshToken']['value']
        }
    )
    cookies_2 = extract_falcon_cookies(response_2)
    assert cookies_2 == {}


def test_login_handle(driver_config_client: testing.TestClient):
    init_st()

    response_1 = driver_config_client.simulate_get('/login')
    cookies_1 = extract_falcon_cookies(response_1)

    assert response_1.headers.get('anti-csrf') is not None
    assert cookies_1['sAccessToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sIdRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sAccessToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sRefreshToken']['path'] == TEST_DRIVER_CONFIG_REFRESH_TOKEN_PATH
    assert cookies_1['sIdRefreshToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sAccessToken']['http_only']
    assert cookies_1['sRefreshToken']['http_only']
    assert cookies_1['sIdRefreshToken']['http_only']
    assert cookies_1['sAccessToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sIdRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sAccessToken']['secure'] is None
    assert cookies_1['sRefreshToken']['secure'] is None
    assert cookies_1['sIdRefreshToken']['secure'] is None

    response_2 = driver_config_client.simulate_get(
        '/handle',
        headers={
            'anti-csrf': response_1.headers.get('anti-csrf')
        },
        cookies={
            'sAccessToken': cookies_1['sAccessToken']['value'],
            'sIdRefreshToken': cookies_1['sIdRefreshToken']['value']
        }
    )
    result_dict = response_2.json
    assert "s" in result_dict
    assert is_valid_uuid(result_dict["s"])


def test_login_refresh_error_handler(driver_config_client: testing.TestClient):
    init_st()

    response_1 = driver_config_client.simulate_get('/login')
    cookies_1 = extract_falcon_cookies(response_1)

    assert response_1.headers.get('anti-csrf') is not None
    assert cookies_1['sAccessToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sIdRefreshToken']['domain'] == TEST_DRIVER_CONFIG_COOKIE_DOMAIN
    assert cookies_1['sAccessToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sRefreshToken']['path'] == TEST_DRIVER_CONFIG_REFRESH_TOKEN_PATH
    assert cookies_1['sIdRefreshToken']['path'] == TEST_DRIVER_CONFIG_ACCESS_TOKEN_PATH
    assert cookies_1['sAccessToken']['http_only']
    assert cookies_1['sRefreshToken']['http_only']
    assert cookies_1['sIdRefreshToken']['http_only']
    assert cookies_1['sAccessToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sIdRefreshToken']['same_site'].lower() == TEST_DRIVER_CONFIG_COOKIE_SAME_SITE
    assert cookies_1['sAccessToken']['secure'] is None
    assert cookies_1['sRefreshToken']['secure'] is None
    assert cookies_1['sIdRefreshToken']['secure'] is None

    response_2 = driver_config_client.simulate_post(
        '/refresh',
        headers={
            'anti-csrf': response_1.headers.get('anti-csrf')
        },
        cookies={}  # no cookies
    )
    assert response_2.status_code == 401  # not authorized because no refresh tokens
