from django import forms
from django.forms import ModelForm
from .models import *
from datetime import datetime, timedelta, time

class LivraisonForm(ModelForm):
    class Meta:
        model = Livraison
        fields = ('status',)

modes = (
    ("driving", "driving"),
)

class DistanceForm(ModelForm):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    from_location = forms.ModelChoiceField(label="De", required=True, queryset=Livraison.objects.all())
    to_location = forms.ModelChoiceField(label="Vers", required=True, queryset=Livraison.objects.all())
    mode = forms.ChoiceField(choices= modes, required=True)
    class Meta:
        model = Distances
        exclude = ['created_at', 'edited_at','distance_km', 'duration_mins','duration_traffic_mins']


