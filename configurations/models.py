from django.db import models
from django.utils import timezone

class Annonce(models.Model):
    CATEGORIES = [
        ('INFO', 'Information'),
        ('ALERTE', 'Alerte'),
        ('EVENEMENT', 'Évènement'),
    ]

    ETATS = [
        ('BROUILLON', 'Brouillon'),
        ('A_VALIDER', 'À valider'),
        ('PUBLIE', 'Publié'),
    ]

    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='INFO')
    etat = models.CharField(max_length=20, choices=ETATS, default='BROUILLON')
    cible_global = models.BooleanField(default=True)
    classes = models.ManyToManyField('academic.ClasseSession', blank=True)
    visible_depuis = models.DateTimeField(default=timezone.now)
    visible_jusquau = models.DateTimeField(null=True, blank=True)
    publie_par = models.ForeignKey('users.Staff', null=True, blank=True, on_delete=models.SET_NULL, related_name='annonces_publiees')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.etat}] {self.titre}"

    class Meta:
        ordering = ['-date_creation']

class LuParAnnonce(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='lus')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='annonces_lues')
    date_lecture = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('annonce', 'user')

class PreferenceUser(models.Model):
    THEME_CHOICES = [('light', 'Clair'), ('dark', 'Sombre'), ('system', 'Système')]
    COULEUR_CHOICES = [('purple', 'Violet'), ('blue', 'Bleu'), ('green', 'Vert'), ('orange', 'Orange'), ('red', 'Rouge'), ('pink', 'Rose')]
    DISPOSITION_CHOICES = [('tabs', 'Onglets'), ('sidebar', 'Barre latérale')]

    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    couleur = models.CharField(max_length=10, choices=COULEUR_CHOICES, default='violet')
    disposition = models.CharField(max_length=10, choices=DISPOSITION_CHOICES, default='tabs')

    def __str__(self):
        return f"Préférences de {self.user.email}"

# ConfigurationClasse, DispositionClasse, Place models

class ConfigurationClasse(models.Model):
    nom = models.CharField(max_length=255)
    classe_session = models.ForeignKey('academic.ClasseSession', on_delete=models.CASCADE, related_name='configurations')
    nb_rangees = models.PositiveSmallIntegerField()
    nb_lignes_par_rangee = models.PositiveSmallIntegerField()
    nb_places_par_ligne = models.PositiveSmallIntegerField()
    est_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} ({'active' if self.est_active else 'inactive'})"

class DispositionClasse(models.Model):
    configuration = models.ForeignKey(ConfigurationClasse, on_delete=models.CASCADE, related_name='dispositions')
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    est_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} ({'active' if self.est_active else 'inactive'})"

class Place(models.Model):
    disposition = models.ForeignKey(DispositionClasse, on_delete=models.CASCADE, related_name='places')
    rangee = models.PositiveSmallIntegerField()
    ligne = models.PositiveSmallIntegerField()
    place = models.PositiveSmallIntegerField()
    inscription = models.ForeignKey('academic.Inscription', on_delete=models.CASCADE)

    def __str__(self):
        return f"R{self.rangee}-L{self.ligne}-P{self.place}"

class DemandeChangementPlace(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='demandes_places')
    inscription = models.ForeignKey('academic.Inscription', on_delete=models.CASCADE, related_name='demandes_places')
    date_demande = models.DateTimeField(auto_now_add=True)
    date_reponse = models.DateTimeField(auto_now=True)
    motif = models.TextField()
    raison_refus = models.TextField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')

    def __str__(self):
        return f"Demande de changement de {self.user} pour {self.inscription.eleve}"
    
