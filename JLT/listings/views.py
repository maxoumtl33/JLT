from django.http import HttpResponse
from django.shortcuts import render, redirect
from listings.models import Livraison
from .models import Livreur
from .models import Tacheafaire
from .models import Journee
from .models import Route
from .forms import LivraisonForm
from tablib import Dataset
from .ressources import LivraisonResource
from django.utils.timezone import now
from datetime import datetime, timedelta, time
from .models import Recuperation

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
   livreur = Livreur.objects.all()
   journee = Journee.objects.all()
   recuperation = "oui"
   form = LivraisonForm(request.POST or None, instance=livraison)
   if form.is_valid():
       form.save()

       
       
     
   return render(request,
          'listings/livraison_detail.html',
          context={'livraison': livraison, 'livreur':livreur, 'recuperation': recuperation, 'form': form, 'journee':journee,}) # nous passons l'id au modèle

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

