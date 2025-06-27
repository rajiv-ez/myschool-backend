from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import (
    Domaine, UniteEnseignement, Matiere, MatiereGroupee, 
    Evenement, FichierEvenement, Presence, Exercice, 
    FichierExercice, Note, NoteConfig
)

from academic.models import Inscription
from .serializers import (
    DomaineSerializer, UniteEnseignementSerializer, MatiereSerializer, MatiereGroupeeSerializer,
    EvenementSerializer, FichierEvenementSerializer, PresenceSerializer, ExerciceSerializer,
    FichierExerciceSerializer, NoteSerializer, NoteConfigSerializer
)
from django_filters.rest_framework import DjangoFilterBackend

class DomaineViewSet(viewsets.ModelViewSet):
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer

class UniteEnseignementViewSet(viewsets.ModelViewSet):
    queryset = UniteEnseignement.objects.all()
    serializer_class = UniteEnseignementSerializer

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['unite', ]

class MatiereGroupeeViewSet(viewsets.ModelViewSet):
    queryset = MatiereGroupee.objects.all()
    serializer_class = MatiereGroupeeSerializer

class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'palier', 'classe_session', 'matiere']

class FichierEvenementViewSet(viewsets.ModelViewSet):
    queryset = FichierEvenement.objects.all()
    serializer_class = FichierEvenementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['evenement']

class ExerciceViewSet(viewsets.ModelViewSet):
    queryset = Exercice.objects.all()
    serializer_class = ExerciceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['evenement']

class FichierExerciceViewSet(viewsets.ModelViewSet):
    queryset = FichierExercice.objects.all()
    serializer_class = FichierExerciceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exercice']

class PresenceViewSet(viewsets.ModelViewSet):
    queryset = Presence.objects.all()
    serializer_class = PresenceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['evenement', 'inscription']

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['evaluation', 'inscription']

class NoteConfigViewSet(viewsets.ModelViewSet):
    queryset = NoteConfig.objects.all()
    serializer_class = NoteConfigSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['matiere', 'enseignant', 'classe_session']


# vues utiles

def grouper_notes_par_matiere(notes, classe_session):
    """Regroupe les notes par matière pour un relevé de notes."""
    grouped = {}
    for note in notes:
        matiere = note.evaluation.matiere
        mat_name = matiere.nom
        config = NoteConfig.objects.filter(matiere=matiere, classe_session=classe_session).first()

        if mat_name not in grouped:
            grouped[mat_name] = {'notes': {}, 'values': [], 'coefficient': matiere.coefficient, 'config': config}

        key = f"eval{note.evaluation.pk}"
        note_value = float(note.note)  #(float(note.note) / float(note.evaluation.barreme)) * 20 # pour avoir une note sur 20
        grouped[mat_name]['notes'][key] = note_value
        grouped[mat_name]['values'].append(note_value)

    return grouped

def calculer_moyenne_par_matiere(dict_notes_par_matiere):
    """Calcule la moyenne pour chaque matière en fonction de la configuration.
    Renvoie un tuple (moyennes, total_points, total_coeffs)."""
    moyennes = {}
    total_points = 0
    total_coeffs = 0
    for mat, content in dict_notes_par_matiere.items():
        config = content['config']
        coef = float(content['coefficient'])
        if config:
            try:
                moy = float(config.evaluer_formule(content['notes']))
            except ValidationError as e:
                moy = 0  # ou gérer différemment les erreurs
        else:
            moy = sum(content['values']) / len(content['values'])

        moyennes[mat] = round(moy, 2)
        total_points += moy * coef
        total_coeffs += coef

    return moyennes, total_points, total_coeffs

class ReleveBulletinViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='releve')
    def releve(self, request):
        inscription_id = request.query_params.get('inscription_id')
        palier_id = request.query_params.get('palier_id')
        if not inscription_id or not palier_id:
            return Response({'error': 'inscription_id et palier_id requis'}, status=status.HTTP_400_BAD_REQUEST)

        inscription = Inscription.objects.select_related('eleve', 'classe_session').get(pk=inscription_id)
        notes = Note.objects.filter(inscription=inscription, evaluation__palier_id=palier_id)

        grouped = grouper_notes_par_matiere(notes, inscription.classe_session)

        if not grouped:
            return Response({'error': 'Aucune note trouvée pour cette inscription et ce palier'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calcul des moyennes par matière et moyenne générale
        moyennes, total_points, total_coeffs = calculer_moyenne_par_matiere(grouped)
        
        moyenne_generale = round(total_points / total_coeffs, 2) if total_coeffs else 0

        return Response({
            'moyennes': moyennes,
            'moyenne_generale': moyenne_generale
        })

    @action(detail=False, methods=['get'], url_path='bulletin')
    def bulletin(self, request):
        inscription_id = request.query_params.get('inscription_id')
        palier_id = request.query_params.get('palier_id')
        if not inscription_id or not palier_id:
            return Response({'error': 'inscription_id et palier_id requis'}, status=status.HTTP_400_BAD_REQUEST)

        inscription = Inscription.objects.select_related('eleve', 'classe_session').get(pk=inscription_id)
        notes = Note.objects.filter(inscription=inscription, evaluation__palier_id=palier_id)

        grouped = {}
        for note in notes:
            matiere = note.evaluation.matiere
            unite = matiere.unite
            groupees = matiere.groupes.all()
            matiere_key = matiere.nom
            unite_key = unite.nom

            config = NoteConfig.objects.filter(matiere=matiere, classe_session=inscription.classe_session).first()

            if unite_key not in grouped:
                grouped[unite_key] = {'matieres': {}, 'total_coef': 0, 'total_note': 0}

            if matiere_key not in grouped[unite_key]['matieres']:
                grouped[unite_key]['matieres'][matiere_key] = {
                    'notes': {}, 'values': [], 'coefficient': matiere.coefficient, 'config': config
                }

            key = f"eval{note.evaluation.pk}"
            note_value = float(note.note)
            grouped[unite_key]['matieres'][matiere_key]['notes'][key] = note_value
            grouped[unite_key]['matieres'][matiere_key]['values'].append(note_value)

        bulletin = {}
        total_points = 0
        total_coeffs = 0

        for unite, udata in grouped.items():
            unite_total = 0
            unite_coef = 0
            matieres_data = {}

            for mat, content in udata['matieres'].items():
                coef = float(content['coefficient'])
                moy = 0
                if content['config']:
                    try:
                        moy = float(content['config'].evaluer_formule(content['notes']))
                    except:
                        pass
                else:
                    moy = sum(content['values']) / len(content['values'])

                matieres_data[mat] = round(moy, 2)
                unite_total += moy * coef
                unite_coef += coef

            moyenne_unite = round(unite_total / unite_coef, 2) if unite_coef else 0
            bulletin[unite] = {
                'matieres': matieres_data,
                'moyenne_unite': moyenne_unite,
                'total_coef': unite_coef,
                'total_note': unite_total
            }

            total_points += unite_total
            total_coeffs += unite_coef

        moyenne_generale = round(total_points / total_coeffs, 2) if total_coeffs else 0

        return Response({
            'bulletin': bulletin,
            'moyenne_generale': moyenne_generale
        })


# Exemple NoteConfig:
# formule = "(eval1 + (eval2 + eval3)/2 + eval4*2)/3"
# valeurs: eval1=12, eval2=6, eval3=7, eval4=14 ➜ moyenne: 14.0

# Exemple d'utilisation pratique de NoteConfig.evaluer_formule :
# Config existante avec formule = '(ds + tp + exam) / 3'
# Appel depuis code métier :
# config = NoteConfig.objects.get(id=1)
# notes_dict = {'ds': 14, 'tp': 12, 'exam': 16}
# moyenne = config.evaluer_formule(notes_dict)  # retourne Decimal(14.0)
