# plus simple :  faire : python manage.py shell 
# et commencer à partir de la ligne from institutions.models import Client, Domain

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myschool_backend.settings")
django.setup()

from institutions.models import Client, Domain

client = Client(schema_name='csleguide', name='Le Guide de nos enfants')
client.save()

domain = Domain(domain='csleguide.localhost', tenant=client, is_primary=True)
domain.save()

print("Tenant créé avec succès.")