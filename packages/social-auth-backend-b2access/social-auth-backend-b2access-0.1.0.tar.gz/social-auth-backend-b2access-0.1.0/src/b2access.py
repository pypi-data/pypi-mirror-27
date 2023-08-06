from social_core.backends.oauth import BaseOAuth2


class B2AccessOAuth2(BaseOAuth2):
    name = 'b2access'
    REQUIRES_EMAIL_VALIDATION = False
    DEFAULT_SCOPE = ['profile', 'email']
    ACCESS_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'https://b2access.eudat.eu/oauth2/token'
    USERINFO_URL = 'https://b2access.eudat.eu/oauth2/userinfo'
    AUTHORIZATION_URL = 'https://b2access.eudat.eu/oauth2-as/oauth2-authz'
    STATE_PARAMETER = False
    REDIRECT_STATE = False

    def auth_complete_credentials(self):
        return self.get_key_and_secret()

    def get_user_details(self, response):
        """Return user details from B2ACCESS"""
        fullname = response.get('name', '')
        email = response.get('email', '')
        uid = response.get('sub', None)
        email_verified = bool(response.get('email_verified', None))
        return {
            'username': fullname or email or uid,
            'email': email,
            'fullname': fullname,
            'email_verified': email_verified,
        }

    def get_user_id(self, details, response):
        return response['sub']

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(
            self.USERINFO_URL,
            headers={'Authorization': 'Bearer ' + access_token},
        )

    def refresh_token(self, *args, **kwargs):
        raise NotImplementedError(
            'Refresh tokens for B2ACCESS have not been implemented'
        )


class B2AccessIntegrationOAuth2(B2AccessOAuth2):
    name = 'b2access-test'
    ACCESS_TOKEN_URL = 'https://b2access-integration.fz-juelich.de/oauth2/token'
    USERINFO_URL = 'https://b2access-integration.fz-juelich.de/oauth2/userinfo'
    AUTHORIZATION_URL = 'https://b2access-integration.fz-juelich.de/oauth2-as/oauth2-authz'
