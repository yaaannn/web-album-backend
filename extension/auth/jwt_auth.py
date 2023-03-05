from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

# from extension.jwt_token_ext import JwtToken
from util.jwt_token_util import JwtTokenUtil
from app.user.models import User


class JwtAuthentication(BaseAuthentication):
    """
    用户认证
    """

    # 用于在响应头中返回的认证方式
    www_authenticate_realm = "api"

    def __init__(self) -> None:
        super().__init__()
        self.jwt = JwtTokenUtil()

    def authenticate(self, request):
        """
        Return a `User` if the request can be successfully authenticated,
        otherwise return `None`.
        """
        token = request.META.get(self.jwt.header_name, "")
        if not token:
            return None
        token, msg = self.jwt.check_headers_jwt(token)
        if not token:
            raise AuthenticationFailed(msg)
        user, msg = self.jwt.decode_user(token, User)
        if not user:
            raise AuthenticationFailed(msg)
        return user, token

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(
            self.jwt.header_type, self.www_authenticate_realm
        )
