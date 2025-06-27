from rest_framework.permissions import BasePermission
from .models import FraisScolaire, Paiement

class IsTuteur(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'tuteur')

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, FraisScolaire):
            enfants = request.user.tuteur.eleves.all()
            if obj.concerne_toutes_classes:
                return obj.session in request.user.tuteur.sessions.all()
            elif obj.classes.exists():
                return obj.classes.filter(inscriptions__eleve__in=enfants).exists()
            else:
                # If no specific classes are set, check if the tuteur has children in the session
                return obj.session in request.user.tuteur.sessions.all()
            classes_session = [classe.instances for classe in obj.classes.all()]
            return obj.classe_session.inscriptions.filter(eleve__in=enfants).exists()
        elif isinstance(obj, Paiement):
            return (obj.tuteur == request.user.tuteur or obj.nom_payeur is not None)