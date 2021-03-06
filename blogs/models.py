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

class Membership(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'club'], name='unique_user_club'),
        ]

    class UserTypes(models.TextChoices):
        NON_MEMBER = 'NM'
        MEMBER = 'MB'
        OFFICER = 'OF'
        OWNER = 'OW'

    class Application(models.TextChoices):
        PENDING = 'P'
        APPROVED = 'A'
        DENIED = 'D'

    """Attributes of a user in the club"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=False)
    personal_statement = models.CharField(max_length=500, blank=False)
    application_status = models.CharField(max_length=10, choices=Application.choices, default=Application.PENDING)
    user_type = models.CharField(max_length=10, choices=UserTypes.choices, default=UserTypes.NON_MEMBER)

    def approve_membership(self):
        """Application is approved and user becomes a memeber of the club."""
        if self.user_type == self.UserTypes.NON_MEMBER:
            self.application_status = self.Application.APPROVED
            self.user_type = self.UserTypes.MEMBER
            self.save()

    def deny_membership(self):
        """Application is denied and doesn't proceed."""
        if self.user_type == self.UserTypes.NON_MEMBER:
            self.application_status = self.Application.DENIED
            self.save()

    def promote_to_officer(self):
        """Member promoted to officer type of membership."""
        if self.user_type == self.UserTypes.MEMBER:
            self.user_type = self.UserTypes.OFFICER
            self.save()

    def demote_to_member(self):
        """Officer demoted into member type of membership."""
        if self.user_type == self.UserTypes.OFFICER and Club.objects.filter(name=self.club.name, owner=self.user).count() == 0:
                self.user_type = self.UserTypes.MEMBER
                self.save()

    def transfer_ownership(self, new_owner):
        """Previous owner transfers ownership, new owner gains ownership powers."""
        try:
            new_owner_membership = Membership.objects.get(user = new_owner, club = self.club)
        except:
            raise Exception("User is not a member of the club.")
        else:
            if new_owner_membership.user_type == self.UserTypes.OFFICER:
                self.club.owner = new_owner
                self.user_type = self.UserTypes.OFFICER
                new_owner_membership.user_type = self.UserTypes.OWNER

                new_owner_membership.save()
                self.club.save()
                self.save()
            else:
                raise Exception("Member must be an officer to transfer ownership.")


    def kick_member(self):
        """User is removed from the club and deleted from the database."""
        if self.user_type in [self.UserTypes.MEMBER, self.UserTypes.OFFICER]:
            self.delete()
            return True
        return False

    def leave(self):
        """User is leaves the club and deleted from the database."""
        if self.user_type in [self.UserTypes.MEMBER, self.UserTypes.OFFICER]:
            self.delete()
            return True
        return False

    # Define which user types share the same identities
    USER_TYPE_IDENTITIES = {
        UserTypes.NON_MEMBER: [UserTypes.NON_MEMBER],
        UserTypes.MEMBER: [UserTypes.MEMBER]
    }

    # An Officer is a Member and an Officer
    USER_TYPE_IDENTITIES[UserTypes.OFFICER] = USER_TYPE_IDENTITIES[UserTypes.MEMBER] + [
        UserTypes.OFFICER
    ]

    # An Owner is a Member, an Officer, and an Owner
    USER_TYPE_IDENTITIES[UserTypes.OWNER] = USER_TYPE_IDENTITIES[UserTypes.OFFICER] + [
        UserTypes.OWNER
    ]

    def get_user_types(self):
        return self.USER_TYPE_IDENTITIES[self.user_type]


    USER_TYPE_NAMES = {
        UserTypes.NON_MEMBER: "a Non-Member",
        UserTypes.MEMBER: "a Member",
        UserTypes.OFFICER: "an Officer",
        UserTypes.OWNER: "the Owner"
    }

    def get_user_type_name(self):
        return self.USER_TYPE_NAMES[self.user_type]

