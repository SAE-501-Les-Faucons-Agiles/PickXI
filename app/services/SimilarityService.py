#SimilarityService — Machine Learning

#scikit-learn(outil pour recommander des joueur avec similarite) compare les statistiques des 
# joueurs au profil recherché : vitesse, dribble, finition, etc.

#il renvoie les profils les plus proches.


# SimilarityService — Machine Learning (KNN)
#
# ALGORITHME : NearestNeighbors (scikit-learn)
#
# NearestNeighbors est un algorithme de recherche des
# K plus proches voisins (KNN), sans apprentissage supervisé.
#
# PRINCIPE :
# 1. Le LLM comprend la demande de l'utilisateur et extrait
#    les qualités recherchées (vitesse, dribble, tir, etc.).
#
# 2. Le DAO récupère les joueurs dans SQLite en respectant
#    les contraintes : poste, âge et budget.
#
# 3. On transforme les statistiques des joueurs en vecteurs
#    numériques (exemple : [88, 90] = vitesse et dribble).
#
# 4. On construit un profil idéal selon les qualités demandées
#    (exemple : [100, 100] pour vitesse et dribble).
#
# 5. NearestNeighbors calcule la distance euclidienne entre
#    chaque joueur et le profil idéal.
#
# 6. L'algorithme retourne les 5 joueurs les plus proches
#    du profil idéal, donc les plus adaptés à la demande.
#
# OBJECTIF :
# Recommander les 5 joueurs correspondant le mieux aux
# qualités recherchées, en utilisant leurs statistiques FC26.
#
# IMPORTANT :
# Plus la distance est faible, meilleure est la correspondance.
# Le modèle ne prédit pas les performances : il compare
# les profils à partir des données existantes.
from sklearn.neighbors import NearestNeighbors

QUALITES_STATS = {
    "vitesse": "pace",
    "tir": "shooting",
    "passe": "passing",
    "dribble": "dribbling",
    "défense": "defending",
    "physique": "physicality"
}


def calculer_score(joueur, qualites):

    scores = []

    for qualite in qualites:

        
        statistique = QUALITES_STATS[qualite]

        
        valeur = getattr(joueur, statistique, 0) or 0  # Utiliser 0 si l'attribut n'existe pas

        
        scores.append(valeur)
        

    
    moyenne = sum(scores) / len(scores) if scores else 0
    return moyenne


def classer_joueurs(joueurs, qualites):

    joueurs_tries = sorted(
        joueurs,
        key=lambda joueur: calculer_score(joueur, qualites),
        reverse=True
    )

    return joueurs_tries


def construire_vecteurs(joueurs, qualites):

    vecteurs = []

    for joueur in joueurs:

        vecteur = []

        for qualite in qualites:

            statistique = QUALITES_STATS[qualite]

            valeur = getattr(joueur, statistique, 0) or 0

            vecteur.append(valeur)

        vecteurs.append(vecteur)

    return vecteurs


from sklearn.neighbors import NearestNeighbors


def classer_joueurs_knn(joueurs, qualites):

    if not joueurs or not qualites:
        return []

    # 1. Identifier les statistiques demandées
    statistiques = [
        QUALITES_STATS[qualite]
        for qualite in qualites
    ]

    # 2. Exclure les joueurs avec des stats manquantes
    joueurs_valides = [
        joueur for joueur in joueurs
        if all(
            getattr(joueur, stat, None) is not None
            for stat in statistiques
        )
    ]

    if not joueurs_valides:
        return []

    # 3. Transformer les joueurs valides en vecteurs
    vecteurs = construire_vecteurs(
        joueurs_valides,
        qualites
    )

    # 4. Construire le profil idéal
    profil_ideal = [[100] * len(qualites)]

    # 5. Créer et préparer KNN
    knn = NearestNeighbors(
        n_neighbors=min(5, len(joueurs_valides)),
        metric="euclidean"
    )

    knn.fit(vecteurs)

    # 6. Rechercher les joueurs les plus proches
    distances, indices = knn.kneighbors(profil_ideal)

    # 7. Récupérer les joueurs correspondants
    recommandations = []

    for indice, distance in zip(
        indices[0],
        distances[0]
    ):
        # IMPORTANT : même liste que celle des vecteurs
        joueur = joueurs_valides[int(indice)]

        print(
            f"{joueur.name} | Distance KNN : {distance:.2f}"
        )

        recommandations.append(joueur)

    return recommandations
