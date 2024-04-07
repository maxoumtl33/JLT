from django import forms
from django.forms import ModelForm
from .models import Livraison

class LivraisonForm(ModelForm):
    class Meta:
        model = Livraison
        fields = ('status',)