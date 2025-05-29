
from django.db import models

class Succursale(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    est_siege = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class Batiment(models.Model):
    succursale = models.ForeignKey(Succursale, on_delete=models.CASCADE, related_name='batiments')
    nom = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nom} ({self.succursale.nom})"

class Salle(models.Model):
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='salles')
    nom = models.CharField(max_length=255)
    capacite = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nom} - {self.batiment.nom}"