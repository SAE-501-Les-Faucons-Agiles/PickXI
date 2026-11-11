#LLMService — Compréhension de la requête

#en gros le user va dire :Je cherche un jeune attaquant rapide et technique, 
# qui coûte moins de 50 millions


from ollama import chat
import json
from app.services.RecommendationCriteria import RecommendationCriteria

des = input("Description du joueur : ")

reponse = chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": """
            Tu es un expert en football.

            Analyse la demande de l'utilisateur et identifie :
            - Le poste recherché (ST, CB, GK, CM, CAM, etc.)
            - Les qualités recherchées (vitesse, dribble, tir, etc.)

            Retourne uniquement un JSON sous cette forme :
            {
                "position": "ST",
                "qualites": ["vitesse", "dribble"]
            }

            Adapte les valeurs à la demande de l'utilisateur.
            Si le poste n'est pas précisé, utilise null.
            """
        },
        {
            "role": "user",
            "content": des
        }
    ],
    format=RecommendationCriteria.model_json_schema()
)

criteres = RecommendationCriteria.model_validate_json(reponse.message.content)

print(criteres.position)
print(criteres.qualites)
