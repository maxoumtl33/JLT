from django.http import HttpResponse
from django.shortcuts import render, redirect
from listings.models import Livraison
from .models import Livreur
from .models import Tacheafaire
from .models import Journee
from .models import Photo
from .models import Phototaches
from .models import Route, Recupfrigo
from django.views.generic.list import ListView
from .models import Distances
from .models import Checklist, Recuplivreur
from django.shortcuts import get_object_or_404
from .forms import LivraisonForm,PhotoTachesForm,PhotoTachesFormSet
from .forms import LivraisonFeuilleForm
from .forms import LivraisonDragForm
from .forms import LivraisonDragFormtoday, TaskUpdateForm
from .forms import LivraisonsVentesForm, RoutedetailForm
from django.urls import reverse
import json
from .forms import DistanceForm
from tablib import Dataset
from .ressources import LivraisonResource
from django.utils.timezone import now
from datetime import datetime, timedelta, time
from .models import Recuperation
import googlemaps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views import View
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from .models import *
from .models import ItemInv
from django.shortcuts import render
from django.contrib import messages
from .models import Item
from openpyxl import load_workbook
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
from .forms import ItemInvForm
from .forms import SearchFormInv
from .models import Product, Checklist, ChecklistItem
from .forms import PhotoForm, PhotoFormSet
from .forms import RouteForm
from .forms import *
from .forms import ChecklistForm
from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from .utils import add_quantity_to_checklist, remove_quantity_from_checklist
from .forms import DateFilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import UpdateView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.utils import timezone
import random
import requests

def delivery_map(request):
    today = now().date()
    deliveries = Livraison.objects.filter(date=today).exclude(lat__isnull=True, lng__isnull=True)

    # Serialize the deliveries data into JSON-friendly format
    deliveries_data = [
        {
            'nom': d.nom,
            'latitude': float(d.lat),
            'longitude': float(d.lng),
            'heure_livraison': d.heure_livraison
        }
        for d in deliveries if d.lat and d.lng
    ]

    key = settings.GOOGLE_API_KEY
    return render(request, 'listings/delivery_map.html', {
        'deliveries': deliveries_data,
        'key': key,
    })

def geocode_all_livraisons(request):
    if request.method == 'GET':  # Ensure the method is GET
        livraisons = Livraison.objects.filter(lat__isnull=True, lng__isnull=True, place_id__isnull=True)

        if livraisons.exists():
            gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

            for livraison in livraisons:
                if livraison.adress and livraison.country and livraison.zipcode and livraison.city:
                    adress_string = f"{livraison.adress}, {livraison.zipcode}, {livraison.city}, {livraison.country}"

                    result = gmaps.geocode(adress_string)
                    if result:
                        lat = result[0].get('geometry', {}).get('location', {}).get('lat', None)
                        lng = result[0].get('geometry', {}).get('location', {}).get('lng', None)
                        place_id = result[0].get('place_id', None)

                        # Update the livraison instance
                        livraison.lat = lat
                        livraison.lng = lng
                        livraison.place_id = place_id
                        livraison.save()

            return JsonResponse({'success': True, 'message': 'Geocoding completed'})
        else:
            return JsonResponse({'success': False, 'message': 'No livraisons need geocoding'})
    
    # If the request method is not GET
    return JsonResponse({'success': False, 'error': 'Invalid request method. Use GET.'})

TASK_NAMES = ['Nettoyer machines à café', 'Nettoyer intérieur des camions et checker essence', 
              'Faire boites de thé + café', 'Nettoyer dock de livraison']

import random

TASK_NAMES = ['Nettoyer machines à café', 'Nettoyer intérieur des camions', 
              'Faire boites de thé + café', 'Nettoyer dock de livraison', 'Mettre essence camions']

def create_random_task(request):
    # List of names to choose from
    livreur_names = ["Mohamed", "Samuel", "Alex", "Jef", "Zayd"]

    # Check if the number of livreurs is less than the number of tasks
    if len(livreur_names) < len(TASK_NAMES):
        return redirect('acceuilresponsables')  # Handle error: more tasks than livreurs

    # Fetch Livreur instances corresponding to names
    livreurs = []
    for name in livreur_names:
        try:
            livreur = Livreur.objects.get(nom=name)
            livreurs.append(livreur)
        except Livreur.DoesNotExist:
            return redirect('acceuilresponsables')  # Handle case where a Livreur is missing

    # Set the date for tomorrow
    tomorrow = timezone.now().date() + timezone.timedelta(days=1)

    # Shuffle the task names to ensure randomness
    random.shuffle(TASK_NAMES)

    # Assign a random task to each livreur
    for i, livreur in enumerate(livreurs):
        if i < len(TASK_NAMES):
            random_task = TASK_NAMES[i]
            # Create the task
            Tacheafaire.objects.create(
                livreur=livreur,  # Livreur instance
                nom=random_task,
                date=tomorrow
            )

    return redirect('acceuilresponsables')


@csrf_exempt
@require_POST
def create_routes(request):
    try:
        # Calculate tomorrow's date
        tomorrow = timezone.now().date() + timedelta(days=1)

        # Create 20 routes
        routes = []
        for i in range(1, 21):
            route = Route(
                nom=f"{i}",
                date=tomorrow,
                heure_depart="08h00"  # You can set this to any default value
            )
            route.save()
            routes.append(route)

        return JsonResponse({'success': True, 'routes': [route.id for route in routes]})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def create_routesn(request):
    try:
        # Calculate tomorrow's date
        tomorrow = timezone.now().date() + timedelta(days=2)

        # Create 20 routes
        routes = []
        for i in range(1, 21):
            route = Route(
                nom=f"{i}",
                date=tomorrow,
                heure_depart="08h00"  # You can set this to any default value
            )
            route.save()
            routes.append(route)

        return JsonResponse({'success': True, 'routes': [route.id for route in routes]})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def create_routesnn(request):
    try:
        # Calculate tomorrow's date
        tomorrow = timezone.now().date() + timedelta(days=3)

        # Create 20 routes
        routes = []
        for i in range(1, 21):
            route = Route(
                nom=f"{i}",
                date=tomorrow,
                heure_depart="08h00"  # You can set this to any default value
            )
            route.save()
            routes.append(route)

        return JsonResponse({'success': True, 'routes': [route.id for route in routes]})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class ChecklistItemDeleteAjaxView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs.get('pk')
        try:
            item = ChecklistItem.objects.get(pk=item_id)
            product = item.product
            quantity = item.quantity
            item.delete()
            # Adjust the product quantity
            if product:
                product.adjust_quantity(quantity)
            response_data = {'status': 'success', 'message': 'Objet bien supprimé :)'}
        except ChecklistItem.DoesNotExist:
            response_data = {'status': 'error', 'message': 'Checklist item not found.'}

        return JsonResponse(response_data)


def voir_checklist(request):

    checklists = Checklist.objects.all().order_by('-added_on')
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"

    if request.method == 'GET' and 'date' in request.GET:
       form = DateFilterForm(request.GET)
       if form.is_valid():
            date = form.cleaned_data['date']
            checklists = checklists.filter(date=date)
    else:
        form = DateFilterForm()

    paginator = Paginator(checklists, 10)  # Show 10 events per page

    page = request.GET.get('page')
    try:
        checklists = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        checklists = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        checklists = paginator.page(paginator.num_pages)

    context = {

        'checklists': checklists,
        'form': form,
        'encours': encours,
        'valide': valide,
        'refuse': refuse,
    }
    return render(request, 'listings/voir-checklist.html', context)

def checklistvoir_detail(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    checklist_item = ChecklistItem.objects.filter(checklist=checklist)
    products = Product.objects.all()
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"



    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        status = request.POST.get('status')

        # Validate item_id and status
        if not item_id or not status:
            return HttpResponseForbidden("Invalid item ID or status.")

        checklist_item = get_object_or_404(ChecklistItem, id=item_id, checklist=checklist)
        checklist_item.status = status
        checklist_item.save()

        # Redirect to the same page or another page
        return redirect('checklistvoir-detail', checklist_id=checklist_id)

    # Prepare checklist items to be displayed with their statuses
    items = ChecklistItem.objects.filter(checklist=checklist)



    context = {
       'checklist': checklist,
       'checklist_item': checklist_item,
       'products': products,
       'items': items,
       'encours':encours,
       'valide':valide,
       'refuse':refuse,

    }
    return render(request, 'listings/checklistevoir_detail.html', context)

def product_detail(request, item_id):
    item = get_object_or_404(ItemInv, pk=item_id)

    context = {
        'item': item,
    }
    return render(request, 'listings/product_detail.html', context)

def inventory(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'listings/inventory.html', context)

def add_to_checklist(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_to_modify = int(request.POST.get('quantity', 0))
        action = request.POST.get('action')  # 'add' or 'subtract' action

        product = get_object_or_404(Product, pk=product_id)

        if action == 'add' and quantity_to_modify > 0:
            # Add quantity to ChecklistItem and subtract from inventory
            checklist_item, created = ChecklistItem.objects.get_or_create(checklist=checklist, product=product)
            checklist_item.quantity += quantity_to_modify
            checklist_item.save()

            product.quantity -= quantity_to_modify
            product.save()

        elif action == 'subtract' and quantity_to_modify > 0:
            # Subtract quantity from ChecklistItem and add back to inventory
            try:
                checklist_item = ChecklistItem.objects.get(checklist=checklist, product=product)
                if checklist_item.quantity >= quantity_to_modify:
                    checklist_item.quantity -= quantity_to_modify
                    checklist_item.save()

                    product.quantity += quantity_to_modify
                    product.save()
                else:
                    # Handle insufficient quantity in checklist item
                    pass
            except ChecklistItem.DoesNotExist:
                # Handle case where ChecklistItem does not exist
                pass


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def subtract_to_checklist(request, checklist_id):

    checklist_item = get_object_or_404(Checklist, pk=checklist_id)
    item = checklist_item.item
    quantity_to_subtract = checklist_item.quantity_checked

    # Ensure there are enough items in inventory to subtract
    if item.quantity >= quantity_to_subtract:
        # Update item quantity in inventory
        item.quantity -= quantity_to_subtract
        item.save()

        # Delete checklist item after subtracting
        checklist_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checklist_detail(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    checklist_items = ChecklistItem.objects.filter(checklist=checklist)
    products = Product.objects.all()
    query = request.GET.get('query')
    equipementdebase = "ÉQUIPEMENT DE BASE"
    jetable = "JETABLE"
    accessoirededecor = "ACCESSOIRES DE DÉCOR"
    equipementdebar = "ÉQUIPEMENT DE BAR"
    equipementpourservicecafe = "ÉQUIPEMENT POUR SERVICE CAFÉ"
    itemsdivers = "ITEMS DIVERS"
    tableetlinge = "TABLE ET LINGE DE TABLE"
    verrerie = "VERRERIE"
    porcelaine = "PORCELAINE ET COUTELLERIE"
    montage = "ÉQUIPEMENT POUR MONTAGE CANAPÉS"
    cuisson = "ÉQUIPEMENT DE CUISSON"
    service = "USTENSILES DE SERVICE"
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"





    if query:
        products = products.filter(name__icontains=query)

    formbis = ChecklistForm(request.POST or None, instance=checklist)
    if formbis.is_valid():
       formbis.save()
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'encours':encours,
        'valide': valide,
        'refuse': refuse,
        'checklist': checklist,
        'checklist_items': checklist_items,
        'products': products,
        'form': SearchFormInv(),
        'query': query,
        'formbis': formbis,
        'equipementdebase':equipementdebase,
        'jetable':jetable,
        'accessoirededecor':accessoirededecor,
        'equipementdebar':equipementdebar,
        'equipementpourservicecafe':equipementpourservicecafe,
        'itemsdivers':itemsdivers,
        'tableetlinge':tableetlinge,
        'verrerie':verrerie,
        'porcelaine':porcelaine,
        'montage':montage,
        'cuisson':cuisson,
        'service':service,

    }
    return render(request, 'listings/checklist_detail.html', context)

def creerchecklist(request):
    checklists = Checklist.objects.all().order_by('date')
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"


    if request.method == 'GET' and 'date' in request.GET:
        form = DateFilterForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            checklists = checklists.filter(date=date)
    else:
        form = DateFilterForm()

    if request.method == 'POST':
        form2 = ChecklistForm(request.POST)
        if form2.is_valid():
            form2.save()
        return redirect('creerchecklist')

    paginator = Paginator(checklists, 10)  # Show 10 events per page

    page = request.GET.get('page')
    try:
        checklists = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        checklists = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        checklists = paginator.page(paginator.num_pages)


    context = {
       'checklists': checklists,
       'form': form,
       'form2': ChecklistForm(),
       'encours': encours,
       'valide': valide,
       'refuse': refuse,

    }
    return render(request, 'listings/checklistcreate.html', context)

def edit_item(request, pk):
    item = get_object_or_404(ItemInv, pk=pk)
    if request.method == 'POST':
        form = ItemInvForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventaire')
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is not valid.'}, status=400)
    else:
        form = ItemInvForm(instance=item)
    return render(request, 'listings/edit_item.html', {'form': form, 'item':item})

def import_items(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        temp_file = NamedTemporaryFile(delete=True, suffix='.xlsx')

        # Write the uploaded file to a temporary file
        for chunk in myfile.chunks():
            temp_file.write(chunk)
        temp_file.flush()

        # Load the Excel workbook
        wb = load_workbook(temp_file.name)
        ws = wb.active

        # Process each row in the Excel sheet
        for row in ws.iter_rows(min_row=2, values_only=True):
            name = row[0]
            description = row[1]
            quantity = row[2]
            photo_url = row[3]  # Assuming the photo URL is in the fourth column

            item = ItemInv(name=name, description=description, quantity=quantity)

            # Download the photo and save it as ImageField
            if photo_url:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(photo_url).read())
                img_temp.flush()
                item.photo.save(f'{name}.jpg', File(img_temp))

            item.save()

        messages.success(request, 'Les données ont été importées avec succès.')
        temp_file.close()
    else:
        messages.error(request, 'Veuillez fournir un fichier.')

    return render(request, 'listings/import.html')


def tacheslist(request):

    today = now().date()
    tachestoday = Tacheafaire.objects.filter(date = today)
    tachesok = Tacheafaire.objects.filter(status=True)
    tachesko = Tacheafaire.objects.filter(status=False)
    taches = Tacheafaire.objects.all()



    context = {
        'tachestoday':tachestoday,
        'tachesok':tachesok,
        'tachesko':tachesko,
        'taches':taches,
                }
    return render(request, 'listings/tacheslist.html', context)
def inventory_list(request):
    items = ItemInv.objects.all()
    query = request.GET.get('query')

    if query:
        items = items.filter(name__icontains=query)

    context = {
        'items': items,
        'query': query,
        'form': SearchFormInv()
    }
    return render(request, 'listings/inventory_list.html', context)

@csrf_exempt
def save_positions(request):
    if request.method == 'POST':
        positions = json.loads(request.POST['positions'])
        for position, livraison_id in enumerate(positions):
            Livraison.objects.filter(id=livraison_id).update(position=position)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def home(request):
    livraisons  = Livraison.objects.all()
    livreurs = Livreur.objects.all()
    return render(request, 'listings/home.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs})

def livraisons_list(request):

    livraisons  = Livraison.objects.all()
    livreurs = Livreur.objects.all()
    journees = Journee.objects.all()
    return render(request, 'listings/livraisons_list.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journees' : journees})
def responsable_list(request):
    today = now().date()
    livraisons  = Livraison.objects.order_by('position').filter(date = today)
    livraisonsok  = Livraison.objects.filter(date = today, recuperation=False)
    livraisonsrecup  = Livraison.objects.filter(date = today, recuperation=True)
    journees = Journee.objects.all().order_by('-date')


    if request.method == 'GET' and 'date' in request.GET:
        form = DateFilterForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            journees = journees.filter(date=date)
    else:
        form = DateFilterForm()

    paginator = Paginator(journees, 7)  # Show 10 events per page

    page = request.GET.get('page')
    try:
        journees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        journees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        journees = paginator.page(paginator.num_pages)

    livreurs = Livreur.objects.all()

    ventes = "Ventes"
    cuisine = "Cuisine"
    return render(request, 'listings/responsableslist.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journees' : journees,
                                                              'ventes':ventes,
                                                              'today':today,
                                                              'livraisonsok':livraisonsok,
                                                              'livraisonsrecup':livraisonsrecup,
                                                              'cuisine':cuisine,
                                                              'form':form})

# View to handle Recupfrigo and its items
def create_recupfrigo(request):
    # Define the acceptable values for mode_envoi
    valid_modes_envoi = [
        "Porcelaine",
        "Chaud et porcelaine",
        "Porcelaine et bois",
        "Plateau de bois",
        "Froid et bois",
        "Chaud et jetable"
    ]

    # Get today's date
    today = date.today()

    # Filter livraisons by date and mode_envoi
    livraisons = Livraison.objects.filter(
        date_livraison=today,
        mode_envoi__in=valid_modes_envoi
    )
    print(livraisons)

    if request.method == 'POST':
        recupfrigo_form = RecupfrigoForm(request.POST)
        formset = RecupfrigoItemFormset(request.POST)

        if recupfrigo_form.is_valid() and formset.is_valid():
            # Save the recupfrigo
            recupfrigo = recupfrigo_form.save(commit=False)
            recupfrigo.save()

            # Save the formset
            items = formset.save(commit=False)
            for item in items:
                item.recupfrigo = recupfrigo  # Set the Recupfrigo for each item
                item.save()

            return redirect(reverse('create_recupfrigo'))

    else:
        recupfrigo_form = RecupfrigoForm()
        formset = RecupfrigoItemFormset()

    return render(request, 'listings/create_recupfrigo.html', {
        'recupfrigo_form': recupfrigo_form,
        'formset': formset,
        'livraisons': livraisons
    })
# View to handle Recuplivreur and its items
def create_recuplivreur(request, livraison_id):
    # Fetch the Livraison instance
    livraison = get_object_or_404(Livraison, id=livraison_id)
    
    if request.method == 'POST':
        recuplivreur_form = RecuplivreurForm(request.POST)
        formset = RecuplivreurItemFormset(request.POST)

        if recuplivreur_form.is_valid() and formset.is_valid():
            # Create the recuplivreur object but don't save to DB yet
            recuplivreur = recuplivreur_form.save(commit=False)

            # Ensure that livraison and date are set properly
            recuplivreur.livraison = livraison
            recuplivreur.date = livraison.date_livraison - timedelta(days=1) # Set the date from livraison
            recuplivreur.filled_by = request.user  # Track the user
            recuplivreur.filled_at = timezone.now()  # Track the timestamp
            
            # Now save the recuplivreur object to the database
            recuplivreur.save()

            # Save the formset with recuplivreur linked
            items = formset.save(commit=False)
            for item in items:
                item.recuplivreur = recuplivreur  # Set the recuplivreur for each item
                item.save()
            
            # Redirect after successful save
            return redirect(reverse('create_recuplivreur', args=[livraison_id]))

    else:
        recuplivreur_form = RecuplivreurForm()
        formset = RecuplivreurItemFormset()

    return render(request, 'listings/create_recuplivreur.html', {
        'recuplivreur_form': recuplivreur_form,
        'formset': formset,
        'livraison': livraison
    })


def journeerecupdetail(request, id):
    journee = get_object_or_404(Journee, id=id)
    recupfrigo = Recupfrigo.objects.filter(date=journee.date)
    recuplivreur = Recuplivreur.objects.filter(date=journee.date)

    # Build a comparison dictionary by item name
    comparison_data = []
    frigo_dict = {}
    livreur_dict = {}

    # Group RecupFrigo items by name
    for frigo in recupfrigo:
        for item in frigo.items_frigo.all():
            if item.item_name not in frigo_dict:
                frigo_dict[item.item_name] = []
            frigo_dict[item.item_name].append({
                'livraison_nom': frigo.livraison.nom,
                'frigo_quantity': item.quantity,
                'frigo_filled_by': frigo.filled_by,   # User who filled the form
                'frigo_filled_at': frigo.filled_at    # Timestamp when form was filled
            })

    # Group RecupLivreur items by name
    for livreur in recuplivreur:
        for item in livreur.items_livreur.all():
            if item.item_name not in livreur_dict:
                livreur_dict[item.item_name] = []
            livreur_dict[item.item_name].append({
                'livraison_nom': livreur.livraison.nom,
                'livreur_quantity': item.quantity,
                'livreur_filled_by': livreur.filled_by,   # User who filled the form
                'livreur_filled_at': livreur.filled_at,    # Timestamp when form was filled
                'livreur_nom': livreur.filled_by.username  # Access the username
            })

    # Build a comparison list
    all_items = set(list(frigo_dict.keys()) + list(livreur_dict.keys()))
    for item_name in all_items:
        livraisons = []
        frigo_data = frigo_dict.get(item_name, [])
        livreur_data = livreur_dict.get(item_name, [])

        # Combine livraisons by name for comparison
        livraison_names = set([data['livraison_nom'] for data in frigo_data] + [data['livraison_nom'] for data in livreur_data])
        for livraison_name in livraison_names:
            frigo_quantity = next((data['frigo_quantity'] for data in frigo_data if data['livraison_nom'] == livraison_name), 0)
            livreur_quantity = next((data['livreur_quantity'] for data in livreur_data if data['livraison_nom'] == livraison_name), 0)
            difference = livreur_quantity - frigo_quantity

            # Get user and timestamp info for each livraison
            frigo_filled_by = next((data['frigo_filled_by'] for data in frigo_data if data['livraison_nom'] == livraison_name), None)
            livreur_filled_by = next((data['livreur_filled_by'] for data in livreur_data if data['livraison_nom'] == livraison_name), None)
            frigo_filled_at = next((data['frigo_filled_at'] for data in frigo_data if data['livraison_nom'] == livraison_name), None)
            livreur_filled_at = next((data['livreur_filled_at'] for data in livreur_data if data['livraison_nom'] == livraison_name), None)
            livreur_nom = next((data['livreur_nom'] for data in livreur_data if data['livraison_nom'] == livraison_name), None)

            livraisons.append({
                'nom': livraison_name,
                'frigo_quantity': frigo_quantity,
                'livreur_quantity': livreur_quantity,
                'difference': difference,
                'frigo_filled_by': frigo_filled_by.username if frigo_filled_by else 'N/A',
                'livreur_filled_by': livreur_filled_by.username if livreur_filled_by else 'N/A',
                'frigo_filled_at': frigo_filled_at,
                'livreur_filled_at': livreur_filled_at,
                'livreur_nom': livreur_nom,
            })

        comparison_data.append({
            'item_name': item_name,
            'frigo_quantity': sum([data['frigo_quantity'] for data in frigo_data]),
            'livreur_quantity': sum([data['livreur_quantity'] for data in livreur_data]),
            'quantity_difference': sum([data['difference'] for data in livraisons]),
            'livraisons': livraisons,  # Include livraisons for dropdown
            'mismatch': any(data['difference'] != 0 for data in livraisons)
        })

    context = {
        'journee': journee,
        'comparison_data': comparison_data,
    }

    return render(request, 'listings/journeerecupdetail.html', context)



def journeedetailvente(request, id):
   journees = Journee.objects.get(id=id)
   livreurs = Livreur.objects.all()
   livraisonsroute  = Livraison.objects.order_by('position')
   today = now().date()
   livraisons = Livraison.objects.order_by('position')
   livraisonsok = Livraison.objects.filter(recuperation=False,date=journees.date)
   recuperations = Livraison.objects.filter(recuperation=True, date=journees.date)
   recuperationes = Livraison.objects.filter(recuperation = True, date=journees.date)
   retourtraiteur = "oui"
   retourtraiteurno = "non"
   recuperation = "oui"
   recuperationo = "non"
   rien = "."
   return render(request, 'listings/journeedetailvente.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journees' : journees,
                                                              'today':today,
                                                              'livraisonsok':livraisonsok,
                                                              'livraisonsroute':livraisonsroute,
                                                              'journees':journees,
                                                              'recuperations':recuperations,
                                                              'recuperationes':recuperationes,
                                                              'recuperation':recuperation,
                                                              'recuperationo':recuperationo,

                                                              })
