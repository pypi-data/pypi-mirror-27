import datetime
import logging
import warnings
import jwt
from zope.interface import implementer
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.interfaces import IAuthenticationPolicy


log = logging.getLogger('kinto_jwt')

@implementer(IAuthenticationPolicy)
class JWTAuthenticationPolicy(CallbackAuthenticationPolicy):
    def __init__(self, public_key=None, algorithm='RS256',
            leeway=0, http_header='Authorization', auth_type='JWT', audience=None, 
            userIdTokenKey='sub', unauthorizedUserId='public', verifyToken=True):
        self.public_key = public_key
        self.algorithm = algorithm
        self.leeway = leeway
        self.http_header = http_header
        self.auth_type = auth_type
        self.audience = audience
        self.verifyToken = verifyToken
        self.unauthorizedUserId = unauthorizedUserId
        self.userIdTokenKey = userIdTokenKey

    def get_claims(self, request):
        if self.http_header == 'Authorization':
            try:
                if request.authorization is None:
                    return {}
            except ValueError:  # Invalid Authorization header
                return {}

            (auth_type, token) = request.authorization
            
            if auth_type != self.auth_type:
                return {}
        else:
            token = request.headers.get(self.http_header)

        if not token:
            return {}

        try:
            if self.verifyToken:
                claims = jwt.decode(token, self.public_key, algorithms=[self.algorithm], leeway=self.leeway, audience=self.audience)
            else:
                claims = jwt.decode(token, verify=False)
        except jwt.InvalidTokenError as e:
            log.warning('Invalid JWT token from %s: %s', request.remote_addr, e)
            return {}

        return claims

    def unauthenticated_userid(self, request):
        claims = self.get_claims(request)
        if claims != {} and self.userIdTokenKey in claims:
            return claims[self.userIdTokenKey]
        else:
            return self.unauthorizedUserId

    def remember(self, request, principal, **kw):
        warnings.warn(
            'JWT tokens need to be returned by an API. Using remember() '
            'has no effect.',
            stacklevel=3)
        return []

    def forget(self, request):
        warnings.warn(
            'JWT tokens are managed by API (users) manually. Using forget() '
            'has no effect.',
            stacklevel=3)
        return []