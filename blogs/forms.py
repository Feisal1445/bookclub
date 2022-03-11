from django import forms
from django.core.validators import RegexValidator
from .models import User, Club
from django.utils.safestring import mark_safe


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio']
    new_password= forms.CharField(
        label='Password ',
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'[A-Z]',
                message = 'Password must contain at least one uppercase letter.'
            ),
            RegexValidator(
                regex=r'[a-z]',
                message = 'Password must contain at least one lowercase letter.'
            ),
            RegexValidator(
                regex=r'[0-9]',
                message = 'Password must contain at least one number.'
            )
        ]
    )
    password_confirmation= forms.CharField(label='Password confirmation ', widget=forms.PasswordInput())


def clean(self):
    super().clean()
    new_password = self.cleaned_data.get('new_password')
    password_confirmation = self.cleaned_data.get('password_confirmation')
    if new_password != password_confirmation:
        self.add_error('passwords dont match')

def save(self):
    super.save(commit = False)
    user = User.objects.create_user(
        first_name = form.cleaned_data.get('first_name'),
        last_name = form.cleaned_data.get('last_name'),
        bio = form.cleaned_data.get('bio'),
        statment = form.cleaned_data.get('statment'),
        level = form.cleaned_data.get('level'),
        password = form.cleaned_data.get('password'),
        username = form.cleaned_data.get('username')

    )
    return user

class SignInForm(forms.Form):
    username = forms.CharField(label = 'Username')
    password = forms.CharField(label=mark_safe('<br />Password'), widget=forms.PasswordInput())


class ClubCreationForm(forms.ModelForm):
    """Form enabling logged user to create a new club."""
    class Meta:
        model = Club
        fields = ['name', 'owner', 'description']
        widgets = {
            'owner': forms.HiddenInput(attrs = {'is_hidden': True})
        }