def journees_list(request):
    today = now().date()
    livraisons  = Livraison.objects.order_by('position').filter(date = today)
    livraisonsok  = Livraison.objects.filter(date = today, recuperation=False)
    livraisonsrecup  = Livraison.objects.filter(date = today, recuperation=True)
    journees = Journee.objects.all().order_by('-date')
    max = "Maxime"
    loic = "Loic"
    jef = "Jef"


    if request.method == 'GET' and 'date' in request.GET:
        form = DateFilterForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            journees = journees.filter(date=date)
    else:
        form = DateFilterForm()

    paginator = Paginator(journees, 7)  # Show 10 events per page

    page = request.GET.get('page')
    try:
        journees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        journees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        journees = paginator.page(paginator.num_pages)

    livreurs = Livreur.objects.all()

    ventes = "Ventes"
    cuisine = "Cuisine"
    return render(request, 'listings/journees_list.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journees' : journees,
                                                              'ventes':ventes,
                                                              'today':today,
                                                              'livraisonsok':livraisonsok,
                                                              'livraisonsrecup':livraisonsrecup,
                                                              'cuisine':cuisine,
                                                              'form':form,
                                                              'max':max,
                                                              'jef':jef,
                                                              'loic':loic})

# RecupFrigo detail view
def recupfrigo_detail(request, id):
    recupfrigo = Recupfrigo.objects.get(id=id)
    items = recupfrigo.itemsfrigo.all()
    
    return render(request, 'listings/recupfrigo_detail.html', {
        'recupfrigo': recupfrigo,
        'items': items,
    })


# Recuplivreur detail view
def recuplivreur_detail(request, id):
    recuplivreur = Recuplivreur.objects.get(id=id)
    items = recuplivreur.items.all()
    
    return render(request, 'listings/recuplivreur_detail.html', {
        'recuplivreur': recuplivreur,
        'items': items,
    })



def recupslist(request):
    if request.user.is_authenticated:
        today = now().date()
        journees = Journee.objects.all().order_by('-date')
        
        
        # Initialize the form first
        form = DateFilterForm(request.GET or None)
        
        # Process the form if it's a GET request and has a 'date' field
        if request.method == 'GET' and 'date' in request.GET:
            if form.is_valid():
                date = form.cleaned_data['date']
                journees = journees.filter(date=date)

        paginator = Paginator(journees, 7)  # Show 7 items per page
        page = request.GET.get('page')
        
        try:
            journees = paginator.page(page)
        except PageNotAnInteger:
            journees = paginator.page(1)  # Deliver first page if page is not an integer
        except EmptyPage:
            journees = paginator.page(paginator.num_pages)  # Deliver last page if out of range

        return render(request, 'listings/recups-list.html', context={
            'journees': journees,
            'form': form,
            'today':today,
        })
    else:
        return redirect('home')

def routedetail(request, id):  # notez le paramètre id supplémentaire
   
   route = Route.objects.get(id=id)
   today = datetime.now().date()
   tomorrow = today + timedelta(1)
   livraison = Livraison.objects.filter(date = tomorrow)
   form = RoutedetailForm(request.POST or None, instance = route)
   if form.is_valid():
       form.save()
       return redirect('my_map_view')

   return render(request,
          'listings/routedetail.html',
          context={'route': route, 'form': form, 'livraison':livraison}) # nous passons l'id au modèle

def journee_detail(request, id):  # notez le paramètre id supplémentaire
    journees = Journee.objects.get(id=id)
    livreurs = Livreur.objects.all()
    livraisonsroute = Livraison.objects.order_by('position')
    today = now().date()

    livraisonss = Livraison.objects.order_by('position').select_related('statut', 'statut__livreur').filter(date=journees.date)  # Use select_related to include related data

    # Convert to JSON-like structure with error handling for 'livreur'
    livraisons_data = [
        {
            'id': livraison.id,
            'nom': livraison.nom,
            'infodetail': livraison.infodetail,
            'heure_livraison': livraison.heure_livraison,
            'livreur': livraison.statut.livreur.nom if livraison.statut.livreur else "Aucun livreur",  # Check if livreur exists
            'heure_depart': livraison.statut.heure_depart if livraison.statut else "Non défini",
            'recuperation': livraison.recuperation,
        }
        for livraison in livraisonss
    ]

    livraisons_json = json.dumps(livraisons_data)
    livraisonsok = Livraison.objects.filter(recuperation=False, date=journees.date)
    recuperations = Livraison.objects.filter(recuperation=True, date=journees.date)
    recuperationes = Livraison.objects.filter(recuperation=True, date=journees.date)

    retourtraiteur = "oui"
    retourtraiteurno = "non"
    recuperation = "oui"
    recuperationo = "non"
    loic = "Loic"
    maxime = "Maxime"
    rien = "."

    return render(request,
                  'listings/journee_detail.html',
                  context={
                      'journees': journees,
                      'livraisonsroute': livraisonsroute,
                      'livreurs': livreurs,
                      'recuperations': recuperations,
                      'retourtraiteur': retourtraiteur,
                      'recuperation': recuperation,
                      'retourtraiteurno': retourtraiteurno,
                      'livraisonss': livraisons_json,
                      'recuperationo': recuperationo,
                      'loic': loic,
                      'maxime': maxime,
                      'rien': rien,
                      'recuperations': recuperation,
                      'livraisons_data': livraisons_data,
                      'livraisonsok': livraisonsok,
                      'recuperationes': recuperationes,
                      'today': today,
                  })  # nous passons l'id au modèle



