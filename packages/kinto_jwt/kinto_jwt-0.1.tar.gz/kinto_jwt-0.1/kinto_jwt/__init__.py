from .policy import JWTAuthenticationPolicy


def includeme(config):
    config.add_directive(
        'set_jwt_authentication_policy',
        set_jwt_authentication_policy,
        action_wrap=True)


def create_jwt_authentication_policy(config, public_key=None, algorithm=None,
            leeway=None, http_header=None, auth_type=None, audience=None, 
            userIdTokenKey=None, unauthorizedUserId=None, verifyToken=None):
    settings = config.get_settings()
    algorithm = algorithm or settings.get('jwt.algorithm') or 'RS256'
    public_key = public_key or settings.get('jwt.public_key')
    leeway = int(settings.get('jwt.leeway', 0)) if leeway is None else leeway
    http_header = http_header or settings.get('jwt.http_header') or 'Authorization'
    audience = audience or settings.get('jwt.audience')
    userIdTokenKey = userIdTokenKey or settings.get('jwt.userIdTokenKey') or 'sub'
    verifyToken = verifyToken or True
    unauthorizedUserId = unauthorizedUserId or 'public'

    if http_header.lower() == 'authorization':
            auth_type = auth_type or settings.get('jwt.auth_type') or 'JWT'
    else:
            auth_type = None

    return JWTAuthenticationPolicy(
            public_key=public_key,
            algorithm=algorithm,
            leeway=leeway,
            http_header=http_header,
            auth_type=auth_type,
            audience=audience,
            userIdTokenKey=userIdTokenKey,
            unauthorizedUserId=unauthorizedUserId,
            verifyToken=verifyToken)


def set_jwt_authentication_policy(cconfig, public_key=None, algorithm=None,
            leeway=None, http_header=None, auth_type=None, audience=None, 
            userIdTokenKey=None, unauthorizedUserId=None, verifyToken=None):
    policy = create_jwt_authentication_policy(
            config, public_key, algorithm, leeway, http_header, auth_type, 
            audience, userIdTokenKey, unauthorizedUserId, verifyToken)

    def request_claims(request):
        return policy.get_claims(request)

    config.set_authentication_policy(policy)
    config.add_request_method(request_claims, 'jwt_claims', reify=True)