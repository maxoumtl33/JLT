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
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Checklist
from .forms import ChecklistForm, DateFilterForm
from django.utils import timezone
import calendar
from django.shortcuts import render
from django.http import JsonResponse
from .models import Checklist
from .forms import DistanceForm
from tablib import Dataset
from .ressources import LivraisonResource
from django.utils.timezone import now
from datetime import datetime, timedelta, time, date
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
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import transaction
from django.contrib import messages

@login_required
def create_ordercuisine(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        # Filter items by name or category name (ForeignKey lookup)
        items = ItemCuisine.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )
    else:
        items = ItemCuisine.objects.all()  # Get all items if no search query

    if request.method == 'POST':
        for item in items:
            # Get the quantity from the form for each item
            ordered_quantity = request.POST.get(f'quantity-{item.id}')
            if ordered_quantity and int(ordered_quantity) > 0:
                # Create or update the order
                order, created = OrderCuisine.objects.get_or_create(
                    user=request.user, 
                    item=item,
                    defaults={'ordered_quantity': ordered_quantity}
                )
                if not created:
                    order.ordered_quantity += int(ordered_quantity)
                    order.save()

        return redirect('order_list_cuisine')
    if not request.user.is_superuser:
        return redirect('unauthorized')

    return render(request, 'listings/create_ordercuisine.html', {'items': items})

@login_required
def user_order_list(request):
    orders = OrderCuisine.objects.filter(user=request.user)
    # Paginate the orders list
    paginator = Paginator(orders, 15)  # Show 15 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return render(request, 'listings/user_order_list.html', {'orders': page_obj})

@login_required
def update_order_cuisine(request, order_id):
    order = get_object_or_404(OrderCuisine, id=order_id, user=request.user)

    if request.method == 'POST':
        ordered_quantity = request.POST.get('ordered_quantity')
        if ordered_quantity:
            order.ordered_quantity = int(ordered_quantity)
            order.save()
    if not request.user.is_superuser:
        return redirect('unauthorized')
        return redirect('user_order_list')

@login_required
def delete_order_cuisine(request, order_id):
    order = get_object_or_404(OrderCuisine, id=order_id, user=request.user)

    # Prevent deletion if order is marked as done or delivered
    if order.is_done or order.is_delivered:
        # Optionally, you can add a message here to notify the user
        return redirect('user_order_list')

    order.delete()
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return redirect('user_order_list')

@login_required
def order_listcuisine(request):
    search_date = request.GET.get('search_date', None)
    
    if search_date:
        # Convert string to date
        search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
        orders = OrderCuisine.objects.filter(user=request.user, date=search_date)
    else:
        orders = OrderCuisine.objects.filter(user=request.user)

    # Paginate the orders list
    paginator = Paginator(orders, 15)  # Show 15 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if not request.user.is_superuser:
        return redirect('unauthorized')

    return render(request, 'listings/order_listcuisine.html', {
        'orders': page_obj,
        'search_date': search_date
    })

def mark_order_donecuisine(request, order_id):
    order = OrderCuisine.objects.get(id=order_id)
    order.is_done = True
    order.save()
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return redirect('order_list_cuisine')

def mark_order_deliveredcuisine(request, order_id):
    order = OrderCuisine.objects.get(id=order_id)
    order.is_delivered = True
    order.save()
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return redirect('order_list_cuisine')


def geocode_all_livraisons(request):
    if request.method == 'GET':  # Ensure the request method is GET
        livraisons = Livraison.objects.filter(lat__isnull=True, lng__isnull=True, place_id__isnull=True)

        if livraisons.exists():
            try:
                # Initialize the Google Maps Client with the API Key
                gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

                for livraison in livraisons:
                    if livraison.adress and livraison.country and livraison.zipcode and livraison.city:
                        # Create the address string for geocoding
                        adress_string = f"{livraison.adress}, {livraison.zipcode}, {livraison.city}, {livraison.country}"

                        # Perform geocoding request to Google Maps
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

                return JsonResponse({'success': True, 'message': 'Géocode reussit'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'Aucune livraison à géocoder'})
    
    # If the request method is not GET
    return JsonResponse({'success': False, 'error': 'Invalid request method. Use GET.'})

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
    if not request.user.is_superuser:
        return redirect('unauthorized')
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
            item.delete()
            response_data = {'status': 'success', 'message': 'Objet bien supprimé :)'}
        except ChecklistItem.DoesNotExist:
            response_data = {'status': 'error', 'message': 'Objet non trouvé'}
        return JsonResponse(response_data)
    
def voir_checklist(request):

    checklists = Checklist.objects.filter(is_active=True).order_by('-added_on')
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"
    today = date.today()

    current_year = date.today().year
    years = [year for year in range(current_year - 5, current_year + 1)]
    
    selected_day = int(request.GET.get('day', 1))  # Default to the first day of the month if none selected
    current_year = date.today().year
    months = [(month, calendar.month_name[month]) for month in range(1, 13)]
    selected_month = int(request.GET.get('month', today.month))
    # Get the number of days in the selected month
    _, num_days_in_month = calendar.monthrange(current_year, selected_month)
    days_in_month = [day for day in range(1, num_days_in_month + 1)]  # Adjust days in month

    french_months = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]

    # Fetch checklists for the selected month
    checklists = Checklist.objects.filter(date__month=int(selected_month))
    
    change_logs = ChecklistItemChangeLog.objects.all().order_by('-timestamp')
    change_logs_checklist = ChecklistChangeLog.objects.all().order_by('-timestamp')

    context = {

        'checklists': checklists,
        'encours': encours,
        'valide': valide,
        'refuse': refuse,
        'change_logs': change_logs,
        'change_logs_checklist': change_logs_checklist,
        'today': today,
        'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Months as numbers
        'selected_month': selected_month,
        'days': days_in_month,
        'months': months,
        'french_months': french_months,
        'selected_day': selected_day,
        'selected_date': date(current_year, selected_month, selected_day).strftime('%d %B %Y'),
        'years': years,
        'selected_year': current_year,
    }
    return render(request, 'listings/voir-checklist.html', context)

