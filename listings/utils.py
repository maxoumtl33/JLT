from .models import ItemInv, Inventory, Checklist

def add_quantity_to_checklist(item_id, quantity_to_add):
    item = ItemInv.objects.get(pk=item_id)

    # Retrieve or create a checklist item for the product
    checklist_item, created = Checklist.objects.get_or_create(item = item)

    # Add the specified quantity to the checklist
    checklist_item.quantity += quantity_to_add
    checklist_item.save()

    # Adjust inventory accordingly
    inventory, created = Inventory.objects.get_or_create(item=item)
    inventory.quantity += quantity_to_add
    inventory.save()

def remove_quantity_from_checklist(item_id, quantity_to_remove):
    item = ItemInv.objects.get(pk=item_id)

    try:
        # Retrieve checklist item for the product
        checklist_item = Checklist.objects.get(item=item)

        # Check if there's enough quantity in the checklist to remove
        if checklist_item.quantity >= quantity_to_remove:
            checklist_item.quantity -= quantity_to_remove
            checklist_item.save()

            # Adjust inventory accordingly
            inventory = Inventory.objects.get(item=item)
            inventory.quantity -= quantity_to_remove
            inventory.save()
        else:
            raise ValueError("Insufficient quantity in checklist to remove.")
    except Checklist.DoesNotExist:
        raise ValueError("No checklist item found for the product.")