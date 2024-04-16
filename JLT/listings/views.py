from django.http import HttpResponse
from django.shortcuts import render, redirect
from listings.models import Livraison
from .models import Livreur
from .models import Tacheafaire
from .models import Journee
from .models import Distances
from .forms import LivraisonForm
from .forms import DistanceForm
from tablib import Dataset
from .ressources import LivraisonResource
from django.utils.timezone import now
from datetime import datetime, timedelta, time
from .models import Recuperation
import googlemaps
from django.conf import settings
from django.views import View
from datetime import datetime

from django.http import FileResponse, HttpResponseRedirect, HttpResponse


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

def journees_list(request):
    livraisons  = Livraison.objects.all()
    livreurs = Livreur.objects.all()
    journees = Journee.objects.all()
    return render(request, 'listings/journees_list.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journees' : journees})

def livraison_detail(request, ip):  # notez le paramètre id supplémentaire
   livraison = Livraison.objects.get(id=ip)
   adresse = Livraison.adress
   livreur = Livreur.objects.all()
   journee = Journee.objects.all()
   recuperation = "oui"
   form = LivraisonForm(request.POST or None, instance=livraison)
   gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
   result = gmaps.geocode(adresse)
   if form.is_valid():
       form.save()
       
   return render(request,
          'listings/livraison_detail.html',
          context={'livraison': livraison, 'livreur':livreur, 'recuperation': recuperation, 'form': form, 'journee':journee, 'result':result,'adresse': adresse}) # nous passons l'id au modèle

def recuperation_detail(request, id):  # notez le paramètre id supplémentaire
   recuperations = Recuperation.objects.get(id=id)
   livreurs = Livreur.objects.all()
   livraisons = Livraison.objects.all()
   return render(request,
          'listings/recup_detail.html',
          context={'livraisons': livraisons, 'livreurs':livreurs, 'recuperations':recuperations}) # nous passons l'id au modèle

def journee_detail(request, id):  # notez le paramètre id supplémentaire
   journees = Journee.objects.get(id=id)
   livreurs = Livreur.objects.all()
   livraisonsroute  = Livraison.objects.order_by('route')
   today = now().date()
   livraisons = Livraison.objects.order_by('route').filter(date=today)
   recuperations = Recuperation.objects.all()
   retourtraiteur = "oui"
   retourtraiteurno = "non"
   recuperation = "oui"
   recuperationo = "non"
   
   return render(request,
          'listings/journee_detail.html',
          context={'journees': journees ,'livraisonsroute': livraisonsroute, 'livreurs':livreurs, 'recuperations' : recuperations,'retourtraiteur' : retourtraiteur,'recuperation' : recuperation,'retourtraiteurno': retourtraiteurno,'livraisons' : livraisons, 'recuperationo':recuperationo }) # nous passons l'id au modèle


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
    
def dashboard(request, pk, id):  # notez le paramètre id supplémentaire
    if request.user.is_authenticated :
        livreur = Livreur.objects.get(user_id= pk)
        today = now().date()
        livraisons = Livraison.objects.order_by('route').filter(date=today)
        taches = Tacheafaire.objects.all()
        journee = Journee.objects.get(id=id)
        recuperation = "oui"
        countlivraisonok = Livraison.objects.filter(status=True)
        
       
        
        return render(request, "listings/dashboard.html", context={'livreur':livreur,
                                                                'livraisons' : livraisons,
                                                                'taches' : taches,
                                                                'recuperation' : recuperation,
                                                                'journee' : journee,
                                                                'countlivraisonok' : countlivraisonok,
                                                                
                                                                
                                                                

                                                                })
    else:
        return redirect('home')
    
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
    tomorrow = today + timedelta(1)
    livraisons  = Livraison.objects.order_by('route').filter(date=tomorrow)
    livreurs = Livreur.objects.all()
    journee = Journee.objects.get(id=id)
    recuperation = "oui"
    return render(request, 'listings/responsables.html', context={'livraisons': livraisons,
                                                              'livreurs': livreurs,
                                                              'journee' : journee,
                                                              'recuperation' : recuperation,})




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
       

class MapView(View):
    def get(self, request):
        key = settings.GOOGLE_API_KEY
        eligable_locations = Livraison.objects.filter(place_id_isnull=False)
        context = {'key': key

        }
        return render(request, 'listings/map.html', context)
    


def deleteDistance(request, pk):
    distance = Distances.objects.get(id= pk)
    if request.method == 'POST':
        distance.delete()
        return redirect('my_distance_view')

    context = {'distance':distance}
    return render(request, 'listings/deletedistance.html', context)