def checklistvoir_detail(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    checklist_item = ChecklistItem.objects.filter(checklist=checklist)
    quantity_change_logs = QuantityChangeLog.objects.filter(
        checklist_item__checklist_id=checklist_id
    ).order_by('-timestamp')
    change_logs = ChecklistItemChangeLog.objects.filter(checklist_item__checklist=checklist).order_by('-timestamp')
    products = Product.objects.all()
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"

    # Process the checklist note form if submitted
    if request.method == 'POST':
        # Check if the form is for updating the note
        if 'note' in request.POST:
            note = request.POST.get('note')
            if note is not None:
                checklist.notechecklist = note  # Save the note to the model
                checklist.save()
            return redirect('checklistvoir-detail', checklist_id=checklist_id)  # Redirect back to the same page

        # Process the checklist item status change form
        item_id = request.POST.get('item_id')
        status = request.POST.get('status')

        if item_id and status:
            checklist_item = get_object_or_404(ChecklistItem, id=item_id, checklist=checklist)
            checklist_item.status = status
            checklist_item.save()

            # Update checklist status based on items' statuses
            checklist.update_status()

            return redirect('checklistvoir-detail', checklist_id=checklist_id)

    # Prepare checklist items to be displayed with their statuses
    items = ChecklistItem.objects.filter(checklist=checklist)

    context = {
        'checklist': checklist,
        'checklist_item': checklist_item,
        'products': products,
        'items': items,
        'encours': encours,
        'valide': valide,
        'refuse': refuse,
        'quantity_change_logs': quantity_change_logs,
        'change_logs': change_logs,
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

import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def add_to_checklist(request, checklist_id):
    if request.method == 'POST':
        checklist = get_object_or_404(Checklist, pk=checklist_id)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        commentaire = request.POST.get('commentaire')
        product = get_object_or_404(Product, pk=product_id)

        

        checklist_item, created = ChecklistItem.objects.get_or_create(
            checklist=checklist, 
            product=product,
            defaults={'quantity': quantity, 'commentaire': commentaire}
        )

        if not created:
            checklist_item._changed_by = request.user
            checklist_item.quantity = quantity
            checklist_item.commentaire = commentaire
            checklist_item.save()

        return JsonResponse({'success': True, 'message': 'Objet ajouté avec succès'})

    return redirect(request.META.get('HTTP_REFERER', '/'))


def checklist_detail(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    checklist_items = ChecklistItem.objects.filter(checklist=checklist)
    breuvages = ChecklistItem.objects.filter(checklist=checklist, product__category = "BREUVAGE")
    checklist_documents = ChecklistDocument.objects.filter(checklist=checklist)
    recup_photos = ChecklistRecupPhoto.objects.filter(checklist=checklist)
    md_photos = ChecklistMDPhoto.objects.filter(checklist=checklist)
    products = Product.objects.all()
    query = request.GET.get('query')
    checklist_item_quantities = {
        item.product_id: item.quantity for item in checklist_items
    }
    checklist_item_comments = {item.product_id: item.commentaire for item in checklist_items}

    # Define categories
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
    breuvage = "BREUVAGE"
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"

    # Document formset for uploading multiple documents
    document_formset = ChecklistDocumentFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=ChecklistDocument.objects.filter(checklist=checklist),
        prefix='documents'
    )

    # Checklist form instance
    formbis = ChecklistForm(request.POST or None, instance=checklist, prefix='checklist_form')
    commentaire_form = CommentaireForm(request.POST or None, instance=checklist, prefix='commentaire_form')

    if 'documents-TOTAL_FORMS' in request.POST and document_formset.is_valid():
        documents = document_formset.save(commit=False)
        for document in documents:
            document.checklist = checklist
            document.save()
        return HttpResponseRedirect(reverse('checklist-detail', args=[checklist_id]))

    elif 'checklist_form-name' in request.POST and formbis.is_valid():
        formbis.save()
        return HttpResponseRedirect(reverse('checklist-detail', args=[checklist_id]))
    
    elif 'commentaire_form-commentairevente' in request.POST and commentaire_form.is_valid():
        commentaire_form.save()
        return HttpResponseRedirect(reverse('checklist-detail', args=[checklist_id]))



    # Filter products based on the search query
    if query:
        products = products.filter(name__icontains=query)

    context = {
        'encours':encours,
        'breuvages': breuvages,
        'valide': valide,
        'refuse': refuse,
        'checklist': checklist,
        'checklist_items': checklist_items,
        'products': products,
        'equipementdebase': equipementdebase,
        'jetable': jetable,
        'accessoirededecor': accessoirededecor,
        'equipementdebar': equipementdebar,
        'equipementpourservicecafe': equipementpourservicecafe,
        'itemsdivers': itemsdivers,
        'tableetlinge': tableetlinge,
        'verrerie': verrerie,
        'breuvage': breuvage,
        'porcelaine': porcelaine,
        'montage': montage,
        'cuisson': cuisson,
        'service': service,
        'formbis': formbis,
        'commentaire_form': commentaire_form,
        'document_formset': document_formset,
        'checklist_documents': checklist_documents,
        'recup_photos': recup_photos,
        'md_photos': md_photos,
        'checklist_item_quantities': checklist_item_quantities,
        'checklist_item_comments': checklist_item_comments,
    }
    return render(request, 'listings/checklist_detail.html', context)




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


@login_required
def conseiller_dashboard(request):
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"
    conseiller_instance = get_object_or_404(Conseiller, user=request.user)
    checklists = Checklist.objects.filter(conseillere=conseiller_instance)
    active_checklists = checklists.filter(is_active=True)
    inactive_checklists = checklists.filter(is_active=False)
    paginator = Paginator(checklists, 10)  # 10 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Initialize both forms
    checklist_form = ChecklistForm(initial={'conseillere': conseiller_instance})

    if request.method == 'POST':
        if 'create_checklist' in request.POST:
            # Handle the checklist creation form
            checklist_form = ChecklistForm(request.POST)
            if checklist_form.is_valid():
                checklist = checklist_form.save(commit=False)
                checklist.conseillere = conseiller_instance
                checklist.save()
                messages.success(request, 'Nouvelle checklist créée.')
                return redirect('conseiller_dashboard')
            else:
                messages.error(request, 'Veuillez corriger les erreurs dans le formulaire de création.')

        elif 'toggle_checklist' in request.POST:
            # Handle the toggle checklist action
            checklist_id = request.POST.get('checklist_id')
            try:
                checklist = Checklist.objects.get(id=checklist_id, conseillere=conseiller_instance)
                checklist.is_active = not checklist.is_active
                checklist.save()
                if checklist.is_active:
                    messages.success(request, 'Checklist activée.')
                else:
                    messages.success(request, 'Checklist désactivée.')
            except Checklist.DoesNotExist:
                messages.error(request, 'Checklist non trouvée.')

    context = {
        'checklists': checklists,
        'checklist_form': checklist_form,
        'conseiller_instance': conseiller_instance,
        'active_checklists': active_checklists,
        'inactive_checklists': inactive_checklists,  # Update context to use checklist_form
        'page_obj': page_obj,
        'encours': encours,
        'valide': valide,
        'refuse': refuse,
    }

    return render(request, 'listings/conseiller_dashboard.html', context)

def creerchecklist(request):
    # Retrieve all checklists and define status labels
    checklists = Checklist.objects.all().order_by('date')
    encours = "en_cours"
    valide = "valide"
    refuse = "refuse"
    today = date.today()

    current_year = date.today().year
    years = [year for year in range(current_year - 5, current_year + 1)]
    
    selected_day = int(request.GET.get('day', 1))  # Default to the first day of the month if none selected
    current_year = date.today().year
    months = [(month, calendar.month_name[month]) for month in range(1, 13)]
    selected_month = int(request.GET.get('month', today.month))
    # Get the number of days in the selected month
    _, num_days_in_month = calendar.monthrange(current_year, selected_month)
    days_in_month = [day for day in range(1, num_days_in_month + 1)]  # Adjust days in month

    french_months = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]

    # Fetch checklists for the selected month
    checklists = Checklist.objects.filter(date__month=int(selected_month))


    form2 = ChecklistForm()

    if request.method == 'POST':
        form2 = ChecklistForm(request.POST)
        if form2.is_valid():
            form2.save()
            messages.success(request, 'Nouvelle Checklist')
            return redirect('creerchecklist')

 

    context = {
        'checklists': checklists,
        'form2': form2,
        'encours': encours,
        'valide': valide,
        'refuse': refuse,
        'today': today,
        'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Months as numbers
        'selected_month': selected_month,
        'days': days_in_month,
        'months': months,
        'french_months': french_months,
        'selected_day': selected_day,
        'selected_date': date(current_year, selected_month, selected_day).strftime('%d %B %Y'),
        'years': years,
        'selected_year': current_year,
    }
    
    return render(request, 'listings/checklistcreate.html', context)


from django.http import JsonResponse
from django.utils.dateparse import parse_date
from .models import Checklist
import calendar
from django.utils import formats

def get_checklists_for_day(request, day):
    # Get the selected month and year
    selected_month = int(request.GET.get('month', date.today().month))
    selected_year = int(request.GET.get('year', date.today().year))

    # Ensure day is within the range of the selected month
    _, num_days_in_month = calendar.monthrange(selected_year, selected_month)
    day = min(int(day), num_days_in_month)  # Prevent out-of-range days

    # Construct the date object for filtering checklists
    selected_date = date(selected_year, selected_month, day)

    selected_date_formatted = formats.date_format(selected_date, "j F Y", use_l10n=True)

    # Retrieve only active checklists for the selected date
    checklists = Checklist.objects.filter(date=selected_date, is_active=True).select_related('conseillere').values(
        'id', 'name', 'date', 'heure_livraison', 'nb_convive', 'status', 
        'conseillere__user__username', 'added_on'
    )

    # Prepare data for JSON response
    checklists_list = list(checklists)
    
    # Format the date objects for JSON serialization
    for checklist in checklists_list:
        checklist['date'] = checklist['date'].strftime('%Y-%m-%d')
        checklist['conseillere'] = checklist.get('conseillere__user__username', 'N/A')  # Get the username or set to 'N/A'

    response_data = {
        'checklists': checklists_list,
        'selected_date': selected_date_formatted,
    }

    return JsonResponse(response_data)
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


from django.http import HttpResponse
from django.urls import reverse
import qrcode
from django.conf import settings

def generate_qr_code(request, product_id):
    # Get product details
    product = Product.objects.get(id=product_id)
    quantity = product.quantity  # You can include any relevant information for the QR code
    
    # URL that will be encoded in the QR code
    product_url = reverse('product_quantity_update', args=[product_id])
    
    # Generate the full URL including the domain
    full_url = request.build_absolute_uri(product_url)
    
    # Create the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(full_url)  # Use the full URL with domain
    qr.make(fit=True)
    
    # Create an image of the QR code
    img = qr.make_image(fill='black', back_color='white')
    
    # Create an HTTP response with the image
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


from django.shortcuts import render, redirect
from .models import Product, QuantityChangeLog
from django.contrib.auth.models import User

def update_product_quantity(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        increment = request.POST.get('quantity')
        
        # Ensure increment is a valid number
        if increment and increment.isdigit():
            # Get the previous quantity
            previous_quantity = product.quantity
            
            # Add the increment to the current quantity
            product.quantity += int(increment)
            product.save()  # Save the updated product
            
            # Log the change
            QuantityProductChangeLog.objects.create(
                product=product,
                previous_quantity=previous_quantity,
                new_quantity=product.quantity,
                user=request.user,  # The user who made the change
            )
            
            return redirect('product_list')  # Redirect to the product list or another page
            
        else:
            # Handle invalid input (non-numeric or empty value)
            return render(request, 'listings/update_quantity.html', {'product': product, 'error': 'Veuillez entrer une quantité valide.'})
    
    return render(request, 'listings/update_quantity.html', {'product': product})

from django.shortcuts import render
from .models import QuantityChangeLog

from datetime import timedelta

def view_quantity_change_logs(request, product_id):
    product = Product.objects.get(id=product_id)
    logs = QuantityProductChangeLog.objects.filter(product=product).order_by('-timestamp')

    # Calculate the difference for each log entry and adjust timestamp
    for log in logs:
        log.difference = log.new_quantity - log.previous_quantity
        log.adjusted_timestamp = log.timestamp - timedelta(hours=5)  # Subtract 5 hours

    context = {
        'product': product,
        'logs': logs,
    }
    
    return render(request, 'listings/view_logs.html', context)







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
    if not request.user.is_superuser:
        return redirect('unauthorized')
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

from django.http import JsonResponse
from .models import Product


def search_productsbase(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "ÉQUIPEMENT DE BASE") if query else Product.objects.filter( category = "ÉQUIPEMENT DE BASE")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def search_productsjetable(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "JETABLE") if query else Product.objects.filter( category = "JETABLE")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    return JsonResponse({'products': product_data})

def search_productsdecor(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "ACCESSOIRES DE DÉCOR") if query else Product.objects.filter( category = "ACCESSOIRES DE DÉCOR")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def search_productsbar(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "ÉQUIPEMENT DE BAR") if query else Product.objects.filter( category = "ÉQUIPEMENT DE BAR")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def search_productscafe(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "ÉQUIPEMENT POUR SERVICE CAFÉ") if query else Product.objects.filter( category = "ÉQUIPEMENT POUR SERVICE CAFÉ")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def get_breuvages_products(request, checklist_id):
    breuvages_items = ChecklistItem.objects.filter(checklist_id=checklist_id, product__category="BREUVAGE")
    
    product_data = [
        {
            'id': item.product.id,
            'name': item.product.name,
            'total_quantity': item.total_quantity,
            'consumed_quantity': item.consumed_quantity,
            'unconsumed_quantity': item.unconsumed_quantity
        }
        for item in breuvages_items
    ]
    
    return JsonResponse({'products': product_data})

def search_productstable(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "TABLE ET LINGE DE TABLE") if query else Product.objects.filter( category = "TABLE ET LINGE DE TABLE")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def search_productsverre(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "VERRERIE") if query else Product.objects.filter( category = "VERRERIE")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def search_productsporcelaine(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "PORCELAINE ET COUTELLERIE") if query else Product.objects.filter( category = "PORCELAINE ET COUTELLERIE")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def search_productscanape(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "ÉQUIPEMENT POUR MONTAGE CANAPÉS") if query else Product.objects.filter( category = "ÉQUIPEMENT POUR MONTAGE CANAPÉS")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def search_productscuisson(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "ÉQUIPEMENT DE CUISSON") if query else Product.objects.filter( category = "ÉQUIPEMENT DE CUISSON")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})
def search_productsservice(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "USTENSILES DE SERVICE") if query else Product.objects.filter( category = "USTENSILES DE SERVICE")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})
def search_productsdivers(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "ITEMS DIVERS") if query else Product.objects.filter( category = "ITEMS DIVERS")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})
def search_productsbreuvage(request, checklist_id):
    query = request.GET.get('query', '')
    checklist_items = ChecklistItem.objects.filter(checklist_id=checklist_id)
    products = Product.objects.filter(name__icontains=query, category = "BREUVAGE") if query else Product.objects.filter( category = "BREUVAGE")
    
    product_data = []
    for product in products:
        # Get the quantity for each product from the checklist
        checklist_item = checklist_items.filter(product=product).first()
        quantity = checklist_item.quantity if checklist_item else 0
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'checklist_quantity': quantity,  # Add this to send the checklist quantity
        })
    
    return JsonResponse({'products': product_data})

