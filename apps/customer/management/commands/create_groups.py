from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create required user groups'

    def handle(self, *args, **kwargs):
        group_names = ['admin', 'supervisor', 'data_entry', 'customer']
        # Group.objects.deleteAll()
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Group '{group_name}' created.")
            else:
                self.stdout.write(f"Group '{group_name}' already exists.")