def livreur_list(request):
    if request.user.is_authenticated:
        livreurs = Livreur.objects.exclude(user=request.user)
        return render(request, 'listings/livreur_list.html', context={'livreurs': livreurs
                                                                      })
    else:
        return redirect('home')


def livreur_detail(request, pk):  # notez le paramètre id supplémentaire
    if request.user.is_authenticated :
        livreur = Livreur.objects.get(user_id= pk)
        livraisons  = Livraison.objects.all()
        taches = Tacheafaire.objects.all()
        recuperations = Recuperation.objects.all()
        journee = Journee.objects.all()
        return render(request, "listings/livreur_detail.html", context={'livreur':livreur,
                                                                'livraisons' : livraisons,
                                                                'taches' : taches,
                                                                'recuperations' : recuperations,
                                                                'journee' : journee})
    else:
        return redirect('home')
def taskdetail(request, id):
    task = get_object_or_404(Tacheafaire, id=id)  # Get the task instance
    photoss = task.photo

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        formbis = PhotoTachesFormSet(request.POST, request.FILES, queryset=Phototaches.objects.filter(tache=task))
        
        if form.is_valid():
            # Save the task instance first
            task = form.save()

        if formbis.is_valid():
            # Process and save the associated photos
            photos = formbis.save(commit=False)
            for photo in photos:
                photo.tache = task  # Associate each photo with the task
                photo.save()

            # If there are many-to-many fields, save them as well
            formbis.save_m2m()

            return redirect(request.META.get('HTTP_REFERER', 'task_list'))  # Redirect after save
        

    else:
        form = TaskUpdateForm(instance=task)
        formbis = PhotoTachesFormSet(queryset=Phototaches.objects.filter(tache=task))  # Initialize formset with existing photos for the task

    return render(request, 'listings/taskdetail.html', {'task': task, 'form': form, 'formbis': formbis, 'photoss':photoss,})


def dashboard(request, pk, id):  # notez le paramètre id supplémentaire
    if request.user.is_authenticated :
        journee = Journee.objects.get(id=id)
        livreur = Livreur.objects.get(user_id= pk)
        key = settings.GOOGLE_API_KEY
        userid = livreur.id
        today = now().date()
        livraisonss  = Livraison.objects.filter( statut__livreur = userid, date = journee.date)
        livraisons  = Livraison.objects.order_by('position').filter( statut__livreur = userid, date = journee.date)

        livraisonstatusok = Livraison.objects.filter(status=True, recuperation=False, statut__livreur = userid, date = journee.date)
        livraisonstatusko = Livraison.objects.filter(status=False, recuperation=False, statut__livreur = userid, date = journee.date)
        recuperation = Livraison.objects.filter(recuperation=True,  statut__livreur = userid, date = journee.date)
        recuperationok = Livraison.objects.filter(recuperation=True, status=True,  statut__livreur = userid, date = journee.date)
        recuperationko = Livraison.objects.filter(status=False,recuperation=True, statut__livreur = userid, date = journee.date)
        livraison = Livraison.objects.filter(recuperation=False, statut__livreur = userid, date = journee.date)
        tacheok = Tacheafaire.objects.filter(livreur = userid, status=True, date = today )
        tacheko =  Tacheafaire.objects.filter(livreur = userid, status=False, date = today)
        recuperation = "oui"
        recuperationo = "non"
        retourtraiteur = "oui"
        taches = Tacheafaire.objects.filter(livreur = userid)
        routes = Livraison.objects.order_by('position')
        routess = Route.objects.filter(date = journee.date, livreur_id = livreur)
        routes_with_livraisons = []
        for route in routess:
            ordered_livraisons = route.livraisons.all().order_by('position')
            routes_with_livraisons.append({
                'route': route,
                'livraisons': ordered_livraisons,
                'nom': route.nom,
                'heure_depart': route.heure_depart,

            })

        livraisons_data = [
        {
            'address': livraison.adress,
            'latitude': float(livraison.lat),
            'longitude': float(livraison.lng),
            'nom': livraison.nom,
            'mode_envoi': livraison.mode_envoi,
            'convive': livraison.convives,
            'heure_livraison': livraison.heure_livraison,
        }
        for livraison in livraisonss
        
    ]
        


        return render(request, "listings/dashboard.html", context={'livreur':livreur,
                                                                   'livraisons':livraisons,
                                                                'livraisonss' : livraisons_data,
                                                                'livraisonstatusok':livraisonstatusok,
                                                                'livraisonstatusko':livraisonstatusko,
                                                                'recuperation' : recuperation,
                                                                'journee' : journee,
                                                                'recuperationok':recuperationok,
                                                                'recuperationko':recuperationko,
                                                                'livraison':livraison,
                                                                'recuperation':recuperation,
                                                                'key':key,
                                                                'userid':userid,
                                                                'recuperationo':recuperationo,
                                                                'retourtraiteur':retourtraiteur,
                                                                'routes':routes,
                                                                'today':today,
                                                                'routess':routess,
                                                                'routes_with_livraisons': routes_with_livraisons,
                                                                'taches':taches,
                                                                'tacheok':tacheok,
                                                                'tacheko':tacheko,

                                                                })
    else:
        return redirect('home')
def update_task(request, pk):

    task = get_object_or_404(Tacheafaire, pk=pk)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            # Update the task status
            task.status = form.cleaned_data['status']
            task.save()


    return render(request, 'listings/update_task.html', {'task': task})

def update_photo_task(request, pk):
    task = get_object_or_404(Tacheafaire, pk=pk)

    if request.method == 'POST':
       photo_formset = PhotoTachesFormSet(request.POST, request.FILES)
       if photo_formset.is_valid():
        photos = photo_formset.save(commit=False)
        for photo in photos:
                photo.task = task  # Set the related Livraison for each photo
                photo.save()
    else:
        form = PhotoTachesForm()

    return render(request, 'listings/update_photo_task.html', {'form': form, 'task': task})



def responsableschoixjournee(request):

    if request.method == 'POST':
        livraison_resource = LivraisonResource()
        dataset = Dataset()
        new_livraisons = request.FILES['livraisons_file']
        imported_data = dataset.load(new_livraisons.read(), format='xlsx')
        for data in imported_data:
            value = Livraison(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
                data[13],
                data[14],
                data[15],
                data[16],
            )
            value .save()

    livraisons  = Livraison.objects.all()
    livreurs = Livreur.objects.all()
    journees = Journee.objects.all()
    return render(request, 'listings/responsableschoixjournee.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journees' : journees})

def responsables(request, id):
    today = datetime.now().date()
    journee = Journee.objects.get(id=id)
    tomorrow = today + timedelta(1)
    livraisons  = Livraison.objects.order_by('position')
    livraisonstatusok = Livraison.objects.filter(status=True,recuperation=False, date=journee.date)
    livraisonstatusko = Livraison.objects.filter(status=False,recuperation=False, date=journee.date)
    recuperation = Livraison.objects.filter(recuperation=True, date=journee.date)
    recuperationok = Livraison.objects.filter(recuperation=True, status=True, date=journee.date)
    recuperationko = Livraison.objects.filter(status=False,recuperation=True, date=journee.date)
    livraison = Livraison.objects.filter(recuperation=False, date=journee.date)
    livreurs = Livreur.objects.all()

    recuperations = "oui"
    return render(request, 'listings/responsables.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journee' : journee,
                                                              'recuperations' : recuperations,
                                                              'livraisonstatusok':livraisonstatusok,
                                                              'livraisonstatusko':livraisonstatusko,
                                                              'livraison':livraison,
                                                              'recuperationok':recuperationok,
                                                              'recuperationko':recuperationko,
                                                              'recuperation' : recuperation,
                                                              })