def save_breuvages_report(request, checklist_id):
    if request.method == "POST":
        for item_id, consumed in request.POST.items():
            if item_id.startswith("consumed_"):
                item_id = int(item_id.split("_")[1])
                checklist_item = ChecklistItem.objects.get(id=item_id)
                
                consumed_quantity = int(consumed)
                unconsumed_quantity = int(request.POST.get(f'unconsumed_{item_id}', 0))
                
                checklist_item.consumed_quantity = consumed_quantity
                checklist_item.unconsumed_quantity = unconsumed_quantity
                checklist_item.save()
        
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

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
    if not request.user.is_superuser:
        return redirect('unauthorized')
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
    md = "md"
    


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
                                                              'is_md': request.user.groups.filter(name='md').exists(),
                                                              'is_ventes': request.user.groups.filter(name='ventes').exists(),
                                                              'is_livreur': request.user.groups.filter(name='livreurs').exists(),
                                                              'jef':jef,
                                                              'md':md,
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
    journees = get_object_or_404(Journee, id=id)
    livreurs = Livreur.objects.all()
    shifts = Shift.objects.filter(date=journees.date)
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
            'status': livraison.status,
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
                      'shifts': shifts,
                  })  # nous passons l'id au modèle



def livreur_list(request):
    if request.user.is_authenticated:
        livreurs = Livreur.objects.exclude(user=request.user)
        return render(request, 'listings/livreur_list.html', context={'livreurs': livreurs
                                                                      })
    else:
        return redirect('home')

