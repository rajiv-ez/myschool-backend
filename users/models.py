
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENRE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    )
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    adresse = models.TextField()
    tel1 = models.CharField(max_length=20)
    tel2 = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='users/photos/', blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    objects = UserManager()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
   
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    poste = models.ForeignKey('hr.Poste', on_delete=models.SET_NULL, null=True, related_name='employees')
    date_embauche = models.DateField()
    statut = models.CharField(max_length=20, choices=[
        ('ACTIF', 'Actif'),
        ('CONGE', 'En congé'),
        ('SUSPENDU', 'Suspendu'),
        ('INACTIF', 'Inactif')
    ])
    domaines = models.ManyToManyField('teaching.Domaine', blank=True)
    niveaux = models.ManyToManyField('academic.Niveau', blank=True)

class Tuteur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tuteur')
    profession = models.CharField(max_length=100)

class Eleve(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='eleve')
    matricule = models.CharField(max_length=50)
    # classe_session = models.ForeignKey('academic.ClasseSession', on_delete=models.SET_NULL, null=True, blank=True)
    tuteurs = models.ManyToManyField(Tuteur, related_name='eleves', through='RelationEleveTuteur')

class RelationEleveTuteur(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='relations_tuteurs')
    tuteur = models.ForeignKey(Tuteur, on_delete=models.CASCADE, related_name='relations_eleves')
    relation = models.CharField(max_length=100)  # e.g., "Père", "Mère", "Tuteur légal"

    class Meta:
        unique_together = ('eleve', 'tuteur')  # Un élève ne peut avoir qu'une relation unique avec un tuteur
    