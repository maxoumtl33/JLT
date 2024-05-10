from django.db.models import Max
from .models import Livraison
from datetime import datetime, timedelta, time



def get_max_order() -> int:
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    existing_films = Livraison.objects.filter(date=tomorrow)
    if not existing_films.exists():
        return 1
    else:
        current_max = existing_films.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1

def reorder():
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    existing_films = Livraison.objects.filter(date=tomorrow)
    if not existing_films.exists():
        return
    number_of_films = existing_films.count()
    new_ordering = range(1, number_of_films+1)
    
    for order, user_film in zip(new_ordering, existing_films):
        user_film.order = order
        user_film.save()