from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError


class Domaine(models.Model):
    """Domaine d'enseignement"""
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class UniteEnseignement(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    domaines = models.ManyToManyField(Domaine, blank=True, related_name='unites_enseignement')

    def __str__(self):
        return self.nom

class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    unite = models.ForeignKey(UniteEnseignement, on_delete=models.CASCADE, related_name='matieres')
    coefficient = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class MatiereGroupee(models.Model):
    nom = models.CharField(max_length=25545)
    matieres = models.ManyToManyField(Matiere, related_name='groupes')

    def __str__(self):
        return self.nom

class Evenement(models.Model):
    TYPES = [
        ('COURS', 'Cours'),
        ('EVALUATION', 'Évaluation'),
        ('AUTRE', 'Autre'),
    ]
    titre = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPES)
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    palier = models.ForeignKey('academic.Palier', on_delete=models.CASCADE, related_name='evenements', null=True, blank=True)
    classe_session = models.ForeignKey('academic.ClasseSession', on_delete=models.CASCADE, related_name='evenements', null=True, blank=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='evenements')
    barreme = models.PositiveSmallIntegerField(default=20)
    description = models.TextField(blank=True)
    contenu = models.TextField(null=True, blank=True)
    correction = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.titre} ({self.type}) - {self.date}"

class FichierEvenement(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='fichiers')
    fichier = models.FileField(upload_to='teaching/fichiers/evenements/')

class Exercice(models.Model):
    nom = models.CharField(max_length=255)
    date = models.DateField()
    est_a_rendre = models.BooleanField(default=False)
    echeance = models.DateField(null=True, blank=True)
    contenu = models.TextField()
    correction = models.TextField(null=True, blank=True)
    evenement = models.ForeignKey(Evenement, on_delete=models.SET_NULL, null=True, blank=True, related_name='exercices')

    def __str__(self):
        return self.nom

class FichierExercice(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, related_name='fichiers')
    fichier = models.FileField(upload_to='teaching/fichiers/exercices/')

class Presence(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='presences')
    inscription = models.ForeignKey('academic.Inscription', on_delete=models.CASCADE, related_name='presences', null=True)
    present = models.BooleanField(default=True)
    retard = models.BooleanField(default=False)
    justification = models.TextField(blank=True)

    def __str__(self):
        return f"{self.eleve.user.nom} - {self.evenement.titre}"

class Note(models.Model):
    evaluation = models.ForeignKey(Evenement, on_delete=models.CASCADE, limit_choices_to={'type': 'EVALUATION'}, related_name='notes')
    inscription = models.ForeignKey('academic.Inscription', on_delete=models.CASCADE, related_name='notes')
    note = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Note {self.note}/{self.evaluation.barreme} - {self.inscription}"

class NoteConfig(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='configs')
    enseignant = models.ForeignKey('users.Staff', on_delete=models.SET_NULL, null=True, related_name='note_configs')
    classe_session = models.ForeignKey('academic.ClasseSession', on_delete=models.CASCADE, related_name='note_configs')
    formule = models.TextField(help_text="Expression Python à évaluer. Ex: (ds + tp + exam) / 3")

    def evaluer_formule(self, notes: dict) -> Decimal:
        try:
            # sécurité limitée - n'utiliser que des variables définies dans notes
            return eval(self.formule, {}, notes)
        except Exception as e:
            raise ValidationError(f"Erreur d'évaluation de la formule : {e}")
        
    def __str__(self):
        return f"Config {self.matiere.nom} - {self.classe_session}"
