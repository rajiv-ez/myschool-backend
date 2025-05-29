from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Client(TenantMixin):
    CATEGORIES = (
        ('PREPRIMAIRE', 'Pré-primaire'),
        ('PRIMAIRE', 'primaire'),
        ('COLLEGE', 'collège'),
        ('LYCEE', 'lycée'),
        ('FORMATION', 'Ecole de formation'),
        ('UNIVERSITE', 'Université'),
    )
    TYPES = (
        ('PUBLIC', 'Public'),
        ('PRIVE', 'Privé'),
        ('PARPUBLIC', 'Parapublic'),
    )
    name = models.CharField(max_length=100)

    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='ECOLE')
    type = models.CharField(max_length=20, choices=TYPES, default='PUBLIC')
    adresse = models.TextField(blank=True)
    tel = models.CharField(max_length=20, blank=True)
    tel2 = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)

    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass