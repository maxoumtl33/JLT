from django import forms
from django.forms import ModelForm
from .models import *
from datetime import datetime, timedelta, time
from .models import ItemInv
from .models import Checklist
from .models import Phototaches
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.forms import inlineformset_factory
from .models import Livraison, Photo




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
        fields = ('nom','statut', 'heure_depart','aidelivreur',  'livreur', 'retourtraiteur', 'commentairedispatch', 'recuperation', 'status', 'date', 'journee')

modes = (
    ("driving", "driving"),
)

class OrderCuisineForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=ItemCuisine.objects.all(), 
        required=False,
        label='Select Existing Item'
    )
    new_item_name = forms.CharField(
        max_length=200, 
        required=False, 
        label='Or Create a New Item'
    )
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = OrderCuisine
        fields = ['item', 'new_item_name', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get("item")
        new_item_name = cleaned_data.get("new_item_name")

        if not item and not new_item_name:
            raise forms.ValidationError('You must either select an existing item or enter a new item name.')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(OrderCuisineForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = ItemCuisine.objects.all()

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
        fields = ('infodetail','heure_livraison', 'commentairedispatch', 'recuperation')

class LivraisonDragFormtoday(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('heure_depart', 'nom', 'infodetail',  'livreur', 'aidelivreur', 'statut', 'commentairedispatch', 'recuperation', 'retourtraiteur')

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['livreur', 'date', 'start_time', 'end_time', 'notes']


class LivraisonsVentesForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('nom_client', 'contact_site', 'app')

class RoutedetailForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('livreur', 'heure_depart')

class LoadingDockForm(forms.ModelForm):
    class Meta:
        model = LoadingDock
        fields = ['address', 'photo', 'description']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse du Dock'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description du Dock', 'rows': 4}),
        }
        
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']

class PhotoTachesForm(forms.ModelForm):
    class Meta:
        model = Phototaches
        fields = ['image', 'caption']

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Tacheafaire
        fields = ('status','commentaire')

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

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['nom','date', 'livreur', 'heure_depart']
        widgets = {
            'heure_depart': forms.Select(choices=Route.choiceheures),
            'livreur': forms.Select(),  # Optional: customize widget if needed
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# Create a formset for the Photo model linked to the Livraison
PhotoFormSet = inlineformset_factory(
    Livraison,  # The parent model
    Photo,      # The model the formset is for
    form=PhotoForm,  # Use the PhotoForm we defined above
    extra=3,  # Number of additional blank photo forms to display
    
)

PhotoTachesFormSet = inlineformset_factory(
    Tacheafaire,  # The parent model
    Phototaches,      # The model the formset is for
    form=PhotoTachesForm,  # Use the PhotoForm we defined above
    extra=7,  # Number of additional blank photo forms to display
    
)

# Form for Recupfrigo
class RecupfrigoForm(forms.ModelForm):
    livraison = forms.ModelChoiceField(queryset=Livraison.objects.none(), empty_label="Sélectionnez une Livraison")

    class Meta:
        model = Recupfrigo
        fields = ['livraison', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the parent constructor first

        # Get today's date
        today = date.today()

        # Set up the valid modes_envoi
        valid_modes_envoi = [
            "Porcelaine",
            "Chaud et porcelaine",
            "Porcelaine et bois",
            "Plateau de bois",
            "Froid et bois",
            "Chaud et jetable",
        ]

        # Get the Livraison IDs that are already associated with a Recupfrigo
        used_livraison_ids = Recupfrigo.objects.values_list('livraison_id', flat=True)

        # Filter Livraison queryset based on today's date, mode_envoi, and exclude used Livraisons
        self.fields['livraison'].queryset = Livraison.objects.filter(
            date_livraison=today,
            mode_envoi__in=valid_modes_envoi,
            recuperation = False,
        ).exclude(id__in=used_livraison_ids)

# Form for RecupfrigoItem
# forms.py
class RecupfrigoItemForm(forms.ModelForm):
    class Meta:
        model = RecupfrigoItem
        fields = ['item_name', 'quantity']
        

       

# Formset for RecupfrigoItem
RecupfrigoItemFormset = inlineformset_factory(
    Recupfrigo,
    RecupfrigoItem,
    form=RecupfrigoItemForm,
    extra=9,  # Number of empty forms displayed initially

)
# Form for Recuplivreur
class RecuplivreurForm(forms.ModelForm):
    class Meta:
        model = Recuplivreur
        fields = ['date']
        widgets = {
                'date': forms.DateInput(attrs={'type': 'date'}),
            }

# Form for RecuplivreurItem
class RecuplivreurItemForm(forms.ModelForm):
    class Meta:
        model = RecuplivreurItem
        fields = ['item_name', 'quantity']

# Formset for RecuplivreurItem
# Formset for RecupfrigoItem
RecuplivreurItemFormset = inlineformset_factory(
    Recuplivreur,
    RecuplivreurItem,
    form=RecuplivreurItemForm,
    extra=9,  # Number of empty forms displayed initially

)