class DistanceView(View):

    def get(self, request):
        form = DistanceForm
        distances = Distances.objects.all()
        context={'form': form,
                 'distances':distances,
                                                                    }
        return render(request, 'listings/distances.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        return redirect('my_distance_view')

@csrf_exempt
def update_livraison(request):
    if request.method == 'POST':
        livraison_id = request.POST.get('livraison_id')
        new_route_id = request.POST.get('new_route_id')

        try:
            livraison = Livraison.objects.get(id=livraison_id)
            new_route = Route.objects.get(id=new_route_id)

            # Update route and possibly other fields
            livraison.statut = new_route

            # Optionally update journee if needed
            livraison.journee = new_route.journee  # Assuming you want to update journee based on the new route

            livraison.save()

            return JsonResponse({'success': True})
        except Livraison.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Livraison not found'})
        except Route.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Route not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def update_status(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        task_id = request.POST.get('livraison_id')
        new_status = request.POST.get('new_statut_id')
        task = Livraison.objects.get(id=task_id)
        task.statut_id = new_status
        task.save()
        return JsonResponse({'message': 'Route mise à jour'})
    else:
        return JsonResponse({'message': 'Echec'})

class MapView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        matin = ['05h00', '05h15', '05h30', '05h45', '06h00', '06h15', '06h30', '06h45', '07h00', '07h15', '07h30', '07h45', '08h00','08h15', '08h30', '08h45', '09h00', '09h15', '09h30', '09h45', 'recup']
        distances = Distances.objects.all()
        todo_livraison = Livraison.objects.filter(date=tomorrow, heure_livraison__in = matin, place_id__isnull=False, statut__id= 21)
        route1 = Livraison.objects.filter(date=tomorrow, heure_livraison__in = matin)
        route2 = Livraison.objects.filter(statut__id= 2, date=tomorrow, heure_livraison__in = matin)
        route3 = Livraison.objects.filter(statut__id= 3, date=tomorrow, heure_livraison__in = matin)
        route4 = Livraison.objects.filter(statut__id= 4, date=tomorrow, heure_livraison__in = matin)
        routesmatin = ['1','2','3','4','5','6']
        routes21 = Route.objects.filter(id=21)
        routes = Route.objects.filter(date=tomorrow, nom__in=routesmatin)
        eligable_locations = Livraison.objects.order_by('position').filter(place_id__isnull=False, heure_livraison__in = matin, date=tomorrow)
        livraisons =[]

        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'adress' : a.adress,
                'convives': a.convives,
                'mode_envoi': a.mode_envoi,
                'infodetail': a.infodetail,

            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'routes':routes,
                   'routesmatin':routesmatin,
                   'route1':route1,
                   'route2':route2,
                   'route3':route3,
                   'route4':route4,
                   'todo_livraison':todo_livraison,
                   'routes21':routes21,
                   'tomorrow':tomorrow,

        }
        return render(request, 'listings/map.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        return redirect('my_map_view')
class MapApremView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        distances = Distances.objects.all()
        aprem = ['13h00', '13h15', '13h30', '13h45', '14h00', '14h15', '14h30', '14h45', '15h00', '15h15', '15h30', '15h45', '16h00', '16h15', '16h30', '16h45', '17h00', '17h15', '17h30', '17h45', '18h00', '18h15', '18h30', '18h45', '19h00', 'recup']
        todo_livraison = Livraison.objects.filter(statut=21, date=tomorrow, heure_livraison__in = aprem, place_id__isnull=False)
        routesaprem = ['6','7','8','9','10','11','12','13','14','15','16','17', '18','19','20']
        routes = Route.objects.filter(date=tomorrow, nom__in=routesaprem)
        route1 = Livraison.objects.filter(date=tomorrow, heure_livraison__in = aprem)
        route7 = Livraison.objects.filter(statut='7', date=tomorrow, heure_livraison__in = aprem)
        route8 = Livraison.objects.filter(date=tomorrow, heure_livraison__in = aprem)
        route9 = Livraison.objects.filter(statut='9', date=tomorrow, heure_livraison__in = aprem)
        route10 = Livraison.objects.filter(statut='27', date=tomorrow, heure_livraison__in = aprem)
        route11 = Livraison.objects.filter(statut='11', date=tomorrow, heure_livraison__in = aprem)
        route12 = Livraison.objects.filter(statut='12', date=tomorrow, heure_livraison__in = aprem)
        route13 = Livraison.objects.filter(statut='13', date=tomorrow, heure_livraison__in = aprem)
        route14 = Livraison.objects.filter(statut='14', date=tomorrow, heure_livraison__in = aprem)
        route15 = Livraison.objects.filter(statut='15', date=tomorrow, heure_livraison__in = aprem)
        route16 = Livraison.objects.filter(statut='16', date=tomorrow, heure_livraison__in = aprem)
        route17 = Livraison.objects.filter(statut='17', date=tomorrow, heure_livraison__in = aprem)
        route18 = Livraison.objects.filter(statut='18', date=tomorrow, heure_livraison__in = aprem)
        route19 = Livraison.objects.filter(statut='19', date=tomorrow, heure_livraison__in = aprem)
        route20 = Livraison.objects.filter(statut='20', date=tomorrow, heure_livraison__in = aprem)
        routes21 = Route.objects.filter(id=21)
        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = aprem, date=tomorrow )
        livraisons =[]
        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'adress' : a.adress,
                'convives': a.convives,
                'mode_envoi': a.mode_envoi,
                'infodetail': a.infodetail
            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'route1':route1,
                   'route8':route8,
                   'route9':route9,
                   'route10':route10,
                   'route11':route11,
                   'route12':route12,
                   'route13':route13,
                   'route14':route14,
                   'route15':route15,
                   'route16':route16,
                   'route17':route17,
                   'route18':route18,
                   'route19':route19,
                   'route20':route20,
                   'routes':routes,
                   'todo_livraison':todo_livraison,
                   'routes21': routes21,


        }
        return render(request, 'listings/mapaprem.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        return redirect('my_mapaprem_view')
class MapMidiView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        distances = Distances.objects.all()
        midi = ['10h00', '10h15', '10h30', '10h45', '11h00', '11h15', '11h30', '11h45', '12h00', '12h15', '12h30', '12h45', 'recup']
        todo_livraison = Livraison.objects.filter(statut=21, date=tomorrow, heure_livraison__in = midi, place_id__isnull=False)
        routesmidi = ['2','3','4','5','6','7','8','9','10','11','12']
        routes21 = Route.objects.filter(id=21)
        routes = Route.objects.filter(date=tomorrow, nom__in=routesmidi)
        route1 = Livraison.objects.filter(date=tomorrow, heure_livraison__in=midi)
        route2 = Livraison.objects.filter(date=tomorrow, heure_livraison__in = midi)
        route3 = Livraison.objects.filter(statut='3', date=tomorrow, heure_livraison__in = midi)
        route4 = Livraison.objects.filter(statut='4', date=tomorrow, heure_livraison__in = midi)
        route5 = Livraison.objects.filter(statut='5', date=tomorrow, heure_livraison__in = midi)
        route6 = Livraison.objects.filter(statut='6', date=tomorrow, heure_livraison__in = midi)
        route7 = Livraison.objects.filter(statut='7', date=tomorrow, heure_livraison__in = midi)
        route8 = Livraison.objects.filter(statut='8', date=tomorrow, heure_livraison__in = midi)
        route9 = Livraison.objects.filter(statut='9', date=tomorrow, heure_livraison__in = midi)

        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = midi, date=tomorrow)
        livraisons =[]
        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'adress' : a.adress,
                'convives': a.convives,
                'mode_envoi': a.mode_envoi,
                'infodetail': a.infodetail
            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'route2':route2,
                   'route3':route3,
                   'route4':route4,
                   'route5':route5,
                   'route6':route6,
                   'route7':route7,
                   'route8':route8,
                   'route9':route9,
                   'todo_livraison':todo_livraison,
                   'route1':route1,
                   'routes': routes,
                   'routes21':routes21,

        }
        return render(request, 'listings/mapmidi.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        return redirect('my_mapmidi_view')

class MapApremTodayView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        tomorrow = today + timedelta(2)
        distances = Distances.objects.all()
        aprem = ['13h00', '13h15', '13h30', '13h45', '14h00', '14h15', '14h30', '14h45', '15h00', '15h15', '15h30', '15h45', '16h00', '16h15', '16h30', '16h45', '17h00', '17h15', '17h30', '17h45', '18h00', '18h15', '18h30', '18h45', '19h00', 'recup']
        todo_livraison = Livraison.objects.filter(statut=21, date=tomorrow, heure_livraison__in = aprem, place_id__isnull=False)
        routesaprem = ['6','7','8','9','10','11','12','13','14','15','16','17', '18','19','20']
        routes = Route.objects.filter(date=tomorrow, nom__in=routesaprem)
        route1 = Livraison.objects.filter(date=tomorrow, heure_livraison__in = aprem)
        route7 = Livraison.objects.filter(statut='7', date=tomorrow, heure_livraison__in = aprem)
        route8 = Livraison.objects.filter(date=tomorrow, heure_livraison__in = aprem)
        route9 = Livraison.objects.filter(statut='9', date=tomorrow, heure_livraison__in = aprem)
        route10 = Livraison.objects.filter(statut='27', date=tomorrow, heure_livraison__in = aprem)
        route11 = Livraison.objects.filter(statut='11', date=tomorrow, heure_livraison__in = aprem)
        route12 = Livraison.objects.filter(statut='12', date=tomorrow, heure_livraison__in = aprem)
        route13 = Livraison.objects.filter(statut='13', date=tomorrow, heure_livraison__in = aprem)
        route14 = Livraison.objects.filter(statut='14', date=tomorrow, heure_livraison__in = aprem)
        route15 = Livraison.objects.filter(statut='15', date=tomorrow, heure_livraison__in = aprem)
        route16 = Livraison.objects.filter(statut='16', date=tomorrow, heure_livraison__in = aprem)
        route17 = Livraison.objects.filter(statut='17', date=tomorrow, heure_livraison__in = aprem)
        route18 = Livraison.objects.filter(statut='18', date=tomorrow, heure_livraison__in = aprem)
        route19 = Livraison.objects.filter(statut='19', date=tomorrow, heure_livraison__in = aprem)
        route20 = Livraison.objects.filter(statut='20', date=tomorrow, heure_livraison__in = aprem)
        routes21 = Route.objects.filter(id=21)
        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = aprem, date=tomorrow )
        livraisons =[]
        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'adress' : a.adress,
                'convives': a.convives,
                'mode_envoi': a.mode_envoi,
                'infodetail': a.infodetail
            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'route1':route1,
                   'route8':route8,
                   'route9':route9,
                   'route10':route10,
                   'route11':route11,
                   'route12':route12,
                   'route13':route13,
                   'route14':route14,
                   'route15':route15,
                   'route16':route16,
                   'route17':route17,
                   'route18':route18,
                   'route19':route19,
                   'route20':route20,
                   'routes':routes,
                   'todo_livraison':todo_livraison,
                   'routes21': routes21,


        }
        return render(request, 'listings/maptodayaprem.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        return redirect('my_maptodayaprem_view')
class MapMidiTodayView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        aftertomorrow = today + timedelta(2)
        distances = Distances.objects.all()
        midi = ['10h00', '10h15', '10h30', '10h45', '11h00', '11h15', '11h30', '11h45', '12h00', '12h15', '12h30', '12h45', 'recup']
        todo_livraison = Livraison.objects.filter(date=aftertomorrow, heure_livraison__in = midi, place_id__isnull=False, statut__id= 21)
        routesmidi = ['2','3','4','5','6','7','8','9','10','11','12']
        routes21 = Route.objects.filter(id=21)
        routes = Route.objects.filter(nom__in=routesmidi, date=aftertomorrow)
        route1 = Livraison.objects.filter(date=aftertomorrow)
        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = midi, date=aftertomorrow )
        livraisons =[]
        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'convives' : a.convives,
                'mode_envoi' : a.mode_envoi,
            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'routes21':routes21,
                   'routes':routes,
                   'todo_livraison':todo_livraison,
                   'route1':route1,

        }
        return render(request, 'listings/maptodaymidi.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        
        return render(request, 'listings/maptodaymidi.html')  
class MapTodayView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        aftertomorrow = today + timedelta(2)
        distances = Distances.objects.all()
        matin = ['05h00', '05h15', '05h30', '05h45', '06h00', '06h15', '06h30', '06h45', '07h00', '07h15', '07h30', '07h45', '08h00','08h15', '08h30', '08h45', '09h00', '09h15', '09h30', '09h45', 'recup']
        todo_livraison = Livraison.objects.filter(date=aftertomorrow, heure_livraison__in = matin, place_id__isnull=False, statut__id= 21)
        routesmatin = ['1','2','3','4']
        routes21 = Route.objects.filter(id=21)
        routes = Route.objects.filter(nom__in=routesmatin, date=aftertomorrow)
        route1 = Livraison.objects.filter(date=aftertomorrow)
        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = matin, date=aftertomorrow )
        livraisons =[]
        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'convives' : a.convives,
                'mode_envoi' : a.mode_envoi,
            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'routes21':routes21,
                   'routes':routes,
                   'todo_livraison':todo_livraison,
                   'route1':route1,

        }
        return render(request, 'listings/maptoday.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        return redirect('my_maptoday_view')


class MapApremDimView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        tomorrow = today + timedelta(3)
        distances = Distances.objects.all()
        aprem = ['13h00', '13h15', '13h30', '13h45', '14h00', '14h15', '14h30', '14h45', '15h00', '15h15', '15h30', '15h45', '16h00', '16h15', '16h30', '16h45', '17h00', '17h15', '17h30', '17h45', '18h00', '18h15', '18h30', '18h45', '19h00', 'recup']
        todo_livraison = Livraison.objects.filter(statut=21, date=tomorrow, heure_livraison__in = aprem, place_id__isnull=False)
        routesaprem = ['6','7','8','9','10','11','12','13','14','15','16','17', '18','19','20']
        routes = Route.objects.filter(date=tomorrow, nom__in=routesaprem)
        route1 = Livraison.objects.filter(date=tomorrow, heure_livraison__in = aprem)
        route7 = Livraison.objects.filter(statut='7', date=tomorrow, heure_livraison__in = aprem)
        route8 = Livraison.objects.filter(date=tomorrow, heure_livraison__in = aprem)
        route9 = Livraison.objects.filter(statut='9', date=tomorrow, heure_livraison__in = aprem)
        route10 = Livraison.objects.filter(statut='27', date=tomorrow, heure_livraison__in = aprem)
        route11 = Livraison.objects.filter(statut='11', date=tomorrow, heure_livraison__in = aprem)
        route12 = Livraison.objects.filter(statut='12', date=tomorrow, heure_livraison__in = aprem)
        route13 = Livraison.objects.filter(statut='13', date=tomorrow, heure_livraison__in = aprem)
        route14 = Livraison.objects.filter(statut='14', date=tomorrow, heure_livraison__in = aprem)
        route15 = Livraison.objects.filter(statut='15', date=tomorrow, heure_livraison__in = aprem)
        route16 = Livraison.objects.filter(statut='16', date=tomorrow, heure_livraison__in = aprem)
        route17 = Livraison.objects.filter(statut='17', date=tomorrow, heure_livraison__in = aprem)
        route18 = Livraison.objects.filter(statut='18', date=tomorrow, heure_livraison__in = aprem)
        route19 = Livraison.objects.filter(statut='19', date=tomorrow, heure_livraison__in = aprem)
        route20 = Livraison.objects.filter(statut='20', date=tomorrow, heure_livraison__in = aprem)
        routes21 = Route.objects.filter(id=21)
        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = aprem, date=tomorrow )
        livraisons =[]
        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'adress' : a.adress,
                'convives': a.convives,
                'mode_envoi': a.mode_envoi,
                'infodetail': a.infodetail
            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'route1':route1,
                   'route8':route8,
                   'route9':route9,
                   'route10':route10,
                   'route11':route11,
                   'route12':route12,
                   'route13':route13,
                   'route14':route14,
                   'route15':route15,
                   'route16':route16,
                   'route17':route17,
                   'route18':route18,
                   'route19':route19,
                   'route20':route20,
                   'routes':routes,
                   'todo_livraison':todo_livraison,
                   'routes21': routes21,


        }
        return render(request, 'listings/mapdimaprem.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()
    
            return render(request, 'listings/mapdimaprem.html')
class MapMidiDimView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        aftertomorrow = today + timedelta(2)
        distances = Distances.objects.all()
        midi = ['10h00', '10h15', '10h30', '10h45', '11h00', '11h15', '11h30', '11h45', '12h00', '12h15', '12h30', '12h45', 'recup']
        todo_livraison = Livraison.objects.filter(date=aftertomorrow, heure_livraison__in = midi, place_id__isnull=False, statut__id= 21)
        routesmidi = ['2','3','4','5','6','7','8','9','10','11','12']
        routes21 = Route.objects.filter(id=21)
        routes = Route.objects.filter(nom__in=routesmidi, date=aftertomorrow)
        route1 = Livraison.objects.filter(date=aftertomorrow)
        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = midi, date=aftertomorrow )
        livraisons =[]
        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'convives' : a.convives,
                'mode_envoi' : a.mode_envoi,
            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'routes21':routes21,
                   'routes':routes,
                   'todo_livraison':todo_livraison,
                   'route1':route1,

        }
        return render(request, 'listings/mapdimmidi.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()


        
        return render(request, 'listings/mapdimmidi.html')
class MapDimView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        aftertomorrow = today + timedelta(3)
        distances = Distances.objects.all()
        matin = ['05h00', '05h15', '05h30', '05h45', '06h00', '06h15', '06h30', '06h45', '07h00', '07h15', '07h30', '07h45', '08h00','08h15', '08h30', '08h45', '09h00', '09h15', '09h30', '09h45', 'recup']
        todo_livraison = Livraison.objects.filter(date=aftertomorrow, heure_livraison__in = matin, place_id__isnull=False, statut__id= 21)
        routesmatin = ['1','2','3','4']
        routes21 = Route.objects.filter(id=21)
        routes = Route.objects.filter(nom__in=routesmatin, date=aftertomorrow)
        route1 = Livraison.objects.filter(date=aftertomorrow)
        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = matin, date=aftertomorrow )
        livraisons =[]
        for a in eligable_locations:
            data = {
                'lat': float(a.lat),
                'lng': float(a.lng),
                'place_id': a.place_id,
                'nom': a.nom,
                'heure_livraison': a.heure_livraison,
                'convives' : a.convives,
                'mode_envoi' : a.mode_envoi,
            }

            livraisons.append(data)

        context = {'key': key,
                   'livraisons':livraisons,
                   'form': form,
                   'distances':distances,
                   'routes21':routes21,
                   'routes':routes,
                   'todo_livraison':todo_livraison,
                   'route1':route1,

        }
        return render(request, 'listings/mapdim.html', context)

    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            from_location_info = Livraison.objects.get(nom=from_location)
            from_adress_string = str(from_location_info.adress)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Livraison.objects.get(nom=to_location)
            to_adress_string = str(to_location_info.adress)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            calculate = gmaps.distance_matrix(
                from_adress_string,
                to_adress_string,
                mode = mode,
                departure_time = now
            )
            print(calculate)

            duration_secons = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_secons/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters/1000

            if 'duration_in_traffic' in calculate['rows'][0]['elements'][0]:
                duration_in_traffic_seconds = calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None

            obj = Distances(
                from_location = Livraison.objects.get(nom=from_location),
                to_location = Livraison.objects.get(nom=to_location),
                mode = mode,
                distance_km = distance_km,
                distance_mins = duration_minutes,
                distance_traffic_mins = duration_in_traffic_minutes
            )

            obj.save()

        return redirect('my_mapdim_view')
