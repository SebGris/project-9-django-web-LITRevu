from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom d'utilisateur",
                'style': 'border:2px solid #333; border-radius:4px; padding:8px; width:100%;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password1'].label = ''
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = ''
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'style': 'border:2px solid #333; border-radius:4px; padding:8px; width:100%;'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmation du mot de passe',
            'style': 'border:2px solid #333; border-radius:4px; padding:8px; width:100%;'
        })


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d’utilisateur',
            'style': 'border: 2px solid #007bff; border-radius: 4px; padding: 8px;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'style': 'border: 2px solid #007bff; border-radius: 4px; padding: 8px;'
        })
    )
