from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User  # Import your custom User model


@receiver(post_save, sender=User)
def add_to_customer_group(sender, instance, created, **kwargs):
    if created:  # Only for newly created users
        try:
            # Get or create the "Customer" group
            customer_group, _ = Group.objects.get_or_create(name='customer')

            # Add the user to the group
            instance.groups.add(customer_group)
        except Exception as e:
            # Log the exception or handle it as needed
            print(f"Error assigning user to Customer group: {e}")