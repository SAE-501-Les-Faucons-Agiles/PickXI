from pathlib import Path
import json
import re

from ollama import chat
from pydantic import BaseModel

from app.services.RecommendationCriteria import RecommendationCriteria


CONTEXTE_PATH = (
    Path(__file__).resolve().parent
    / "Contexte_LLM.md"
)

CONTEXTE_EXPLICATIONS_PATH = (
    Path(__file__).resolve().parent
    / "Contexte_Explications.md"
)


# Structure des explications retournées par le LLM

class ExplicationJoueur(BaseModel):
    id: int
    explication: str


class Explications(BaseModel):
    joueurs: list[ExplicationJoueur]


# Vérification des contraintes d'âge

def verifier_age(description, criteres):

    texte = description.lower()

    age_min = re.search(
        r"(?<!pas )\bplus\s+de\s+(\d{1,2})\s*ans?\b",
        texte
    )

    age_max = re.search(
        r"\b(?:moins de|pas plus de)\s+(\d{1,2})\s*ans?\b",
        texte
    )

    if age_min:
        criteres.min_age = int(age_min.group(1)) + 1

        if not age_max and not re.search(
            r"\b\d{1,2}\s*ans?\s*max(?:imum)?\b",
            texte
        ):
            criteres.max_age = None

    if age_max:
        criteres.max_age = int(age_max.group(1))

    return RecommendationCriteria.model_validate(
        criteres.model_dump()
    )


# Extraction des critères de recherche

def extraire_criteres(description: str):

    contexte = CONTEXTE_PATH.read_text(
        encoding="utf-8"
    )

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
        options={"temperature": 0},
        keep_alive="30m"
    )

    criteres = RecommendationCriteria.model_validate_json(
        reponse.message.content
    )

    criteres = verifier_age(description, criteres)

    return criteres


# Génération des explications des recommandations

def expliquer_recommandations(description, joueurs):

    if not joueurs:
        return {}

    contexte = CONTEXTE_EXPLICATIONS_PATH.read_text(
        encoding="utf-8"
    )

    # Transformer les objets Player en dictionnaires

    donnees = []

    for joueur in joueurs:

        dictionnaire = {
            "id": joueur.sofifa_id,
            "nom": joueur.name,
            "club": joueur.club,
            "poste": joueur.position,
            "age": joueur.age,
            "note": joueur.overall,
            "vitesse": joueur.pace,
            "tir": joueur.shooting,
            "passe": joueur.passing,
            "dribble": joueur.dribbling,
            "defense": joueur.defending,
            "physique": joueur.physicality,
            "valeur": joueur.market_value_eur
        }

        donnees.append(dictionnaire)

    # Associer la demande aux joueurs recommandés

    message = {
        "demande": description,
        "joueurs": donnees
    }

    # Envoyer les données au LLM

    reponse = chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": contexte
            },
            {
                "role": "user",
                "content": json.dumps(
                    message,
                    ensure_ascii=False
                )
            }
        ],
        format=Explications.model_json_schema(),
        options={"temperature": 0},
        keep_alive="30m"
    )

    # Validation de la réponse

    resultat = Explications.model_validate_json(
        reponse.message.content
    )

    ids_autorises = {
        joueur.sofifa_id for joueur in joueurs
    }

    explications = {
        item.id: item.explication
        for item in resultat.joueurs
        if item.id in ids_autorises
    }

    return explications


# Test de l'extraction des critères

if __name__ == "__main__":

    description = input("Description du joueur : ")

    criteres = extraire_criteres(description)

    print(criteres.model_dump())