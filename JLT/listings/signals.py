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