from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class RegisterTouristForm(UserCreationForm):
    passport_number = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username',  'email', 'passport_number', 'password1', 'password2',]
        labels = {

            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'username': 'Username',
            'passport_number': 'Passport Number',
            'password1': 'Password',
            'password2': 'Password Confirmation',

        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Fist Name',
                'id': 'first_id'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Last Name',
                'id': 'last_id'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username',
                'id': 'last_id'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email',
                'id': 'email_id'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password',
                'id': 'password_id'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
                'id': 'confirm_id'
            })
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'tourist'
        user.is_active = False
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter Email',
            'class': 'form-field animation3',
            'required': True,
        }),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'form-field animation4',
            'required': True,
        }),
        label="Password",
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise ValidationError("Invalid email or password.")
            if not user.is_active:
                raise ValidationError("User account is disabled.")
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Email'})


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})

