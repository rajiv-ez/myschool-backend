# hr/models.py
from django.db import models

class Poste(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, null=True)
    description = models.TextField(blank=True)
    niveau_hierarchique = models.PositiveIntegerField(help_text="Plus le nombre est bas, plus le poste est élevé", default=0)
    est_direction = models.BooleanField(default=False)
    actif = models.BooleanField(default=True)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nom
    

class ClauseContrat(models.Model):
    titre = models.CharField(max_length=100)
    contenu = models.TextField()

    def __str__(self):
        return self.titre

class Contrat(models.Model):
    TYPES = [
        ('CDI', 'Contrat à durée indéterminée'),
        ('CDD', 'Contrat à durée déterminée'),
        ('STAGE', 'Stage'),
        ('VOLONTARIAT', 'Volontariat'),
    ]
    staff = models.OneToOneField('users.Staff', on_delete=models.CASCADE, related_name='contrat')
    type_contrat = models.CharField(max_length=20, choices=TYPES)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    avantages = models.TextField(blank=True)
    clauses = models.ManyToManyField(ClauseContrat, blank=True, related_name='contrats')

    def __str__(self):
        return f"Contrat {self.type_contrat} de {self.staff.user.nom}"

class Absence(models.Model):
    STATUTS = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('REFUSEE', 'Refusée'),
    ]
    staff = models.ForeignKey('users.Staff', on_delete=models.CASCADE, related_name='absences')
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField()
    justifiee = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, choices=STATUTS)

    def __str__(self):
        return f"Absence de {self.staff.user.nom} du {self.date_debut} au {self.date_fin}"

class Paie(models.Model):
    METHODES = [
        ('VIREMENT', 'Virement bancaire'),
        ('ESPECES', 'Espèces'),
        ('CHEQUE', 'Chèque'),
        ('MOBILE', 'Mobile Money'),
    ]
    STATUTS = [
        ('EN_ATTENTE', 'En attente'),
        ('PAYE', 'Payé'),
        ('ANNULE', 'Annulé'),
    ]
    staff = models.ForeignKey('users.Staff', on_delete=models.CASCADE, related_name='paies')
    mois = models.DateField()
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    primes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    retenues = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_a_payer = models.DecimalField(max_digits=10, decimal_places=2)
    date_versement = models.DateField(blank=True, null=True)
    methode_paiement = models.CharField(max_length=20, choices=METHODES)
    statut = models.CharField(max_length=20, choices=STATUTS)

    def __str__(self):
        return f"Paie de {self.staff.user.nom} - {self.mois.strftime('%B %Y')}"

class Pointage(models.Model):
    staff = models.ForeignKey('users.Staff', on_delete=models.CASCADE, related_name='pointages')
    date = models.DateField()
    heure_arrivee = models.TimeField(blank=True, null=True)
    heure_depart = models.TimeField(blank=True, null=True)
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return f"Pointage de {self.staff.user.nom} - {self.date}"

class PauseJournaliere(models.Model):
    pointage = models.ForeignKey(Pointage, on_delete=models.CASCADE, related_name='pauses')
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()


