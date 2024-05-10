import jwt
import uuid
import datetime
from django.conf import settings
from user.models import UserToken



def usertoken(token_id):
    access_token_payload = {
            'token_id': str(token_id),
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=365, minutes=5),
            'iat': datetime.datetime.now(datetime.UTC),
        }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_access_token(user):
    user_token = UserToken.objects.create(
        id=uuid.uuid4(), user=user, is_active=True
        )
    if user_token:
        access_token = usertoken(user_token.id)
        return access_token