def deleteDistance(request, pk):
    distance = Distances.objects.get(id= pk)
    if request.method == 'POST':
        distance.delete()
        return redirect('my_map_view')

    context = {'distance':distance,}
    return render(request, 'listings/deletedistance.html', context)

class GeocodeAllLivraisonsView(View):
    def get(self, request):
        # Get all livraisons that need geocoding (filter for those without lat/lng or place_id)
        livraisons = Livraison.objects.filter(lat__isnull=True, lng__isnull=True, place_id__isnull=True)

        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

        for livraison in livraisons:
            if livraison.adress and livraison.country and livraison.zipcode and livraison.city:
                # Construct the address string
                adress_string = f"{livraison.adress}, {livraison.zipcode}, {livraison.city}, {livraison.country}"

                # Geocode the address
                result = gmaps.geocode(adress_string)

                if result:
                    # Extract the lat, lng, and place_id
                    lat = result[0].get('geometry', {}).get('location', {}).get('lat', {})
                    lng = result[0].get('geometry', {}).get('location', {}).get('lng', {})
                    place_id = result[0].get('place_id', {})

                    # Update the Livraison instance
                    livraison.lat = lat
                    livraison.lng = lng
                    livraison.place_id = place_id
                    livraison.save()

        # Redirect to the livraisonstomorrow page
        return redirect('livraisonstomorrow')

