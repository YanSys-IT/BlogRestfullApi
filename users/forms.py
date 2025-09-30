from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    profile_picture = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css = 'form-control'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': f'{css} textarea'})
            else:
                field.widget.attrs.update({'class': css})

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'bio', 'birth_date', 'profile_picture')


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


class BootstrapPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
