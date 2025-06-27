# dms/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TypeArchive(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    nom_modele = models.CharField(max_length=255, help_text="Nom du modèle lié, ex: 'Inscription'")
    app_label = models.CharField(max_length=255, help_text="Nom de l'app du modèle lié, ex: 'academic.Inscription'")
    champs_affichage = models.JSONField(
        default=list,
        help_text="Liste des champs à afficher pour les filtres, ex: ['classe_session', 'eleve', 'session']"
    )

    def __str__(self):
        return self.nom

class Archive(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type_archive = models.ForeignKey(TypeArchive, on_delete=models.CASCADE, related_name='archives')
    objet_id = models.PositiveIntegerField(help_text="ID de l'instance du modèle archivé")
    fichier = models.FileField(upload_to='archives/files/')  # pour les fichiers multiples, utiliser un autre modèle lié
    tags = models.CharField(max_length=500, blank=True, help_text="Mots clés séparés par des virgules")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archives_crees')
    modifie_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archives_modifiees')

    def __str__(self):
        return f"{self.type_archive.nom} #{self.objet_id}"  


class ModeleDocument(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    template = models.FileField(upload_to='dms/documents/templates/', blank=True, null=True)

    def __str__(self):
        return self.nom

class ChampsModele(models.Model):
    TYPE_CHOICES = [
        ('char', 'Texte court'),
        ('text', 'Texte long'),
    ]
    modele_document = models.ForeignKey(ModeleDocument, on_delete=models.CASCADE, related_name='champs')
    label = models.CharField(max_length=255)
    tag_name = models.CharField(max_length=255, null=True, help_text="Nom du tag qui sera utilisé dans le template word pour génération avec python-docx")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    options = models.TextField(blank=True, null=True, help_text="Options possibles séparées par des points-virgules")
    help_text = models.CharField(max_length=255, blank=True, null=True)
    required = models.BooleanField(default=True)

    def __str__(self):
        return f'Champs "{self.label}" ({self.modele_document.nom})'


class DocumentGenere(models.Model):
    modele = models.ForeignKey(ModeleDocument, on_delete=models.CASCADE, related_name='documents')
    donnees = models.JSONField(help_text="Données remplies pour chaque champ")
    fichier_genere = models.FileField(upload_to='dms/documents/generated/', blank=True, null=True)
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='documents_generes')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.modele.nom} généré(e) le {self.date_creation.date()}"
