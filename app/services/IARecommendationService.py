#Coordonne les étapes : LLM → DAO → similarité → résultat

#on ne cree pas un llm de zero car trop long et couteux, on Ollana et llama qui s
# ont des llms pour comprendre les dmds du user.




from app.services.LLMService import extraire_criteres
from app.services.SimilarityService import (
    classer_joueurs,
    calculer_score
)
from app.models.PlayerDAO import PlayerSqliteDAO


def recommander(description: str):

   
    criteres = extraire_criteres(description)

    print("Critères identifiés :", criteres.model_dump())

    
    dao = PlayerSqliteDAO()

    joueurs = dao.findByCriteria(
        edition="FC26",
        position=criteres.position,
        max_age=criteres.max_age,
        max_budget=criteres.max_budget
    )

    
    # Le DAO ne possède pas encore min_budget
    if criteres.min_budget is not None:
        joueurs = [
            joueur for joueur in joueurs
            if joueur.market_value_eur is not None
            and joueur.market_value_eur > criteres.min_budget
        ]

    print("Joueurs correspondants :", len(joueurs))

    if not joueurs:
        print("Aucun joueur trouvé.")
        return []

    
    if criteres.qualites:
        recommandations = classer_joueurs(
            joueurs,
            criteres.qualites
        )
    else:
        recommandations = sorted(
            joueurs,
            key=lambda j: j.overall or 0,
            reverse=True
        )[:5]

    
    recommandations = recommandations[:5]

   
    print("\nTOP 5 RECOMMANDATIONS :")

    for i, joueur in enumerate(recommandations, start=1):
        score = (
            calculer_score(joueur, criteres.qualites)
            if criteres.qualites
            else joueur.overall or 0
        )

        print(
            f"{i}. {joueur.name} | "
            f"Poste : {joueur.position} | "
            f"Score : {score:.1f} | "
            f"Valeur : {joueur.market_value_eur} €"
        )

    return recommandations


if __name__ == "__main__":
    description = input("Description du joueur : ")
    recommander(description)
