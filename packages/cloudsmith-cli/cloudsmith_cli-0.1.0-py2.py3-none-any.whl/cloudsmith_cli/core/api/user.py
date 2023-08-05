"""API - User endpoints."""
from __future__ import absolute_import, print_function, unicode_literals

import cloudsmith_api
from .exceptions import catch_raise_api_exception


def get_user_api():
    """Get the user API client."""
    config = cloudsmith_api.Configuration()
    client = cloudsmith_api.UserApi()
    if config.user_agent:
        client.api_client.user_agent = config.user_agent
    return client


def get_user_token(login, password):
    """Retrieve user token from the API (via authentication)."""
    client = get_user_api()

    with catch_raise_api_exception():
        data = client.user_token_create(
            data={
                'email': login,
                'password': password
            }
        )

    return data.token


def get_user_brief():
    """Retrieve brief for current user (if any)."""
    client = get_user_api()

    with catch_raise_api_exception():
        data = client.user_self()

    return data.authenticated, data.slug, data.email, data.name
