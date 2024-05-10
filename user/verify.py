import jwt
from django.conf import settings
from user.models import UserToken
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header:
            return None
        else:
            try:
                access_token = header.split(' ')[1]
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                token_id = payload['token_id']
                try:
                    token = UserToken.objects.get(id=token_id, is_active=True)
                except UserToken.DoesNotExist:
                    raise exceptions.AuthenticationFailed('Token expired..')
                user = token.user 
            except IndexError:
                raise exceptions.AuthenticationFailed('Token prefix missing.')
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('Token expired')
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('Invalid token')

            user.is_authenticated = True
            return (user, None)