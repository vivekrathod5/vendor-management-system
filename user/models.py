import uuid
from django.db import models

class User(models.Model):
    class Meta:
        db_table = 'users'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class UserToken(models.Model):
    class Meta:
        db_table = 'users_token'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    user = models.ForeignKey(User, related_name='token', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)