def validate_livraison(request, livraison_id):
    livraison = get_object_or_404(Livraison, id=livraison_id)
    form = LivraisonForm(request.POST or None, instance=livraison)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('livraison-detail', ip=livraison_id)
    return redirect('livraison-detail', ip=livraison_id)

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

def view_shifts_by_date(request):
    # Get date from the request or use today’s date as default
    selected_date = request.GET.get('date', now().date())
    
    # Fetch all shifts for that date
    shifts = Shift.objects.filter(date=selected_date).select_related('livreur')
    if not request.user.is_superuser:
        return redirect('unauthorized')

    return render(request, 'listings/view_shifts_by_date.html', {
        'shifts': shifts,
        'selected_date': selected_date
    })

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

# Admin view for creating shifts


def create_shift(request):
    # Get the list of livreur for which shifts will be created
    liste_livreur = Livreur.objects.filter(nom__in=['Maxime', 'Alex', 'Mohammad', 'Osnel', 'Samuel', 'Jef', 'Zayd'])

    if request.method == 'POST':
        for livreur in liste_livreur:
            # Check if the driver is marked as 'repos'
            is_repos = f"repos_{livreur.id}" in request.POST

            # Get shift data from POST request
            shift_date = request.POST.get(f"shift_date_{livreur.id}")
            shift_start = request.POST.get(f"shift_start_{livreur.id}")
           
            # Check that shift date is provided (start time can be empty)
            if not shift_date:
                return render(request, 'listings/create_shift.html', {'error': 'La date est requise.'})

            # Validate start time if it's provided (optional field)
            if shift_start:
                try:
                    datetime.strptime(shift_start, '%H:%M')
                except ValueError:
                    return render(request, 'listings/create_shift.html', {'error': 'Le format de l\'heure de début est invalide. Veuillez entrer l\'heure au format HH:MM.'})

            

            # Create shift if not in repos
            if is_repos:
                Shift.objects.create(
                    livreur=livreur,
                    date=shift_date,
                    start_time=None,  # No start time for repos
                    notes="Repos"
                )
            else:
                # If repos is not checked, create a shift with start and end time if provided
                Shift.objects.create(
                    livreur=livreur,
                    date=shift_date,
                    start_time=shift_start or None,  # Set start time to None if it's empty
                    notes=""
                )

        # Redirect after creating shifts
        return redirect('acceuilresponsables')

    # Handle GET request to render the page with livreur list
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return render(request, 'listings/create_shift.html', {'liste_livreur': liste_livreur})

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
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return render(request, 'listings/responsableschoixjournee.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journees' : journees,
                                                              })

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
    if not request.user.is_superuser:
        return redirect('unauthorized')
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

