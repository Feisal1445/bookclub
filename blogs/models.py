from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar

# Create your models here.
# Create your models here.
class User(AbstractUser):
    """User model used for authentication and microblog authoring."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\w{3,}$',
            message='Username must contain at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    bio = models.CharField(max_length=520, blank=True)



    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url



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

    location=models.CharField(max_length=100, blank=False)
    mission_statement=models.CharField(max_length=200, blank=False)
    description=models.CharField(max_length=500, blank=False)
