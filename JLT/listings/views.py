from django.http import HttpResponse
from django.shortcuts import render, redirect
from listings.models import Livraison
from .models import Livreur
from .models import Tacheafaire
from .models import Journee
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

def livraison_detail(request, id):  # notez le paramètre id supplémentaire
   livraison = Livraison.objects.get(id=id)
   livreur = Livreur.objects.all()
   return render(request,
          'listings/livraison_detail.html',
          context={'livraison': livraison, 'livreur':livreur}) # nous passons l'id au modèle

def recuperation_detail(request, id):  # notez le paramètre id supplémentaire
   recuperations = Recuperation.objects.get(id=id)
   livreurs = Livreur.objects.all()
   livraisons = Livraison.objects.all()
   return render(request,
          'listings/recup_detail.html',
          context={'livraisons': livraisons, 'livreurs':livreurs, 'recuperations':recuperations}) # nous passons l'id au modèle

def journee_detail(request, id):  # notez le paramètre id supplémentaire
   journee = Journee.objects.get(id=id)
   livreurs = Livreur.objects.all()
   livraisons  = Livraison.objects.all()
   recuperations = Recuperation.objects.all()
   
   return render(request,
          'listings/journee_detail.html',
          context={'journee': journee ,'livraisons': livraisons, 'livreurs':livreurs, 'recuperations' : recuperations}) # nous passons l'id au modèle


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
        livraisons  = Livraison.objects.all()
        taches = Tacheafaire.objects.all()
        recuperations = Recuperation.objects.all()
        journee = Journee.objects.get(id=id)
        return render(request, "listings/dashboard.html", context={'livreur':livreur,
                                                                'livraisons' : livraisons,
                                                                'taches' : taches,
                                                                'recuperations' : recuperations,
                                                                'journee' : journee})
    else:
        return redirect('home')