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
from django.forms import modelformset_factory

class ChecklistDocumentForm(forms.ModelForm):
    class Meta:
        model = ChecklistDocument
        fields = ['document']
    

ChecklistDocumentFormSet = modelformset_factory(
    ChecklistDocument,
    form=ChecklistDocumentForm,
    extra=1,  # Ensures a new empty form always exists
    can_delete=True
)


from django import forms
from django_select2.forms import Select2Widget
from .models import Product

class AdjustProductQuantityForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=Select2Widget(attrs={'class': 'select2'}),
        label="Sélectionner un produit",  # Label for the field itself
        empty_label="-- Choisissez un produit --"  # Label for the default empty choice
    )
    quantity = forms.IntegerField(min_value=1, label="Quantité")




class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['status']  # Only include fields you want to update

class ProductForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['product']

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category']  # Include fields you want in the form
        labels = {
            'name': 'Nom du produit',  # Change the label for the 'name' field
            'category': 'Categorie',  # Change the label for the 'category' field
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop the user from kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.user:  # This will set the 'created_by' if the user is passed
            product.created_by = self.user  # If 'created_by' is a part of Product, ensure it is declared in the model
        if commit:
            product.save()
            self.save_m2m()  # Save the ManyToMany relationship
        return product



class LivraisonForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('status', 'commentaire','nom_client_signature', 'date_signature', 'signature')
        widgets = {
            'status': forms.HiddenInput(),  # Hide the status field as it will be set automatically
            'commentaire': forms.Textarea(attrs={
                'placeholder': 'Ajoutez un commentaire...',
                'class': 'form-control',
                'rows': 4,
            }),
        }

class LivraisonFeuilleForm(forms.ModelForm):
    
    class Meta:
        model = Livraison
        fields = ('nom', 'statut',
                  'commentairedispatch', 'recuperation', 'status', 'date', 'journee')
     
    def __init__(self, *args, **kwargs):
        super(LivraisonFeuilleForm, self).__init__(*args, **kwargs)
        
        # Customizing 'statut' field to show only the option with id = 21
        self.fields['statut'].queryset = self.fields['statut'].queryset.filter(id=21)
        self.fields['statut'].label = "Route"  # Change the label of statut field

        # Assuming 'journee' is a foreign key; modify queryset as needed
        self.fields['journee'].queryset = self.fields['journee'].queryset.order_by('-date')  # Reverse order if date_created exists

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

modes = (
        ("driving", "driving"),
    )

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
        fields = ('nom', 'infodetail', 'commentairedispatch','heure_livraison', 'recuperation')




class XLSXUploadForm(forms.Form):
    file = forms.FileField(required=True)


class LivraisonDragFormtoday(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('heure_depart', 'nom', 'infodetail',  'livreur', 'aidelivreur', 'statut', 'commentairedispatch', 'recuperation', 'retourtraiteur')

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['livreur', 'date', 'start_time', 'notes']


class LivraisonsVentesForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ('nom_client', 'contact_site', 'app')
        labels = {
            'nom_client': 'Nom du client',  
            'contact_site': 'Contact Client',
              'app': 'Etage'  # You can also change the label for photos if needed
        }

class RoutedetailForm(forms.ModelForm):
    livreur = forms.ModelMultipleChoiceField(
        queryset=Livreur.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Livreurs'
    )

    class Meta:
        model = Route  # Replace with your actual model name
        fields = ['livreur', 'heure_depart', 'commentaire']  # Ensure these fields match your model's fields

class LoadingDockForm(forms.ModelForm):
    class Meta:
        model = LoadingDock
        fields = ['name','address','adresse_compagny', 'photo', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'entreprise"}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse du Dock'}),
            'adresse_compagny': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Adresse de l'entreprise"}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description du Dock', 'rows': 4}),
        }

class PhotoUploadForm(forms.ModelForm):
    image = forms.FileField(required=True)

    class Meta:
        model = Photo
        fields = ("image",)

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name']
        labels = {
            'name': 'Véhicule',  # Change 'Vehicle Name' to whatever custom label you wan
        }