class GeocodingTodayView(View):
    def get(self, request, pk):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        livraison = Livraison.objects.get(pk = pk)

        if livraison.lng and livraison.lat and livraison.place_id != None:

            lat = livraison.lat
            lng = livraison.lng
            place_id = livraison.place_id




        elif livraison.adress and livraison.country and livraison.zipcode and livraison.city != None:

            adress_string = str(livraison.adress)+", "+str(livraison.zipcode)+", "+str(livraison.city)+", "+str(livraison.country)

            gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
            result =  gmaps.geocode(adress_string)[0]

            lat = result.get('geometry', {}).get('location', {}).get('lat', {})
            lng = result.get('geometry', {}).get('location', {}).get('lng', {})
            place_id = result.get('place_id', {})



            livraison.lat = lat
            livraison.lng = lng
            livraison.place_id = place_id

            livraison.save()
            return redirect('livraisonstoday')

        else:

            result = ""
            lat = ""
            lng = ""
            place_id = ""

        context = {'livraison': livraison,
                   'lat':lat,
                   'lng':lng,
                   'place_id':place_id,

        }
        return render(request, 'listings/geocodingtoday.html', context)

def livraison_detail(request, ip):  # notez le paramètre id supplémentaire
   livraison = Livraison.objects.get(id=ip)
   adresse = Livraison.adress
   livreur = Livreur.objects.all()
   journee = Journee.objects.all()
   recuperation = "oui"
   loic = "Loic"
   maxime = "Maxime"

   if request.method == 'POST':
        form = LivraisonForm(request.POST or None, instance=livraison)
        formbis = PhotoFormSet(request.POST, request.FILES or None, instance=livraison)
        
        if form.is_valid():
            livraison = form.save()  # Save the Livraison instance
        if formbis.is_valid():
            # Save the associated photos
            photos = formbis.save(commit=False)
            for photo in photos:
                photo.livraison = livraison  # Set the related Livraison for each photo
                photo.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  # Redirect to a page showing deliveries (adjust this)

   else:
        form = LivraisonForm()
        formbis = PhotoFormSet()




   gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
   result = gmaps.geocode(adresse)

   return render(request,
          'listings/livraison_detail.html',
          context={'livraison': livraison, 'livreur':livreur, 'recuperation': recuperation, 'form': form, 'journee':journee, 'result':result,'adresse': adresse, 'loic': loic, 'maxime':maxime, 'formbis':formbis}) # nous passons l'id au modèle

def update_photo(request, pk):
    livraison = Livraison.objects.get(pk=pk)

    if request.method == 'POST':
       photo_formset = PhotoFormSet(request.POST, request.FILES)
       if photo_formset.is_valid():
        photos = photo_formset.save(commit=False)
        for photo in photos:
                photo.livraison = livraison  # Set the related Livraison for each photo
                photo.save()
    else:
        form = PhotoForm()

    return render(request, 'listings/update_photo.html', {'form': form, 'livraison': livraison})

def livraisonstomorrow(request):
    recuperation = "oui"
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    aftertomorrow = today + timedelta(2)
    afteraftertomorrow = today + timedelta(3)
    matin = ['05h00', '05h15', '05h30', '05h45', '06h00', '06h15', '06h30', '06h45', '07h00', '07h15', '07h30', '07h45', '08h00',
             '08h15', '08h30', '08h45', '09h00', '09h15', '09h30', '09h45', 'recup']
    midi = ['10h00', '10h15', '10h30', '10h45', '11h00', '11h15', '11h30', '11h45', '12h00', '12h15', '12h30', '12h45', 'recup']
    apresmidi = ['13h00', '13h15', '13h30', '13h45', '14h00', '14h15', '14h30', '14h45', '15h00', '15h15', '15h30', '15h45', '16h00', '16h15', '16h30', '16h45', '17h00', '17h15', '17h30', '17h45', '18h00', '18h15', '18h30', '18h45', '19h00', 'recup']
    livraisons = Livraison.objects.order_by('position')
    livraisonsok = Livraison.objects.filter(date=tomorrow, recuperation=False)
    livraisonrecup = Livraison.objects.filter(date=tomorrow, recuperation=True)
    livraisonsmatin =  Livraison.objects.order_by('position').filter(heure_livraison__in= matin, date =tomorrow)
    livraisonsmidi =  Livraison.objects.order_by('position').filter(heure_livraison__in=midi, date =tomorrow)
    livraisonsapresmidi =  Livraison.objects.order_by('position').filter(heure_livraison__in=apresmidi, date =tomorrow)
    livraisonsmatinn =  Livraison.objects.order_by('position').filter(heure_livraison__in= matin, date =aftertomorrow)
    livraisonsmidin =  Livraison.objects.order_by('position').filter(heure_livraison__in=midi, date =aftertomorrow)
    livraisonsapresmidin =  Livraison.objects.order_by('position').filter(heure_livraison__in=apresmidi, date =aftertomorrow)
    livraisonsmatinnn =  Livraison.objects.order_by('position').filter(heure_livraison__in= matin, date =afteraftertomorrow)
    livraisonsmidinn =  Livraison.objects.order_by('position').filter(heure_livraison__in=midi, date =afteraftertomorrow)
    livraisonsapresmidinn =  Livraison.objects.order_by('position').filter(heure_livraison__in=apresmidi, date =afteraftertomorrow)
    retourtraiteur = "oui"
    context = {'livraisons':livraisons,
               'recuperation': recuperation,
               'retourtraiteur': retourtraiteur,
               'livraisonsmatin': livraisonsmatin,
               'livraisonsmidi': livraisonsmidi,
               'livraisonsapresmidi': livraisonsapresmidi,
               'livraisonsok':livraisonsok,
               'livraisonrecup':livraisonrecup,
               'aftertomorrow':aftertomorrow,
               'afteraftertomorrow':afteraftertomorrow,
               'livraisonsmatinn':livraisonsmatinn,
               'livraisonsmatinnn':livraisonsmatinnn,
               'livraisonsmidin':livraisonsmidin,
               'livraisonsmidinn':livraisonsmidinn,
               'livraisonsapresmidinn':livraisonsapresmidinn,
               'livraisonsapresmidin':livraisonsapresmidin,




               }
    return render(request, 'listings/livraisonstomorrow.html', context)

def livraisonstoday(request):
    recuperation = "oui"
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    matin = ['05h00', '05h15', '05h30', '05h45', '06h00', '06h15', '06h30', '06h45', '07h00', '07h15', '07h30', '07h45', '08h00','08h15', '08h30', '08h45', '09h00', '09h15', '09h30','09h45']
    midi = ['10h00', '10h15', '10h30', '10h45', '11h00', '11h15', '11h30', '11h45', '12h00', '12h15', '12h30', '12h45']
    apresmidi = ['13h00', '13h15', '13h30', '13h45', '14h00', '14h15', '14h30', '14h45', '15h00', '15h15', '15h30', '15h45', '16h00', '16h15', '16h30', '16h45', '17h00', '17h15', '17h30', '17h45', '18h00', '18h15', '18h30', '18h45', '19h00']
    livraisons = Livraison.objects.order_by('position').filter(date=today)
    livraisonsmatin =  Livraison.objects.order_by('position').filter(heure_livraison__in= matin,date=today)
    livraisonsmidi =  Livraison.objects.order_by('position').filter(heure_livraison__in=midi, date=today)
    livraisonsapresmidi =  Livraison.objects.order_by('position').filter(heure_livraison__in=apresmidi, date=today)
    retourtraiteur = "oui"
    context = {'livraisons':livraisons,
               'recuperation': recuperation,
               'retourtraiteur': retourtraiteur,
               'livraisonsmatin': livraisonsmatin,
               'livraisonsmidi': livraisonsmidi,
               'livraisonsapresmidi': livraisonsapresmidi,
               }


    return render(request, 'listings/livraisonstoday.html', context)

