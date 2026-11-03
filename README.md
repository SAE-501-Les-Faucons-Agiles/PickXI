# FUTScout 26 – Recommandation Comparée de Joueurs FIFA / EA Sports FC

Application web découplée d'optimisation d'équipe et d'évaluation comparative d'algorithmes de recommandation, développée avec **Flask** (Backend) et **Jinja2 + Tailwind CSS + Chart.js** (Frontend) pour la **SAÉ BUT3 5.Real.01** (IUT de Villetaneuse).

---

## ⚽ Cas d'Usage & Fonctionnalités

Permet aux joueurs d'Ultimate Team (FUT) de trouver la recrue idéale pour leur effectif selon leurs critères tactiques et financiers, tout en comparant en direct l'efficience de deux approches algorithmiques :

1. **Filtres de Recrutement Précis** :
   - Poste (BU, AG, AD, MOC, MC, MDC, DC, DG, DD, G).
   - Budget maximal en crédits (Coins 🪙).
   - Exigence minimale de Mauvais Pied (1★ à 5★).
   - Liens de synergie pour le collectif (Club, Ligue, Nationalité).
   - Pondération personnalisée des 6 attributs clés : **PAC** (Vitesse), **SHO** (Tir), **PAS** (Passe), **DRI** (Dribble), **DEF** (Défense), **PHY** (Physique).

2. **Interface Split-View (Conforme à votre demande)** :
   - **À gauche** : Liste des cartes de joueurs recommandés, classées avec note générale, poste, club, prix, étoiles WF/SM et stats détaillées. Onglets pour basculer entre l'approche vectorielle et l'approche graphe.
   - **À droite** : Tableau de bord visuel en temps réel (*Pastushenko et al., 2021*) avec temps de calcul (min, max, moyen en ms), consommation mémoire, radar des 6 attributs et impact batterie.

3. **Les Deux Approches Algorithmiques Comparées** :
   - **Approche 1 : Similarité Vectorielle (Distance Cosinus)** :
     - Projette les statistiques de chaque joueur dans un espace à 7 dimensions ($\mathbb{R}^7$).
     - Calcule la similarité cosinus avec le profil athlétique et technique recherché.
     - Complexité théorique : $\mathcal{O}(N \times D)$ ($D = 7$).
   - **Approche 2 : Graphe de Collectif & Rentabilité Économique** :
     - Modélise le collectif comme un graphe de synergies (+3 Club, +2 Ligue, +1 Nation).
     - Applique une heuristique qualité/prix pour maximiser la rentabilité en crédits.
     - Complexité théorique : $\mathcal{O}(N \times C + N \log K)$.

4. **Compatibilité avec le Dataset Kaggle** :
   - Conçu pour le schéma SoFIFA du dataset : [FC 26 FIFA 26 Player Data (rovnez)](https://www.kaggle.com/datasets/rovnez/fc-26-fifa-26-player-data/data).
   - Intègre un chargeur automatique de CSV dans `data/` (+18 000 joueurs supportés) avec repli transparent sur un échantillon des meilleures cartes méta du jeu (Mbappé, Haaland, Vinícius Jr., Bellingham, Rodri, De Bruyne...).

---

## 📂 Architecture MVC Découplée

```text
SAE_501/
├── app/
│   ├── __init__.py               # Factory Flask (create_app)
│   ├── config.py                 # Configuration de l'environnement
│   ├── models/                   # [M] Modèles de données
│   │   ├── __init__.py
│   │   └── player_model.py       # Player, PlayerFilter, RankedPlayer, PerformanceMetrics
│   ├── templates/                # [V] Vues Jinja (Frontend Split-View)
│   │   ├── base.html             # Layout principal (Thème EA FC sombre & doré, Chart.js)
│   │   ├── index.html            # Split-View : Joueurs à gauche, Dashboard à droite
│   │   ├── players.html          # Catalogue complet des cartes de joueurs
│   │   └── about.html            # Documentation technique & Licence MIT
│   ├── static/css/style.css      # Styles complémentaires
│   ├── controllers/              # [C] Contrôleurs Flask
│   │   ├── home_controller.py    # Contrôleur Web (rendu des vues Jinja)
│   │   └── api_controller.py     # Contrôleur API REST découplée (/api/v1)
│   └── services/                 # Logique métier & Algorithmes
│       ├── metrics_service.py     # Mesures de temps (min/max/moy), mémoire, batterie
│       ├── player_repository.py   # Chargeur CSV Kaggle + base de secours
│       └── recommendation_service.py # Vectoriel (Cosinus) vs Graphe de Collectif
├── data/                         # Déposez votre CSV Kaggle ici (ex: data/players.csv)
├── tests/
│   └── test_recommendations.py   # Suite de tests unitaires
├── run.py                        # Point d'entrée de l'application
├── requirements.txt              # Dépendances (Flask)
└── README.md
```

---

## 🚀 Démarrage Rapide

### 1. Lancer le serveur local
```bash
python3 run.py
```
Accédez à l'application sur : **http://localhost:5000**

- **Comparateur & Dashboard (Split-View)** : `http://localhost:5000/`
- **Catalogue des joueurs** : `http://localhost:5000/players`
- **API REST découplée** : `http://localhost:5000/api/v1/players`

### 2. Importer le dataset Kaggle complet (Optionnel)
Téléchargez le fichier CSV depuis [Kaggle](https://www.kaggle.com/datasets/rovnez/fc-26-fifa-26-player-data/data) et placez-le dans le dossier `data/` :
```bash
# Exemple :
cp /chemin/vers/FC26_20250921.csv data/players.csv
```
Au prochain démarrage, l'application chargera automatiquement l'intégralité des 18 000+ joueurs !

### 3. Exécuter les tests unitaires
```bash
python3 -m unittest discover tests
```

---

## ⚖️ Licence Open Source
Projet sous licence **MIT Open Source**.
