from django.db import models

class FraisScolaire(models.Model):
    nom = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    classes = models.ManyToManyField('academic.Classe', related_name='frais_scolaires', blank=True, help_text="Sélectionnez les classes concernées par ce frais scolaire")
    concerne_toutes_classes = models.BooleanField(default=False, help_text="Indique si ce frais concerne toutes les classes de la session")
    session = models.ForeignKey('academic.Session', on_delete=models.CASCADE, related_name='frais_scolaires')
    palier = models.ForeignKey('academic.Palier', on_delete=models.CASCADE, related_name='frais_scolaires', blank=True, null=True)
    est_immateriel = models.BooleanField(default=False)
    est_obligatoire = models.BooleanField(default=True)
    est_actif = models.BooleanField(default=True)
    quantite = models.PositiveIntegerField(default=1)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    echeance = models.DateField(blank=True, null=True)
    date_creation = models.DateField(auto_now_add=True)

class FraisIndividuel(models.Model):
    STATUS_CHOICES = [
        ('EN_ATTENTE', 'En Attente'),
        ('PAYE_PARTIELLEMENT', 'Partiellement Payé'),
        ('PAYE', 'Payé'),
        ('ANNULE', 'Annullé'),
        ('REMBOURSE', 'Remboursé'),
    ]
    inscription = models.ForeignKey('academic.Inscription', on_delete=models.CASCADE, related_name='frais_individuels')
    frais = models.ForeignKey(FraisScolaire, on_delete=models.CASCADE, related_name='frais_individuels')
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    statut = models.CharField(max_length=50, choices=STATUS_CHOICES, default='EN_ATTENTE')
    date_creation = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('inscription', 'frais')
    
    def update_statut(self):
        total_verse = sum(v.montant for v in self.versements.all())
        if total_verse == 0:
            self.statut = 'EN_ATTENTE'
        elif total_verse < self.montant:
            self.statut = 'PARTIEL'
        else:
            self.statut = 'PAYE'
        self.save(update_fields=['statut'])

class Paiement(models.Model):  # ou VersementPaiement si renommage complet
    frais_individuel = models.ForeignKey(FraisIndividuel, on_delete=models.CASCADE, related_name='versements', null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    user_payeur = models.ForeignKey("users.User", on_delete=models.SET_NULL, blank=True, null=True)
    tiers_payeur = models.CharField(max_length=255, blank=True, null=True)
    methode_paiement = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Versement {self.montant} pour {self.frais_individuel}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.frais_individuel.update_statut()
        
class Depense(models.Model):
    CATEGORIES = [
        ('MATERIEL', 'Matériel'),
        ('MAINTENANCE', 'Maintenance'),
        ('SALAIRES', 'Salaires'),
        ('CHARGES', 'Charges'),
        ('TRANSPORT', 'Transport'),
        ('ALIMENTATION', 'Alimentation'),
        ('AUTRES', 'Autres'),
    ]
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    beneficiaire = models.CharField(max_length=255, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='AUTRES')

    def __str__(self):
        return f"Dépense de {self.montant} le {self.date}"
