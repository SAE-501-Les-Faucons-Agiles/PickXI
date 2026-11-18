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
<p align="left">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" />
  <img src="https://img.shields.io/badge/Git_LFS-24292E?style=for-the-badge&logo=gitlfs&logoColor=white" alt="Git LFS" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Docker_Compose-v2+-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose v2" />
</p>
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

Attendre la fin du téléchargement du modèle, puis ouvrir **http://localhost:8000/**. Le téléchargement du modèle n'est nécessaire qu'à la première utilisation ou si le volume des modèles a été supprimé. Les réponses IA peuvent prendre du temps sur CPU.

Pour arrêter l'application en conservant la base et le modèle :

```bash
docker compose down
```

Pour la relancer :

```bash
docker compose up -d
```

## État du projet

Cette partie est destinée à faire un rapide résumé de l'état du projet et de nos pistes de réflexion lors du premier rendu, le 18 novembre.

- Le premier algorithme « score » est fonctionnel, mais nous réfléchissons déjà à certaines optimisations.
- L'algorithme IA est partiellement fonctionnel. Nous envisageons d'utiliser le même système de critères que le premier algorithme à la place du chatbot, tout en continuant d'utiliser l'IA pour produire un résultat.
- Certains éléments visuels vont être améliorés.
- La partie terrain n'est actuellement que partiellement fonctionnelle, mais nous pensons que c'est un bon ajout au site.
