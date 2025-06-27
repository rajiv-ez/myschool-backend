from django.db import models

class Livre(models.Model):
    CATEGORIES = [
        ('ROMAN', 'Roman'),
        ('CONTE', 'Conte'),
        ('FANTAISIE', 'Fantaisie'),
        ('JEUNESSE', 'Jeunesse'),
        ('SCIENCEFICTION', 'Science-fiction'),
        # Ajouter d'autres catégories si besoin
    ]
    ETATS = [
        ('NEUF', 'Neuf'),
        ('BON', 'Bon état'),
        ('USE', 'Usé'),
        ('ABIME', 'Abîmé'),
    ]
    DISPONIBILITE = [
        ('DISPONIBLE', 'Disponible'),
        ('EMPRUNTE', 'Emprunté'),
        ('RUPTURE', 'Rupture'),
    ]

    titre = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='livres/images/', null=True, blank=True)
    auteur = models.CharField(max_length=255)
    maison_edition = models.CharField(max_length=255, null=True, blank=True)
    date_publication = models.DateField(null=True, blank=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='ROMAN')
    etat = models.CharField(max_length=10, choices=ETATS)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    disponibilite = models.CharField(max_length=20, choices=DISPONIBILITE, default='DISPONIBLE')

    def __str__(self):
        return f"{self.titre} ({self.auteur})"
    
class Emprunt(models.Model):
    STATUTS = [
        ('EN_COURS', 'En cours'),
        ('RENDU', 'Rendu'),
        ('EN_RETARD', 'En retard'),
    ]
    STATUT_PENALITE = [
        ('AUCUNE', 'Aucune'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('DEPASSE', 'Dépassé'),
        ('PROLONGE', 'Prolongé'),
    ]

    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='emprunts')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='emprunts')
    debut = models.DateField()
    fin_prevue = models.DateField()
    fin_reelle = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_COURS')
    prolongation = models.PositiveSmallIntegerField(default=0, null=True, blank=True, help_text="Nombre de jours pde prolongation")
    hist_prolongation = models.CharField(max_length=255, null=True, blank=True, help_text="Toutes les prolongation, séparées d'une virgule")
    penalite = models.TextField(blank=True, null=True)
    echeance_penalite = models.PositiveSmallIntegerField(default=0, null=True, blank=True, help_text="Nombre de jours pour régler la pénalité")
    statut_penalite = models.CharField(max_length=20, choices=STATUT_PENALITE, default='AUCUNE')

    def __str__(self):
        return f"{self.livre.titre} emprunté par {self.user.email}"