def unauthorized_view(request):
    return render(request, 'listings/pasauthorise.html', status=403)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_list(request):
    query = request.GET.get('query', '')  # Get the search query (if any)
    
    # Retrieve all products
    products = Product.objects.all()

    # Apply filter if there is a query
    if query:
        products = products.filter(name__icontains=query)  # Filter by name containing query

    # Paginate the products (10 products per page)
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')

    try:
        # Try to get the page object for the requested page number
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If the page number is not an integer, display the first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If the page number is out of range (too large), display the last page
        page_obj = paginator.get_page(paginator.num_pages)

    # Return the context to the template
    return render(request, 'listings/product_list.html', {'page_obj': page_obj,
                                                           'query': query,
                                                           'is_ventes': request.user.groups.filter(name='ventes').exists(),
                                                           'is_checklist': request.user.groups.filter(name='checklist').exists(),
                                                           'is_admin': request.user.groups.filter(name='admin').exists(),
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

class MapAujourView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        matin = ['05h00', '05h15', '05h30', '05h45', '06h00', '06h15', '06h30', '06h45', '07h00', '07h15', '07h30', '07h45', '08h00','08h15', '08h30', '08h45', '09h00', '09h15', '09h30', '09h45', 'recup']
        distances = Distances.objects.all()
        todo_livraison = Livraison.objects.filter(date=today, heure_livraison__in = matin, place_id__isnull=False, statut__id= 21)
        route1 = Livraison.objects.filter(date=today, heure_livraison__in = matin)
        recups = Livraison.objects.filter(date=today, recuperation = True)
        route2 = Livraison.objects.filter(statut__id= 2, date=today, heure_livraison__in = matin)
        route3 = Livraison.objects.filter(statut__id= 3, date=today, heure_livraison__in = matin)
        route4 = Livraison.objects.filter(statut__id= 4, date=today, heure_livraison__in = matin)
        routesmatin = ['1','2','3','4','5','6']
        routes21 = Route.objects.filter(id=21)
        routes = Route.objects.filter(date=today, nom__in=routesmatin)
        eligable_locations = Livraison.objects.order_by('position').filter(place_id__isnull=False, heure_livraison__in = matin, date=today)
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
                   'recups': recups,
                   'todo_livraison':todo_livraison,
                   'routes21':routes21,
                   'tomorrow':tomorrow,

        }
        return render(request, 'listings/mapmatinaujour.html', context)

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

        return redirect('my_mapaujour_view')
class MapApremAujourView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        distances = Distances.objects.all()
        aprem = ['13h00', '13h15', '13h30', '13h45', '14h00', '14h15', '14h30', '14h45', '15h00', '15h15', '15h30', '15h45', '16h00', '16h15', '16h30', '16h45', '17h00', '17h15', '17h30', '17h45', '18h00', '18h15', '18h30', '18h45', '19h00', 'recup']
        todo_livraison = Livraison.objects.filter(statut=21, date=today, heure_livraison__in = aprem, place_id__isnull=False)
        routesaprem = ['6','7','8','9','10','11','12','13','14','15','16','17', '18','19','20']
        routes = Route.objects.filter(date=today, nom__in=routesaprem)
        route1 = Livraison.objects.filter(date=today, heure_livraison__in = aprem)
        route7 = Livraison.objects.filter(statut='7', date=today, heure_livraison__in = aprem)
        route8 = Livraison.objects.filter(date=today, heure_livraison__in = aprem)
        route9 = Livraison.objects.filter(statut='9', date=today, heure_livraison__in = aprem)
        route10 = Livraison.objects.filter(statut='27', date=today, heure_livraison__in = aprem)
        route11 = Livraison.objects.filter(statut='11', date=today, heure_livraison__in = aprem)
        route12 = Livraison.objects.filter(statut='12', date=today, heure_livraison__in = aprem)
        route13 = Livraison.objects.filter(statut='13', date=today, heure_livraison__in = aprem)
        route14 = Livraison.objects.filter(statut='14', date=today, heure_livraison__in = aprem)
        route15 = Livraison.objects.filter(statut='15', date=today, heure_livraison__in = aprem)
        route16 = Livraison.objects.filter(statut='16', date=today, heure_livraison__in = aprem)
        route17 = Livraison.objects.filter(statut='17', date=today, heure_livraison__in = aprem)
        route18 = Livraison.objects.filter(statut='18', date=today, heure_livraison__in = aprem)
        route19 = Livraison.objects.filter(statut='19', date=today, heure_livraison__in = aprem)
        route20 = Livraison.objects.filter(statut='20', date=today, heure_livraison__in = aprem)
        routes21 = Route.objects.filter(id=21)
        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = aprem, date=today )
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
        return render(request, 'listings/mapapremaujour.html', context)

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

        return redirect('my_mapapremaujour_view')