class PhotoRecupUploadForm(forms.ModelForm):
    image = forms.FileField(required=True)

    class Meta:
        model = PhotoRecup
        fields = ("image",)

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
    date = forms.DateField(label='', widget=forms.DateInput(attrs={'type': 'date'}))
    lieu = forms.CharField(label='Adresse événement', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    num_contrat = forms.CharField(label='Numéro de contrat', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nb_convive = forms.IntegerField(label='Nombre de convives', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    heure_livraison = forms.TimeField(label='Heure de livraison', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    conseillere = forms.ModelChoiceField(queryset=Conseiller.objects.all())   

class ChecklistInfosForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['type_service', 'occasion', 'depart_traiteur', 'heure_arrive', 'heure_convives', 'debut_cocktail', 'debut_repas', 'fin_evenement', 'commodite', 'fourni_client', 'fourni_salle']

    type_service = forms.CharField(label='Type de service', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Coktail, Banquet, bbq, ...'}),required=False)
    occasion = forms.CharField(label='Occasion', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Mariage, anniversaire, ...'}),required=False)
    depart_traiteur = forms.TimeField(label='Départ du traiteur', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),required=False)
    heure_arrive = forms.TimeField(label='Arrivée sur place', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),required=False)
    heure_convives = forms.TimeField(label='Arrivée des convives', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),required=False)
    debut_cocktail = forms.TimeField(label='Début du coktail', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),required=False)
    debut_repas = forms.TimeField(label='Début du repas', widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),required=False)
    fin_evenement = forms.TimeField(label="Fin de l'événement", widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),required=False)
    commodite = forms.CharField(label='Commodités',  max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Four, frigo,...'}),required=False)
    fourni_client = forms.CharField(label='Matériel fourni par client', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    fourni_salle = forms.CharField(label='Matériel dans la salle', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)

from django import forms

from django import forms

from django import forms
from .models import Submission  # Ensure you import your Submission model

from django import forms
from .models import Submission, DeliveryMode, Menu

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'submission_type', 'company_name', 'event_location', 'contact_person',
            'ordered_by', 'phone', 'email', 'billing_address',
            'payment_mode', 'date', 'event_time', 'guest_count',
            'delivery_time', 'budget', 'service_count', 'sub_menus', 'commentaire', 'client', 'etage', 'dock_livraison', 
            'escalier', 'ascenseur', 'carte_dock', 'type_prise_de_commande'  # sub_menus included
        ]
        widgets = {
            'type_prise_de_commande': forms.Select(attrs={'class': 'form-control'}),
            'submission_type': forms.Select(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'ordered_by': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'billing_address': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_mode': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'guest_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'service_count': forms.TextInput(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),  # Use Textarea with height configured
            # Note: delivery_modes handled dynamically via JS
        }

    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        # Add menu choices for the sub_menus field dynamically
        self.fields['sub_menus'].queryset = Menu.objects.all()  # Adjust based on your conditions




class SearchFormInv(forms.Form):
    query = forms.CharField(label='Objet à chercher', max_length=100)

class SearchFormChecklist(forms.Form):
    query = forms.CharField(label='Checklist à chercher', max_length=100)

class QuantityUpdateForm(forms.Form):
    quantity = forms.IntegerField(min_value=0, label='Quantity')

class DateFilterForm(forms.Form):
    date = forms.CharField(label='', widget=forms.DateInput(attrs={'type': 'date'}))





from django import forms
from .models import Menu

class OrderForm(forms.Form):
    # Existing fields...
    delivery_mode = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This can be changed to a different widget if needed
        required=False,
    )



class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['nom','date', 'livreur', 'heure_depart']
        widgets = {
            'heure_depart': forms.Select(choices=Route.choiceheures),
            'livreur': forms.Select(),  # Optional: customize widget if needed
            'date': forms.DateInput(attrs={'type': 'date'}),
        }



PhotoTachesFormSet = inlineformset_factory(
    Tacheafaire,  # The parent model
    Phototaches,      # The model the formset is for
    form=PhotoTachesForm,  # Use the PhotoForm we defined above
    extra=7,  # Number of additional blank photo forms to display
    
)

# forms.py
from django import forms
from .models import Livreur

class LivraisonFilterForm(forms.Form):
    livreur = forms.ModelChoiceField(queryset=Livreur.objects.all(), required=False, label='Livreur')
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


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

class ChecklistItemQForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['quantity']  # Only include the quantity field

    def __init__(self, *args, **kwargs):
        checklist = kwargs.get('checklist')
        product = kwargs.get('product')
        super().__init__(*args, **kwargs)

        # Store checklist and product for later use
        self.checklist = checklist
        self.product = product

    def save(self, *args, **kwargs):
        # Ensure that the checklist and product are set before saving
        self.instance.checklist = self.checklist
        self.instance.product = self.product  # Associate the product with this checklist item
        return super().save(*args, **kwargs)


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['commentairevente']
        widgets = {
            'commentairevente': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Écrire un commentaire...'}),
        }

class CommentairemdForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['commentairemd']
        widgets = {
            'Commentaire': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Écrire un commentaire...'}),
        }


class ChecklistMDPhotoForm(forms.ModelForm):
    class Meta:
        model = ChecklistMDPhoto
        fields = ['image']

ChecklistMDPhotoFormSet = modelformset_factory(ChecklistMDPhoto, form=ChecklistMDPhotoForm, extra=5)

class ChecklistRecupPhotoForm(forms.ModelForm):
    class Meta:
        model = ChecklistRecupPhoto
        fields = ['image']

ChecklistRecupPhotoFormSet = modelformset_factory(ChecklistRecupPhoto, form=ChecklistRecupPhotoForm, extra=5)

class RapportForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['rapportmd']

class RapportRecupForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['rapportrecup']


# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import (
    UniteMesure, Departement, Fournisseur, Ingredient,
    CatalogueFournisseur, Recette, SousRecette,
    RecetteIngredient, SousRecetteIngredient, Commande
)

