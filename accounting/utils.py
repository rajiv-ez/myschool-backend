from decimal import Decimal
from accounting.models import FraisScolaire, Paiement, FraisIndividuel
from django.db.models import Q

def creer_paiements_pour_inscription(inscription):
    """
    Crée des paiements pour les frais scolaires associés à une inscription.
    Cette fonction vérifie les frais scolaires actifs pour la session de l'inscription 
    et la classe de l'inscription, puis crée un paiement
    """
    session = inscription.classe_session.session
    classe = inscription.classe_session.classe
    #palier = getattr(inscription.classe_session.classe.specialite.filiere.session, 'palier', None)

    frais_concernes = FraisScolaire.objects.filter(
        session=session,
        est_actif=True
    ).filter(
        Q(concerne_toutes_classes=True) |
        Q(classes=classe)
        # | Q(palier=palier)
    ).distinct()

    for frais in frais_concernes:
        # Évite les doublons
        if Paiement.objects.filter(inscription=inscription, frais=frais).exists():
            continue

        #montant_total = Decimal(frais.montant) * frais.quantite

        Paiement.objects.create(
            inscription=inscription,
            frais=frais,
            #montant=montant_total,
            montant=frais.montant,
            statut='EN_ATTENTE'
        )


def creer_frais_pour_inscription(inscription):
    session = inscription.classe_session.session
    classe = inscription.classe_session.classe
    # palier = getattr(inscription.classe_session.classe.specialite.filiere.session, 'palier', None)

    frais = FraisScolaire.objects.filter(
        session=session,
        est_actif=True
    ).filter(
        Q(concerne_toutes_classes=True) |
        Q(classes=classe)
        # | Q(palier=palier)
    ).distinct()

    for f in frais:
        if not FraisIndividuel.objects.filter(inscription=inscription, frais=f).exists():
            montant_total = f.quantite * f.montant
            FraisIndividuel.objects.create(inscription=inscription, frais=f, montant=montant_total)
