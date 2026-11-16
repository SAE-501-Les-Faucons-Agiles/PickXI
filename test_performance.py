import time

from app.services.IARecommendationService import recommander

description = "Je cherche un attaquant rapide de moins de 25 ans"

debut = time.perf_counter()

resultats = recommander(description)

fin = time.perf_counter()

print(f"Nombre de joueurs : {len(resultats)}")
print(f"Temps de réponse : {fin - debut:.2f} secondes")
