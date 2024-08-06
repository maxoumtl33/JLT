from django import forms
from django.forms import ModelForm
from .models import *
from datetime import datetime, timedelta, time
from .models import ItemInv
from .models import Checklist
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['status']  # Only include fields you want to update

class ProductForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['product']

class LivraisonForm(ModelForm):
    class Meta:
        model = Livraison
        fields = ('status','commentaire')

class LivraisonFeuilleForm(ModelForm):
    class Meta:
        model = Livraison
        fields = ('nom','statut', 'heure_depart','aidelivreur',  'livreur', 'retourtraiteur', 'commentairedispatch', 'recuperation', 'status', 'date')

modes = (
    ("driving", "driving"),
)

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = []

class DistanceForm(ModelForm):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    from_location = forms.ModelChoiceField(label="De", required=True, queryset=Livraison.objects.filter(date=tomorrow))
    to_location = forms.ModelChoiceField(label="Vers", required=True, queryset=Livraison.objects.filter(date=tomorrow))
    mode = forms.ChoiceField(choices= modes, required=True)
    class Meta:
        model = Distances
        exclude = ['created_at', 'edited_at','distance_km', 'duration_mins','duration_traffic_mins']

class DistanceFormMidi(ModelForm):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    from_location = forms.ModelChoiceField(label="De", required=True, queryset=Livraison.objects.filter(date=tomorrow))
    to_location = forms.ModelChoiceField(label="Vers", required=True, queryset=Livraison.objects.filter(date=tomorrow))
    mode = forms.ChoiceField(choices= modes, required=True)
    class Meta:
        model = Distances
        exclude = ['created_at', 'edited_at','distance_km', 'duration_mins','duration_traffic_mins']

class DistanceFormAprem(ModelForm):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    from_location = forms.ModelChoiceField(label="De", required=True, queryset=Livraison.objects.filter(date=tomorrow))
    to_location = forms.ModelChoiceField(label="Vers", required=True, queryset=Livraison.objects.filter(date=tomorrow))
    mode = forms.ChoiceField(choices= modes, required=True)
    class Meta:
        model = Distances
        exclude = ['created_at', 'edited_at','distance_km', 'duration_mins','duration_traffic_mins']


class LivraisonDragForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('heure_depart', 'nom', 'infodetail','heure_livraison',  'livreur', 'aidelivreur', 'statut', 'commentairedispatch', 'recuperation', 'retourtraiteur')

class LivraisonDragFormtoday(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('heure_depart', 'nom', 'infodetail',  'livreur', 'aidelivreur', 'statut', 'commentairedispatch', 'recuperation', 'retourtraiteur')


class LivraisonsVentesForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('nom_client', 'contact_site', 'app')

class RoutedetailForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('livreur', 'heure_depart')
        
class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ['photo']


class ItemInvForm(forms.ModelForm):
    class Meta:
        model = ItemInv
        fields = ['name']

class ChecklistForm(forms.ModelForm):
   class Meta:
        model = Checklist
        fields = ['name', 'date', 'lieu', 'num_contrat', 'nb_convive', 'heure_livraison', 'conseillere', 'md']

   name = forms.CharField(label='Nom du contrat', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   date = forms.CharField(label='', widget=forms.DateInput(attrs={'type': 'date'}))
   lieu = forms.CharField(label='Adresse événement', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   num_contrat = forms.CharField(label='Numéro de contrat', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   nb_convive = forms.CharField(label='Nombre de convives', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   heure_livraison = forms.CharField(label='Heure de livraison', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   conseillere = forms.CharField(label='Nom du/de la conseiller(e)', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   md = forms.CharField(label='Nom du MD', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class SearchFormInv(forms.Form):
    query = forms.CharField(label='Objet à chercher', max_length=100)

class SearchFormChecklist(forms.Form):
    query = forms.CharField(label='Checklist à chercher', max_length=100)


class DateFilterForm(forms.Form):
    date = forms.CharField(label='', widget=forms.DateInput(attrs={'type': 'date'}))
