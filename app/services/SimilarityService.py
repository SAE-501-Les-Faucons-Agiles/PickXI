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
