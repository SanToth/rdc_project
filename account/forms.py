from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=25, 
        widget=forms.TextInput(
        attrs={
                'class': 'form-control',
                'id': 'floatingInput', 
                'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'class': 'form-control',
            'id': 'floatingPassword', 
            'placeholder': 'Password'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-control',
                                          'id': 'floatingOldPassword',
                                          'placeholder': 'Old Password'}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control',
                                          'class': 'form-control',
                                          'id': 'floatingNewPassword1',
                                          'placeholder': 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control',
                                          'class': 'form-control',
                                          'id': 'floatingNewPassword2',
                                          'placeholder': 'New Password (again)'}),
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
