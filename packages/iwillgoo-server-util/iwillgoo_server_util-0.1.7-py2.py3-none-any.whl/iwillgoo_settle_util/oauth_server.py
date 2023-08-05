from dateutil import parser
from flask_oauthlib.provider import OAuth2Provider

from iwillgoo_settle_util import oauth_client


class UserInfo:
    def __init__(self, data) -> None:
        self.__dict__ = data


class Token:
    def __init__(self, data) -> None:
        self.__dict__ = data
        self.user = UserInfo(data.get("user"))
        self.expires = parser.parse(self.expires)
        self.expires = self.expires.replace(tzinfo=None)


oauth_server = OAuth2Provider()


@oauth_server.tokengetter
def token_getter(access_token, *args, **kwargs):
    assert access_token, "没有传入token"

    url = oauth_server.app.config.get("OAUTH_SERVER_URL") + access_token
    oauth_client.request_token(grant_type='client_credentials')
    data = oauth_client.request(url, 'GET')
    token = Token(data)

    return token


def init_oauth_server(app):
    oauth_server.init_app(app)


@oauth_server.clientgetter
def client_getter(client_id):
    pass


@oauth_server.tokensetter
def grant_setter(client_id, code, request, *agrs, **kwargs):
    pass


@oauth_server.grantsetter
def token_setter(token, request, *args, **kwargs):
    pass


@oauth_server.grantgetter
def grant_getter(client_id, code):
    pass
