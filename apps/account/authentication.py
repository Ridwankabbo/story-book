from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class BlacklistAwareJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if not result:
            return None

        user, token = result

        # Check token blacklist in cache
        if cache.get(f"blacklist_{str(token)}"):
            raise AuthenticationFailed("Token blacklisted")

        return user, token
