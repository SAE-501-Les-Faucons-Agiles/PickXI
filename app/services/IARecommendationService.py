#Coordonne les étapes : LLM → DAO → similarité → résultat

#on ne cree pas un llm de zero car trop long et couteux, on Ollana et llama qui s
# ont des llms pour comprendre les dmds du user.


# Coordination : LLM → DAO → KNN → Explications

from app.services.LLMService import (
    extraire_criteres,
    expliquer_recommandations
)

from app.services.SimilarityService import classer_joueurs_knn
from app.models.PlayerDAO import PlayerSqliteDAO


def recommander(description: str, avec_explications=True):

    # 1. Comprendre la demande utilisateur
    criteres = extraire_criteres(description)

    # 2. Récupérer les joueurs dans la base de données
    dao = PlayerSqliteDAO()

    joueurs = dao.findByCriteria(
        edition="FC26",
        position=criteres.position,
        max_age=criteres.max_age,
        max_budget=criteres.max_budget
    )

    # 3. Filtrer selon l'âge minimum
    if criteres.min_age is not None:
        joueurs = [
            joueur for joueur in joueurs
            if joueur.age is not None
            and joueur.age >= criteres.min_age
        ]

    # 4. Filtrer selon le budget minimum
    if criteres.min_budget is not None:
        joueurs = [
            joueur for joueur in joueurs
            if joueur.market_value_eur is not None
            and joueur.market_value_eur > criteres.min_budget
        ]

    if not joueurs:
        return []

    # 5. Classer les joueurs avec KNN
    if criteres.qualites:
        recommandations = classer_joueurs_knn(
            joueurs,
            criteres.qualites
        )
    else:
        recommandations = sorted(
            joueurs,
            key=lambda joueur: joueur.overall or 0,
            reverse=True
        )

    recommandations = recommandations[:5]

    # 6. Générer les explications avec le LLM
    explications = {}

    if avec_explications and recommandations:
        try:
            explications = expliquer_recommandations(
                description,
                recommandations
            )

        except Exception as erreur:
            print("Erreur des explications :", erreur)

    # 7. Construire les résultats pour Flask
    resultats = []

    for joueur in recommandations:

        resultat = {
            "joueur": joueur,
            "explication": explications.get(
                joueur.sofifa_id,
                ""
            )
        }

        resultats.append(resultat)

    return resultats


# Affichage des résultats dans le terminal
def afficher_resultats(resultats):

    if not resultats:
        print("Aucun joueur trouvé.")
        return

    print("\nTOP 5 RECOMMANDATIONS :")

    for i, resultat in enumerate(resultats, start=1):

        joueur = resultat["joueur"]
        explication = resultat["explication"]

        if joueur.market_value_eur is not None:
            valeur = f"{joueur.market_value_eur:,.0f} €"
        else:
            valeur = "Inconnue"

        print(f"\n{i}. {joueur.name}")
        print(f"   Club : {joueur.club}")
        print(f"   Poste : {joueur.position}")
        print(f"   Âge : {joueur.age}")
        print(f"   Note générale : {joueur.overall}")
        print(f"   Valeur marchande : {valeur}")
        print(f"   Explication : {explication}")


# Test du service
if __name__ == "__main__":

    description = input("Description du joueur : ")

    resultats = recommander(description)

    afficher_resultats(resultats)