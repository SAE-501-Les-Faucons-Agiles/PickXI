#LLMService — Compréhension de la requête

#en gros le user va dire :Je cherche un jeune attaquant rapide et technique, 
# qui coûte moins de 50 millions


from pathlib import Path
from ollama import chat

from app.services.RecommendationCriteria import RecommendationCriteria



CONTEXTE_PATH = (
    Path(__file__).resolve().parent
    / "Contexte_LLM.md"
)


def extraire_criteres(description: str) -> RecommendationCriteria:

    
    contexte = CONTEXTE_PATH.read_text(encoding="utf-8")

    
    reponse = chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": contexte
            },
            {
                "role": "user",
                "content": description
            }
        ],
        format=RecommendationCriteria.model_json_schema(),
        options={"temperature": 0}
    )

    
    criteres = RecommendationCriteria.model_validate_json(
        reponse.message.content
    )

    return criteres



if __name__ == "__main__":

    description = input("Description du joueur : ")

    criteres = extraire_criteres(description)

    print("Poste :", criteres.position)
    print("Qualités :", criteres.qualites)
    print("Âge maximal :", criteres.max_age)
    print("Budget maximal :", criteres.max_budget)
