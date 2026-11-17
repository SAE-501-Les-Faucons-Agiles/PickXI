# SAE-501 — pickXI

Application web de recherche et de recommandation de joueurs de football à partir des données EA Sports FC 26, avec des filtres et un assistant IA.

Dépôt Git : [SAE-501](https://github.com/SAE-501-Les-Faucons-Agiles/SAE-501)

## Développeurs

- Redwan DJEDIA
- Yunes BOUABTA
- Luka JEVTIC
- Jasper PETIT
- Issam KHADROUF
- Riyad LAROUB

## Lancer avec Docker

Prérequis : Git, Git LFS, Docker et Docker Compose v2 installés, Docker démarré, port 8000 disponible et plusieurs Go d'espace disque libre.

Récupérer le projet et sa base SQLite :

```bash
git lfs install
git clone https://github.com/SAE-501-Les-Faucons-Agiles/SAE-501.git
cd SAE-501
git lfs pull
```

Depuis la racine du projet, où se trouve `compose.yaml` :

```bash
docker compose up -d --build
docker compose exec ollama ollama pull llama3.2
```

Le téléchargement peut être volumineux en raison du modèle LLM. Prévoir suffisamment d'espace disque sur la machine, même en cas d'exécution dans une VM.

Attendre la fin du téléchargement du modèle, puis ouvrir **http://localhost:8000/scout**. Le téléchargement du modèle n'est nécessaire qu'à la première utilisation ou si le volume des modèles a été supprimé. Les réponses IA peuvent prendre du temps sur CPU.

Pour arrêter l'application en conservant la base et le modèle :

```bash
docker compose down
```

Pour la relancer :

```bash
docker compose up -d
```
