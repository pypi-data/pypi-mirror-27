import time
from sanction.client import Client


class OauthClient(Client):
    def init_app(self, app):
        self.token_endpoint = app.config.get("OAUTH_CLIENT_URL")  #
        self.client_id = app.config.get("OAUTH_CLIENT_ID")
        self.client_secret = app.config.get("OAUTH_CLIENT_SECRET")
        self.resource_endpoint = app.config.get("OAUTH_CLIENT_RESOURCE")

        return 1

    def request(self, url, method=None, data=None, headers=None, parser=None):
        if not self.access_token or time.time() > self.token_expires:
            self.request_token(grant_type='client_credentials')

        return super().request(url, method, data, headers, parser)