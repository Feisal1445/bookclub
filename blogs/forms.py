from django import forms
from django.core.validators import RegexValidator
from .models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio']
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
        email = form.cleaned_data.get('email')

    )
    return user