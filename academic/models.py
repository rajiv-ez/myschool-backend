from django.db import models

class Session(models.Model):
    nom = models.CharField(max_length=255)
    debut = models.DateField()
    fin = models.DateField()
    en_cours = models.BooleanField(default=False)
    auto_activer_palier = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class Palier(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='paliers')
    nom = models.CharField(max_length=255)
    debut = models.DateField()
    fin = models.DateField()
    en_cours = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} ({self.session.nom})"

class Niveau(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class Filiere(models.Model):
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='filieres')
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nom} ({self.niveau.nom})"

class Specialite(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='specialites')
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nom} ({self.filiere.nom})"

class Classe(models.Model):
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, related_name='classes')
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class ClasseSession(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='instances')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='classes')
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    capacite = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom

class Inscription(models.Model):
    eleve = models.ForeignKey('users.Eleve', on_delete=models.CASCADE, related_name='inscriptions')
    classe_session = models.ForeignKey('ClasseSession', on_delete=models.CASCADE, related_name='inscriptions')
    date_inscription = models.DateField(auto_now_add=True)
    est_reinscription = models.BooleanField(default=False)
    decision_conseil = models.CharField(max_length=255, blank=True, null=True)  # ex: "Redoublement", "Passage"
    motif_reinscription = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=50, choices=[
        ('CONFIRMEE', 'Confirmée'),
        ('EN_ATTENTE', 'En attente'),
        ('ANNULEE', 'Annulée'),
    ], default='EN_ATTENTE')

    def __str__(self):
        return f"{self.eleve.user.nom} {self.classe_session.nom} ({self.date_inscription})"