def livraisonsresp(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    livraisonstatusok = Livraison.objects.filter(status=True, date=today,recuperation=False)
    livraisonstatusko = Livraison.objects.filter(status=False, date=today,recuperation=False)
    recuperations = Livraison.objects.filter(recuperation=True, date=today)
    recuperationok = Livraison.objects.filter(recuperation=True, status=True, date=today)
    recuperationko = Livraison.objects.filter(status=False,recuperation=True, date=today)
    recuperation = "oui"
    retourtraiteur = "oui"
    loic = "Loic"
    maxime= "Maxime"
    livraison = Livraison.objects.all()
    livraisons = Livraison.objects.order_by('position').filter(date=tomorrow)
    return render(request, 'listings/livraisonsresp.html', context={'livraisons': livraisons,


                                                              'livraisonstatusok':livraisonstatusok,
                                                              'livraisonstatusko':livraisonstatusko,
                                                              'retourtraiteur':retourtraiteur,
                                                              'recuperationok':recuperationok,
                                                              'recuperationko':recuperationko,
                                                              'recuperation' : recuperation,
                                                              'recuperations' : recuperations,
                                                              'loic':loic,
                                                              'maxime': maxime,
                                                              'tomorrow': tomorrow,

                                                              })

def recuptoday(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    recups = ["Porcelaine", "Chaud et porcelaine", "Porcelaine et bois", "Plateau de bois", "Froid et bois", "Chaud et jetable"]
    recuperations = Livraison.objects.filter(recuperation=False, date=today, mode_envoi__in = recups)
    recupsencours = Livraison.objects.filter(recuperation=True, status = False)
    return render(request, 'listings/recuptoday.html', context={
                                                              'recuperations' : recuperations,
                                                              'recupsencours' : recupsencours,
                                                              })

def faq(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)

    return render(request, 'listings/faq.html', context={
                                                              })


def livraisonrespdetail(request, ip):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    livraison = Livraison.objects.get(id=ip)
    livraisons = Livraison.objects.order_by('position').filter(date=tomorrow)
    livraisonstatusok = Livraison.objects.filter(status=True, date=today,recuperation=False)
    livraisonstatusko = Livraison.objects.filter(status=False, date=today,recuperation=False)
    recuperation = Livraison.objects.filter(recuperation=True, date=today)
    recuperationok = Livraison.objects.filter(recuperation=True, status=True, date=today)
    recuperationko = Livraison.objects.filter(status=False,recuperation=True, date=today)
    recuperation = "oui"
    retourtraiteur = "oui"
    formbis = LivraisonFeuilleForm(request.POST or None, instance=livraison)
    if formbis.is_valid():
       formbis.save()
       return redirect('livraisonstomorrow')

    return render(request, 'listings/livraisonrespdetail.html', context={'livraisons': livraisons,
                                                              'livraison':livraison,
                                                              'recuperation' : recuperation,
                                                              'livraisonstatusok':livraisonstatusok,
                                                              'livraisonstatusko':livraisonstatusko,
                                                              'retourtraiteur':retourtraiteur,
                                                              'recuperationok':recuperationok,
                                                              'recuperationko':recuperationko,
                                                              'recuperation' : recuperation,
                                                              'tomorrow':tomorrow,
                                                              'formbis':formbis,
                                                              })

def livraisonsventesdetail(request, pk):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    livraison = Livraison.objects.get(id=pk)
    livraisons = Livraison.objects.order_by('position').filter(date=tomorrow)
    livraisonstatusok = Livraison.objects.filter(status=True, date=today,recuperation=False)
    livraisonstatusko = Livraison.objects.filter(status=False, date=today,recuperation=False)
    recuperation = Livraison.objects.filter(recuperation=True, date=today)
    recuperationok = Livraison.objects.filter(recuperation=True, status=True, date=today)
    recuperationko = Livraison.objects.filter(status=False,recuperation=True, date=today)
    recuperation = "oui"
    retourtraiteur = "oui"
    formbis = LivraisonsVentesForm(request.POST or None, instance=livraison)
    if formbis.is_valid():
       formbis.save()
       return redirect('journees-list')

    return render(request, 'listings/livraisonsventes.html', context={'livraisons': livraisons,
                                                              'livraison':livraison,
                                                              'recuperation' : recuperation,
                                                              'livraisonstatusok':livraisonstatusok,
                                                              'livraisonstatusko':livraisonstatusko,
                                                              'retourtraiteur':retourtraiteur,
                                                              'recuperationok':recuperationok,
                                                              'recuperationko':recuperationko,
                                                              'recuperation' : recuperation,
                                                              'tomorrow':tomorrow,
                                                              'formbis':formbis,
                                                              })

def livraisonshier(request):

    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    yesterday = today - timedelta(1)
    livraisonstatusok = Livraison.objects.filter(status=True, date=yesterday,recuperation=False)
    livraisonstatusko = Livraison.objects.filter(status=False, date=yesterday,recuperation=False)
    recuperation = Livraison.objects.filter(recuperation=True, date=yesterday)
    recuperationok = Livraison.objects.filter(recuperation=True, status=True, date=yesterday)
    recuperationko = Livraison.objects.filter(status=False,recuperation=True, date=yesterday)
    recuperation = "oui"
    livraison = Livraison.objects.all()
    livraisons = Livraison.objects.order_by('position').filter(date=yesterday)
    return render(request, 'listings/livraisonshier.html', context={'livraisons': livraisons,

                                                              'recuperation' : recuperation,
                                                              'livraisonstatusok':livraisonstatusok,
                                                              'livraisonstatusko':livraisonstatusko,

                                                              'recuperationok':recuperationok,
                                                              'recuperationko':recuperationko,
                                                              'recuperation' : recuperation,
                                                              })


class Livraisonsdrag(ListView):
    template_name = 'listings/livraisonsdrag.html'
    model = Livraison

    context_object_name = 'livraisons'


    def get_queryset(self):

        today = datetime.now().date()
        tomorrow = today + timedelta(1)


        livraisons = Livraison.objects.order_by('position').filter(date=tomorrow)



        return livraisons



def add_livraison(request):
    # Extract data from POST request
    nom = request.POST.get('filmname')
    date = request.POST.get('date')

    # Validate date format (optional)
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    # Create and save the Livraison instance
    livraison = Livraison.objects.create(nom=nom, date=date_obj)

    # Fetch updated list of livraisons (you can filter this as needed)
    livraisons = Livraison.objects.all()

    # Render the updated livraison list (partial template)
    return render(request, 'listings/partials/livraisonslist.html', {'livraisons': livraisons})

def delete_livraison(request, pk):
    # remove the film from the user's list

    livraison = Livraison.objects.get(id=pk)

    livraison.delete()

    # return template fragment with all the user's films
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    livraisons = Livraison.objects.filter(date=tomorrow)

    return render(request, 'listings/partials/livraisonslist.html', {'livraisons': livraisons})

def sort(request):
    film_pks_order = request.POST.getlist('film_order')
    films = []
    for idx, film_pk in enumerate(film_pks_order, start=1):
        userfilm = Livraison.objects.get(id=film_pk)
        userfilm.order = idx
        userfilm.save()
        films.append(userfilm)

    return render(request, '/listings/partials/livraisonslist.html', {'films': films})

def livraisonsdrag_detailtoday(request, pk):
    livraison = Livraison.objects.get(id=pk)
    context = {'livraison': livraison}
    if request.method == 'GET':
        return render(request, 'listings/livraisonsdragtoday.html', context)
    elif request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = LivraisonDragFormtoday(data, instance=livraison)
        if form.is_valid():
            form.save()
            return render(request, 'listings/partials/livraisonslisttoday.html', context)

        context['form'] = form
        return render(request, 'listings/partials/edit-livraison-formtoday.html', context)

def livraison_edit_formtoday(request, pk):
    livraison = Livraison.objects.get(id=pk)
    form = LivraisonDragFormtoday(instance=livraison)
    context = {'livraison': livraison, 'form': form}
    return render(request, 'listings/partials/edit-livraison-formtoday.html', context)


class Livraisonsdragtoday(ListView):
    template_name = 'listings/livraisonsdragtoday.html'
    model = Livraison

    context_object_name = 'livraisons'


    def get_queryset(self):

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        livraisons = Livraison.objects.order_by('position').filter(date=tomorrow)

        return livraisons



def add_livraisontoday(request):
    nom = request.POST.get('filmname')
    date = request.POST.get('date')

    # add film
    livraison = Livraison.objects.create(nom=nom, date=date)

    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    livraisons = Livraison.objects.filter(date=today)

    return render(request, 'listings/partials/livraisonslisttoday.html', {'livraisons': livraisons})

def livraisonsdrag_detail(request, pk):
    livraison = Livraison.objects.get(id=pk)
    context = {'livraison': livraison}
    if request.method == 'GET':
        return render(request, 'listings/livraisonsdrag.html', context)
    elif request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = LivraisonDragForm(data, instance=livraison)
        if form.is_valid():
            form.save()
            return render(request, 'listings/partials/livraisonslist.html', context)

        context['form'] = form
        return render(request, 'listings/partials/edit-livraison-form.html', context)

def livraison_edit_form(request, pk):
    livraison = Livraison.objects.get(id=pk)
    form = LivraisonDragForm(instance=livraison)
    context = {'livraison': livraison, 'form': form}
    return render(request, 'listings/partials/edit-livraison-form.html', context)


def commentcamarche(request):
    context = {}
    return render(request, 'listings/commentcamarche.html', context)

def routesfrigo(request):
    today = timezone.now().date()
    routes = Route.objects.filter(date=today)
    journee = Journee.objects.filter(date=today)


    context = {
        'routes': routes,
        'journee':journee,
    }
    return render(request, 'listings/routesfrigo.html', context)


def duplicate_model(request, model_id):
    original_object = Livraison.objects.get(pk=model_id)
    today = datetime.now().date()
    tomorrow = today + timedelta(1)

    # Create a new object with the same attributes as the original
    new_object = Livraison()
    new_object.nom = original_object.nom
    new_object.mode_envoi = original_object.mode_envoi
    new_object.status = False
    new_object.recuperation = True
    new_object.client = original_object.client
    new_object.commentaire = original_object.commentaire
    new_object.commentairedispatch = original_object.commentairedispatch
    new_object.adress = original_object.adress
    new_object.infodetail = original_object.infodetail
    new_object.heure_livraison = "."
    new_object.zipcode = original_object.zipcode
    new_object.app = original_object.app
    new_object.ligne2 = original_object.ligne2
    new_object.convives = original_object.convives
    new_object.num_commande = original_object.num_commande
    new_object.nom_client = original_object.nom_client
    new_object.contact_site = original_object.contact_site
    new_object.date = tomorrow
    new_object.heure_livraison = new_object.heure_livraison = "recup"
    new_object.date_livraison = original_object.date_livraison
    new_object.statut = Route.objects.get(id=21)
    new_journee = Journee.objects.get(id=original_object.journee.id + 1)
    new_object.journee = new_journee
    new_object.lat = original_object.lat
    new_object.lng = original_object.lng
    new_object.place_id = original_object.place_id

    # Save the new Livraison object
    new_object.save()

    # Duplicate related Photo objects
    for photo_instance in original_object.livraison_photos.all():
        new_photo = Photo()
        new_photo.livraison = new_object  # Associate the new photo with the new Livraison
        new_photo.image = photo_instance.image  # Copy the image
        new_photo.caption = photo_instance.caption  # Copy the caption if available
        new_photo.save()

    # Redirect back to a page or render a template
    return redirect('recuptoday')  # Redirect to a specific URL name
