from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class FollowUsersForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur",
            'autocomplete': 'off',
            'style': 'border:2px solid #333;'
        })
    )