class MapMidiAujourView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        form = DistanceForm
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        distances = Distances.objects.all()
        midi = ['10h00', '10h15', '10h30', '10h45', '11h00', '11h15', '11h30', '11h45', '12h00', '12h15', '12h30', '12h45', 'recup']
        todo_livraison = Livraison.objects.filter(statut=21, date=today, heure_livraison__in = midi, place_id__isnull=False)
        routesmidi = ['2','3','4','5','6','7','8','9','10','11','12']
        routes21 = Route.objects.filter(id=21)
        routes = Route.objects.filter(date=today, nom__in=routesmidi)
        route1 = Livraison.objects.filter(date=today, heure_livraison__in=midi)
        route2 = Livraison.objects.filter(date=today, heure_livraison__in = midi)
        route3 = Livraison.objects.filter(statut='3', date=today, heure_livraison__in = midi)
        route4 = Livraison.objects.filter(statut='4', date=today, heure_livraison__in = midi)
        route5 = Livraison.objects.filter(statut='5', date=today, heure_livraison__in = midi)
        route6 = Livraison.objects.filter(statut='6', date=today, heure_livraison__in = midi)
        route7 = Livraison.objects.filter(statut='7', date=today, heure_livraison__in = midi)
        route8 = Livraison.objects.filter(statut='8', date=today, heure_livraison__in = midi)
        route9 = Livraison.objects.filter(statut='9', date=today, heure_livraison__in = midi)

        eligable_locations = Livraison.objects.filter(place_id__isnull=False, heure_livraison__in = midi, date=today)
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
        return render(request, 'listings/mapmidiaujour.html', context)

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

        return redirect('my_mapmidiaujour_view')


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
        recups = Livraison.objects.filter(date=tomorrow, recuperation = True)
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
                   'recups': recups,
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
        return render(request, 'listings/mapapremdim.html', context)

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
        aftertomorrow = today + timedelta(3)
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
        return render(request, 'listings/mapmididim.html', context)

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

from difflib import get_close_matches

def livraison_detail(request, ip):
    livraison = get_object_or_404(Livraison, id=ip)
    adresse = livraison.adress
    livreur = Livreur.objects.all()
    journee = Journee.objects.all()
    recuperation = "oui"
    loic = "Loic"
    maxime = "Maxime"
    # If already having place_id, try matching it.
    matching_dock = None
    dock_photos = None

    if livraison.place_id:
        matching_dock = LoadingDock.objects.filter(place_id=livraison.place_id).first()
        dock_photos = matching_dock.photo if matching_dock else None

    # Google Maps geocode to fetch place_id and coordinate information
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    result = gmaps.geocode(adresse)

    if result:
        place_id = result[0].get('place_id')
        if place_id:
            livraison.place_id = place_id
            livraison.save()

    if request.method == 'POST':
        form = LivraisonForm(request.POST, instance=livraison)
        formbis = PhotoFormSet(request.POST, request.FILES, instance=livraison)
        
        if form.is_valid():
            livraison = form.save()
        if formbis.is_valid():
            photos = formbis.save(commit=False)
            for photo in photos:
                photo.livraison = livraison
                photo.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        form = LivraisonForm(instance=livraison)
        formbis = PhotoFormSet(instance=livraison)

    # Use Google Maps API to geocode address
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    result = gmaps.geocode(adresse)
    checklist = Checklist.objects.filter(livraison=livraison)
    

    return render(request, 'listings/livraison_detail.html', {
        'livraison': livraison,
        'livreur': livreur,
        'recuperation': recuperation,
        'form': form,
        'journee': journee,
        'result': result,
        'adresse': adresse,
        'loic': loic,
        'maxime': maxime,
        'formbis': formbis,
        'checklist': checklist,
        'dock_photos': dock_photos,
        'matching_dock': matching_dock,
    })

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

