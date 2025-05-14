from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import ChecklistItem, ChecklistItemChangeLog

@receiver(pre_delete, sender=ChecklistItem)
def log_checklist_item_deletion(sender, instance, **kwargs):
    # Log the deletion before the object is deleted
    ChecklistItemChangeLog.objects.create(
        checklist_item=instance,
        action='deleted',
        changed_by=None,  # Replace with actual user if needed
        previous_quantity=instance.quantity,
        previous_status=instance.status
    )

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ChecklistItem

@receiver(post_save, sender=ChecklistItem)
@receiver(post_delete, sender=ChecklistItem)
def update_checklist_status(sender, instance, **kwargs):
    checklist = instance.checklist
    checklist.update_status()


# signals.py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from listings.models import *

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not UserProfile.objects.filter(user=instance).exists():  # ✅ Prevent duplicates
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from listings.models import UserProfile

@receiver(user_logged_in)
def check_password_change(sender, request, user, **kwargs):
    if hasattr(user, 'userprofile') and user.userprofile.force_password_change:
        print(f"User {user.username} needs to change their password!")


@receiver(post_save, sender=Product)
def log_product_creation(sender, instance, created, **kwargs):
    if created:  # This checks if the product was just created
        user = None
        if hasattr(instance, '_current_user'):
            user = instance._current_user
        ProductLog.objects.create(product=instance, created_by=user)


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Livraison, LoadingDock

@receiver(post_save, sender=Livraison)
def associer_loading_docks_par_nom(sender, instance, created, **kwargs):
    print("Signal déclenché pour livraison id", instance.id)
    if created:
        nom_livraison = instance.nom
        print("Nom de livraison :", nom_livraison)
        docks = LoadingDock.objects.filter(name__icontains=nom_livraison)
        print("Docks trouvés :", docks.count())
        if docks.exists():
            print("Association en cours")
            instance.loading_docks.set(docks)
        else:
            print("Aucun dock trouvé à associer")


            