class UniteMesureForm(forms.ModelForm):
    class Meta:
        model = UniteMesure
        fields = ['nom', 'symbole']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'symbole': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'email', 'telephone', 'adresse', 'contact_principal']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_principal': forms.TextInput(attrs={'class': 'form-control'}),
        }

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['nom', 'unite_mesure', 'stock_reel', 'stock_alerte', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'unite_mesure': forms.Select(attrs={'class': 'form-control'}),
            'stock_reel': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_alerte': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CatalogueFournisseurForm(forms.ModelForm):
    class Meta:
        model = CatalogueFournisseur
        fields = ['fournisseur', 'ingredient', 'prix', 'date_debut', 'date_fin', 
                  'reference_fournisseur', 'conditionnement', 'delai_livraison', 'actif']
        widgets = {
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
            'ingredient': forms.Select(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reference_fournisseur': forms.TextInput(attrs={'class': 'form-control'}),
            'conditionnement': forms.TextInput(attrs={'class': 'form-control'}),
            'delai_livraison': forms.NumberInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ['nom', 'description', 'explication_fabrication', 'photo', 
                  'departement', 'temps_preparation', 'temps_cuisson', 'portions']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'explication_fabrication': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'departement': forms.Select(attrs={'class': 'form-control'}),
            'temps_preparation': forms.NumberInput(attrs={'class': 'form-control'}),
            'temps_cuisson': forms.NumberInput(attrs={'class': 'form-control'}),
            'portions': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RecetteIngredientForm(forms.ModelForm):
    class Meta:
        model = RecetteIngredient
        fields = ['ingredient', 'quantite']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-control ingredient-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
        }

class SousRecetteForm(forms.ModelForm):
    class Meta:
        model = SousRecette
        fields = ['nom', 'explication_fabrication', 'quantite']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'explication_fabrication': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class SousRecetteIngredientForm(forms.ModelForm):
    class Meta:
        model = SousRecetteIngredient
        fields = ['ingredient', 'quantite']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
        }

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['fournisseur', 'date_livraison_prevue', 'notes']
        widgets = {
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
            'date_livraison_prevue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formsets pour gérer les relations many-to-many
RecetteIngredientFormSet = inlineformset_factory(
    Recette, RecetteIngredient,
    form=RecetteIngredientForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)

SousRecetteFormSet = inlineformset_factory(
    Recette, SousRecette,
    form=SousRecetteForm,
    extra=0,
    can_delete=True,
)

SousRecetteIngredientFormSet = inlineformset_factory(
    SousRecette, SousRecetteIngredient,
    form=SousRecetteIngredientForm,
    extra=1,
    can_delete=True,
)

class ImportCatalogueForm(forms.Form):
    fournisseur = forms.ModelChoiceField(
        queryset=Fournisseur.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Fournisseur"
    )
    fichier = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv,.xlsx'}),
        label="Fichier catalogue (CSV ou Excel)"
    )
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Date de début de validité"
    )