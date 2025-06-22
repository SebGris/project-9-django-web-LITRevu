from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={'style': 'border:2px solid #333; width:100%; text-align:center;'}),
            'description': forms.Textarea(attrs={'style': 'border:2px solid #333; width:100%;', 'rows': 8}),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Commentaire',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'headline': forms.TextInput(attrs={'style': 'border:2px solid #333; width:100%;'}),
            'body': forms.Textarea(attrs={'style': 'border:2px solid #333; width:100%;', 'rows': 8}),
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
