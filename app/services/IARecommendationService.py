#Coordonne les étapes : LLM → DAO → similarité → résultat

#on ne cree pas un llm de zero car trop long et couteux, on Ollana et llama qui s
# ont des llms pour comprendre les dmds du user.


from app.services.LLMService import extraire_criteres

from app.services.SimilarityService import (
    classer_joueurs_knn,
    QUALITES_STATS
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

    
     # 4. Filtrer l'âge minimum
    if criteres.min_age is not None:
        joueurs = [
            joueur for joueur in joueurs
            if joueur.age is not None
            and joueur.age >= criteres.min_age
        ]

    # 5. Vérifier l'âge maximum
    if criteres.max_age is not None:
        joueurs = [
            joueur for joueur in joueurs
            if joueur.age is not None
            and joueur.age <= criteres.max_age
        ]

    # 6. Filtrer le budget minimum
    if criteres.min_budget is not None:
        joueurs = [
            joueur for joueur in joueurs
            if joueur.market_value_eur > criteres.min_budget
        ]

    # 7. Vérifier le budget maximum
    if criteres.max_budget is not None:
        joueurs = [
            joueur for joueur in joueurs
            if joueur.market_value_eur <= criteres.max_budget
        ]
        

    print("Joueurs correspondants :", len(joueurs))

    if not joueurs:
        print("Aucun joueur trouvé.")
        return []

    
    if criteres.qualites:
        recommandations = classer_joueurs_knn(
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
        if joueur.market_value_eur is not None:
            valeur = f"{joueur.market_value_eur} €"
        else:
            valeur = "Inconnu"



        print(f"\n{i}. {joueur.name}")
        print(f"   Club : {joueur.club}")
        print(f"   Poste : {joueur.position}")
        print(f"   Âge : {joueur.age}")
        print(f"   Note générale : {joueur.overall}")
        print(f"   Valeur marchande : {valeur}")

        # Afficher les statistiques demandées
        for qualite in criteres.qualites:

            statistique = QUALITES_STATS[qualite]
            note = getattr(joueur, statistique, None)

            print(f"   {qualite.capitalize()} : {note}")

    return recommandations
    






if __name__ == "__main__":
    description = input("Description du joueur : ")
    recommander(description)
   