def create_loading_dock(request):
    if request.method == 'POST':
        form = LoadingDockForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_loading_dock')  # Redirect to a page after saving, adjust as necessary
    else:
        form = LoadingDockForm()

    return render(request, 'listings/create_loading_dock.html', {'form': form})

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
    livraisonsmatinaujour =  Livraison.objects.order_by('position').filter(heure_livraison__in= matin, date =today)
    livraisonsmidiaujour =  Livraison.objects.order_by('position').filter(heure_livraison__in=midi, date =today)
    livraisonsapresmidiaujour =  Livraison.objects.order_by('position').filter(heure_livraison__in=apresmidi, date =today)
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
               'livraisonsmatinaujour':livraisonsmatinaujour,
               'livraisonsmidiaujour':livraisonsmidiaujour,
               'livraisonsapresmidiaujour':livraisonsapresmidiaujour,
               }
    if not request.user.is_superuser:
        return redirect('unauthorized')
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

    if not request.user.is_superuser:
        return redirect('unauthorized')

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
    if not request.user.is_superuser:
        return redirect('unauthorized')
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
    recups = ["Porcelaine", "Chaud et porcelaine", "Porcelaine et bois", "Plateau de bois", "Froid et bois", "Chaud et jetable", "Froid et porcelaine"]

    # Querysets
    recuperations = Livraison.objects.filter(recuperation=False, date=today, mode_envoi__in=recups)
    recupsencours = Livraison.objects.filter(recuperation=True, status=False)
    recuperationstot_list = Livraison.objects.filter(recuperation=False, mode_envoi__in=recups)

    # Pagination
    paginator = Paginator(recuperationstot_list, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    recuperationstot = paginator.get_page(page_number)
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return render(request, 'listings/recuptoday.html', context={
        'recuperations': recuperations,
        'recupsencours': recupsencours,
        'recuperationstot': recuperationstot,
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
    if not request.user.is_superuser:
        return redirect('unauthorized')
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
        # Default queryset for the view
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        
        # Query for tomorrow's deliveries (default queryset)
        livraisons = Livraison.objects.order_by('position').filter(date=tomorrow)
        
        return livraisons

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get current date and the next few days
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        tomorrow1 = today + timedelta(2)
        tomorrow2 = today + timedelta(3)

        # Add queries for each day
        livraisonstoday = Livraison.objects.order_by('position').filter(date=today)
        livraisonsdim = Livraison.objects.order_by('position').filter(date=tomorrow1)
        livraisonslundi = Livraison.objects.order_by('position').filter(date=tomorrow2)

        # Add these to the context so that the template can access them
        context['livraisonstoday'] = livraisonstoday
        context['livraisonsdim'] = livraisonsdim
        context['livraisonslundi'] = livraisonslundi

        return context



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


from django.shortcuts import render, get_object_or_404
from .models import Md, Checklist
from .forms import DateFilterForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def md_dashboard(request):
    # Get the Md instance related to the logged-in user
    md_instance = get_object_or_404(Md, user=request.user)  # This fetches the Md object for the logged-in user
    
    # Get related checklists for the Md instance
    checklists = Checklist.objects.filter(md=md_instance, is_active=True)
    
    # Handle date filtering if applicable
    if request.method == 'GET' and 'date' in request.GET:
        form = DateFilterForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            checklists = checklists.filter(date=date)
    else:
        form = DateFilterForm()

    # Paginate the checklists
    paginator = Paginator(checklists, 10)  # Show 10 checklists per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context data to pass to the template
    context = {
        'md_instance': md_instance,
        'checklists': checklists,
        'form': form,
        'page_obj': page_obj,
    }

    return render(request, 'listings/md_dashboard.html', context)

from django.shortcuts import get_object_or_404, redirect, render
from .models import Checklist, ChecklistMDPhoto, ChecklistRecupPhoto
from .forms import ChecklistMDPhotoFormSet, ChecklistRecupPhotoFormSet, RapportForm, RapportRecupForm


def ChecklistmdDetailView(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)
    md_photos = ChecklistMDPhoto.objects.filter(checklist=checklist)
    recup_photos = ChecklistRecupPhoto.objects.filter(checklist=checklist)
    checklist_items = ChecklistItem.objects.filter(checklist=checklist)
    checklist_documents = ChecklistDocument.objects.filter(checklist=checklist)
    # Initialize the formsets and forms with unique prefixes
    formset = ChecklistMDPhotoFormSet(request.POST or None, request.FILES or None, prefix='formset', queryset=ChecklistMDPhoto.objects.filter(checklist=checklist))
    formset1 = ChecklistRecupPhotoFormSet(request.POST or None, request.FILES or None, prefix='formset1', queryset=ChecklistRecupPhoto.objects.filter(checklist=checklist))
    form = RapportForm(request.POST or None, prefix='form', instance=checklist)
    form1 = RapportRecupForm(request.POST or None, prefix='form1', instance=checklist)
    checklist_itemsbreuvage = ChecklistItem.objects.filter(checklist_id=checklist, product__category="BREUVAGE")
    
    for item in checklist_itemsbreuvage:
        item.remaining_quantity = item.quantity - (item.consumed_quantity or 0)

    if request.method == 'POST':
    # Check which form or formset was submitted and process only that one
        if 'formset-TOTAL_FORMS' in request.POST and formset.is_valid():
            for form in formset:
                if form.cleaned_data:  # Ensure there's data to save
                    checklist_photo = form.save(commit=False)
                    checklist_photo.checklist = checklist  # Associate with the checklist
                    checklist_photo.save()
            return redirect('checklistmd_detail', pk=checklist.pk)

        elif 'formset1-TOTAL_FORMS' in request.POST and formset1.is_valid():
            for form in formset1:
                if form.cleaned_data:  # Ensure there's data to save
                    recup_photo = form.save(commit=False)
                    recup_photo.checklist = checklist  # Associate with the checklist
                    recup_photo.save()
            return redirect('checklistmd_detail', pk=checklist.pk)

        elif 'form-rapportmd' in request.POST and form.is_valid():
            form.save()
            return redirect('checklistmd_detail', pk=checklist.pk)

        elif 'form1-rapportrecup' in request.POST and form1.is_valid():
            form1.save()
        return redirect('checklistmd_detail', pk=checklist.pk)


    context = {
        'checklist': checklist,
        'livraison': checklist.livraison,
        'formset': formset,
        'formset1': formset1,
        'form': form,
        'checklist_itemsbreuvage': checklist_itemsbreuvage,
        'form1': form1,
        'checklist_items' : checklist_items,
        'md_photos' : md_photos,
        'recup_photos' : recup_photos,
        'checklist_documents' : checklist_documents,
    }
    return render(request, 'listings/checklistmd_detail.html', context)



from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def custom_login(request):
    print("Custom login view triggered!")  # Check if the view is being called
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(f"Logged in user: {user.username}")  # Confirm user is logged in

            # Debugging: print the user's groups
            print("User groups:", [group.name for group in user.groups.all()])

            # Check if user belongs to 'md' group
            if user.groups.filter(name='md').exists():
                print("User belongs to 'md' group, redirecting to faq...")
                return redirect('faq')
            else:
                print("User does not belong to 'md' group, redirecting elsewhere...")
                return redirect('journees-list')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})

    return render(request, 'listings/login.html')






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
    if not request.user.is_superuser:
        return redirect('unauthorized')
    
    return render(request, 'listings/partials/edit-livraison-formtoday.html', context)

def livraison_edit_formtoday(request, pk):
    livraison = Livraison.objects.get(id=pk)
    form = LivraisonDragFormtoday(instance=livraison)
    context = {'livraison': livraison, 'form': form}
    if not request.user.is_superuser:
        return redirect('unauthorized')
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
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return render(request, 'listings/partials/edit-livraison-form.html', context)

def livraison_edit_form(request, livraison_id):
    livraison = get_object_or_404(Livraison, id=livraison_id)
    form = LivraisonDragForm(instance=livraison)
    
    if request.method == 'POST':
        form = LivraisonDragForm(request.POST, instance=livraison)
        if form.is_valid():
            form.save()
            return render(request, 'listings/partials/livraison_row.html', {'livraison': livraison})

    # Render the partial template with the form
    if not request.user.is_superuser:
        return redirect('unauthorized')
    return render(request, 'listings/partials/livraison_edit_form.html', {'form': form, 'livraison': livraison})


def commentcamarche(request):
    context = {}
    if not request.user.is_superuser:
        return redirect('unauthorized')
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


from datetime import datetime, timedelta
from django.shortcuts import redirect

def duplicate_model(request, model_id):
    original_object = Livraison.objects.get(pk=model_id)
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    # Create a new Livraison object
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
    new_object.zipcode = original_object.zipcode
    new_object.app = original_object.app
    new_object.ligne2 = original_object.ligne2
    new_object.convives = original_object.convives
    new_object.num_commande = original_object.num_commande
    new_object.nom_client = original_object.nom_client
    new_object.contact_site = original_object.contact_site
    new_object.date = tomorrow
    new_object.heure_livraison = "recup"
    new_object.date_livraison = original_object.date_livraison
    new_object.statut = Route.objects.get(id=21)  # Ensure this is the correct route
    new_journee = Journee.objects.get(id=original_object.journee.id + 1)
    new_object.journee = new_journee
    new_object.lat = original_object.lat
    new_object.lng = original_object.lng
    new_object.place_id = original_object.place_id
    new_object.livreur = original_object.livreur

    # Save the new Livraison object first
    new_object.save()

    # Duplicate related Photo objects for the Livraison
    for photo_instance in original_object.livraison_photos.all():
        new_photo = Photo()
        new_photo.livraison = new_object  # Associate the new photo with the new Livraison
        new_photo.image = photo_instance.image  # Copy the image
        new_photo.caption = photo_instance.caption  # Copy the caption if available
        new_photo.save()
    

    
    print("Checklists to duplicate:", original_object.checklist_set.all())

    # Duplicate related Checklists
    for checklist in original_object.checklist_set.all():
        new_checklist = Checklist()
        new_checklist.name = checklist.name
        new_checklist.livraison = new_object  # Associate with the duplicated Livraison
        new_checklist.date = tomorrow  # Optionally set to tomorrow or keep original
        new_checklist.lieu = checklist.lieu
        new_checklist.num_contrat = checklist.num_contrat
        new_checklist.nb_convive = checklist.nb_convive
        new_checklist.heure_livraison = checklist.heure_livraison
        new_checklist.md = checklist.md
        new_checklist.status = checklist.status  # Keep the original status or reset if needed
        new_checklist.rapportmd = checklist.rapportmd
        new_checklist.rapportrecup = checklist.rapportrecup
        new_checklist.commentairevente = checklist.commentairevente
        new_checklist.notechecklist = checklist.notechecklist
        new_checklist.conseillere = None
        new_checklist.is_active = False
        new_checklist.save()
    
        # Duplicate ChecklistItems
        for item in checklist.checklistitem_set.all():
            new_item = ChecklistItem()
            new_item.checklist = new_checklist
            new_item.product = item.product
            new_item.quantity = item.quantity
            new_item.status = item.status
            new_item.save()

        for photo in checklist.checklistrecupphoto_set.all():
            new_photo = ChecklistRecupPhoto()
            new_photo.checklist = new_checklist
            new_photo.image = photo.image  # Copy the image
            new_photo.save()

    # Redirect back to a page or render a template
    return redirect('recuptoday')  # Redirect to a specific URL name
