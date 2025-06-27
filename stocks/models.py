from django.db import models

class CategorieArticle(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Article(models.Model):
    ETATS = [
        ('neuf', 'Neuf'),
        ('bon', 'Bon état'),
        ('utilise', 'Utilisé'),
        ('reparer', 'À réparer'),
        ('hors_service', 'Hors service')
    ]
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    categorie = models.ForeignKey(CategorieArticle, on_delete=models.CASCADE, related_name='articles')
    quantite = models.PositiveSmallIntegerField(default=1)
    seuil = models.PositiveSmallIntegerField(null=True, blank=True)
    etat = models.CharField(max_length=20, choices=ETATS)
    date_achat = models.DateField()
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nom

class DemandeActif(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('refusee', 'Refusée')
    ]
    demandeur = models.ForeignKey("users.Staff", on_delete=models.CASCADE, related_name='demandes_actifs')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='demandes')
    quantite = models.PositiveIntegerField()
    motif = models.TextField()
    date = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    motif_refus = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.article.nom} x{self.quantite} pour {self.demandeur.nom}"