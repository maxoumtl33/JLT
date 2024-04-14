from django import forms
from django.forms import ModelForm
from .models import *

class LivraisonForm(ModelForm):
    class Meta:
        model = Livraison
        fields = ('status',)

modes = (
    ("driving", "driving"),
)

class DistanceForm(ModelForm):
    from_location = forms.ModelChoiceField(label="De", required=True, queryset=Client.objects.all())
    to_location = forms.ModelChoiceField(label="Vers", required=True, queryset=Client.objects.all())
    mode = forms.ChoiceField(choices= modes, required=True)
    class Meta:
        model = Distances
        exclude = ['created_at', 'edited_at','distance_km', 'duration_mins','duration_traffic_mins']


