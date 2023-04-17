from typing import Optional

from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth


class EtsyOAuthClient(OAuth2Session):
    authorization_url_base = "https://www.etsy.com/oauth/connect"
    token_url_base = "https://api.etsy.com/v3/public/oauth/token"

    """
    The EtsyOAuthClient class is an authentication client for the ETSY marketplace
    that allows users to connect to the API with OAuth2 authentication.
    """
    def __init__(
            self, client_id: str, client_secret: str, redirect_uri: Optional[str] = None,
            scope: Optional[list[str]] = None, code_verifier: Optional[str] = None
    ) -> None:
        """
        Initializes a new instance of the EtsyOAuthClient class.

        Parameters:
        :param client_id: str - the client id obtained from the Etsy Developer Console.
        :param client_secret: str - the client secret obtained from the Etsy Developer Console.
        :param redirect_uri: str - the redirect URI registered with the Etsy Developer Console.
        :param scope: list[str] - list of scopes you wish to request access to.
        :param code_verifier: Optional[str] - the code verifier used in PKCE, defaults to None.
        """
        super().__init__(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope
        )
        self.auth = HTTPBasicAuth(client_id, client_secret)
        self.code_verifier = code_verifier or str(self._client.create_code_verifier(128))

    def authorization_url(self, **kwargs) -> (str, str):
        """
        Returns the authorization URL for the OAuth2 flow with PKCE.

        Parameters:
        :param kwargs: additional parameters for the authorization URL.
        :return: A tuple with the authorization URL and state.
        """
        authorization_url, state = super().authorization_url(
            self.authorization_url_base,
            code_challenge=self._client.create_code_challenge(self.code_verifier, "S256"),
            code_challenge_method="S256",
            **kwargs
        )
        return authorization_url, state

    def fetch_token(self, code: str) -> dict:
        """
        Retrieves the access token from the authorization server.

        Parameters:
        :param code: str - the authorization code received from the authorization server.
        :return: A dictionary with the access token.
        """
        return super().fetch_token(
            self.token_url_base,
            code=code,
            auth=self.auth,
            include_client_id=True,
            code_verifier=self.code_verifier
        )

    def refresh_token(self, refresh_token: str) -> dict:
        """
        Requests a new access token from the authorization server using a refresh token.

        Parameters:
        :param refresh_token: str - the refresh token used to retrieve a new access token.
        :return: A dictionary with the new access token.
        """
        body_params = {"client_id": self.client_id}
        return super().refresh_token(
            self.token_url_base,
            refresh_token=refresh_token,
            auth=self.auth,
            **body_params
        )
