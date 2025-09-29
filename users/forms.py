from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add bootstrap classes to widgets
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


class BootstrapPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
