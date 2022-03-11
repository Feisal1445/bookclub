from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class User(AbstractUser):
    """User model used for authentication and microblog authoring."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    bio = models.CharField(max_length=520, blank=True)


class Club(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z][a-zA-Z0-9 ]+',
            message='Club name must start with a letter and contain only letters, number, and spaces.'
        )])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    location=models.CharField(max_length=100, blank=True)
    mission_statement=models.CharField(max_length=200, blank=True)
    description=models.TextField(max_length=500, blank=False)
