# 🏦 BankReco — Recommandation personnalisée de produits bancaires

**Projet de session INF-5103 — Concepts statistiques pour la science des données**  
Université du Québec en Outaouais (UQO) · Automne 2026  
**Auteur :** Leonel

## Présentation

**BankReco** est une application Python avec interface graphique **Streamlit** qui exploite l'historique des produits bancaires pour recommander à un client jusqu'à **trois produits qu'il pourrait acquérir le mois suivant**. L'outil s'adresse, à titre de client représentatif, à un responsable du marketing et de la relation clientèle d'une banque de détail. Il constitue une démonstration académique et non un outil officiel de Santander.

L'application permet de consulter les produits détenus, l'évolution du portefeuille d'un client, les recommandations personnalisées, les prévisions de juin 2016 et les indicateurs d'évaluation du système.

## Lancer l'application — commande unique

**Depuis le répertoire racine du projet**, après avoir installé les dépendances et vérifié la présence des fichiers de données et des modèles :

```powershell
python -m streamlit run app.py
```

Streamlit affiche normalement une adresse locale, généralement `http://localhost:8501`, à ouvrir dans un navigateur. Pour arrêter le serveur, utiliser `Ctrl+C` dans le terminal.

> **Important :** la commande ci-dessus lance l'application ; elle n'installe pas automatiquement Python, les bibliothèques ni les modèles. La section suivante explique la préparation initiale.

## Prérequis et installation initiale (Windows PowerShell)

- Python et un environnement disposant de `streamlit`, `pandas`, `numpy`, `scikit-learn` et `joblib` ;
- le fichier `app.py`, le jeu de données et les modèles entraînés aux emplacements indiqués ci-dessous ;
- un terminal ouvert dans le dossier racine du projet.

Exemple avec **Anaconda** et l'environnement utilisé pendant le développement :

```powershell
conda activate ml-project
cd C:\Users\alapn\PythonProjects\BankReco
python -m pip install streamlit pandas numpy scikit-learn joblib
python -m streamlit run app.py
```

Le chemin `C:\Users\alapn\PythonProjects\BankReco` est propre à l'ordinateur de développement : **remplacez-le par le chemin réel du dossier téléchargé**. Si les dépendances sont déjà installées, seule la commande de lancement est nécessaire après activation de l'environnement et positionnement dans le dossier du projet.

**Compatibilité :** les modèles sérialisés avec `joblib` peuvent nécessiter des versions de `scikit-learn` compatibles avec celles utilisées pour leur entraînement. Pour une reproduction fiable, publier un fichier `requirements.txt` avec les versions testées ou un fichier d'environnement Conda.

## Organisation du dépôt

```text
BankReco/
├── app.py
├── README.md
├── data/
│   └── santander_echantillon.csv
├── modeles/
│   ├── modeles_bankreco.joblib
│   ├── variables_X.joblib
│   └── noms_produits.joblib
├── resultats/
│   └── predictions_juin_2016.csv
└── notebooks/
    └── 03_modelisation.ipynb
```

Cette arborescence présente les **fichiers nécessaires ou utilisés dans le développement**. Vérifiez que les noms correspondent aux fichiers réellement présents dans le dépôt avant publication. Le notebook sert à documenter les expérimentations ; l'application charge directement les fichiers `joblib` et le CSV.

> **Données et taille du dépôt :** le fichier `santander_echantillon.csv` représente environ 46 Mo dans l'environnement de développement. Vérifiez les règles de redistribution des données et la taille des fichiers avant leur publication. Si un fichier n'est pas inclus dans GitHub, indiquez précisément comment l'obtenir et où le placer ; sinon, la commande de lancement ne suffira pas à reproduire l'application.

## Fonctionnalités

### 1. Recommandations

- Sélection d'un client et d'un mois d'observation ;
- affichage du profil et des produits déjà détenus ;
- génération d'un **Top 3** de produits admissibles avec probabilités estimées ;
- visualisation de l'évolution mensuelle du nombre de produits ;
- consultation des acquisitions et abandons observés et de la matrice de détention des produits.

### 2. Prévisions juin 2016

- Consultation des prévisions établies à partir des profils de mai 2016 ;
- sélection d'un client pour afficher ses recommandations et scores ;
- visualisation de la répartition du nombre de recommandations ;
- consultation et exportation des prévisions en CSV.

**Attention :** les acquisitions réelles de juin 2016 ne figurent pas dans l'échantillon utilisé ; les prévisions de juin ne peuvent donc pas être évaluées directement.

### 3. Tableau de bord

- Présentation des performances mesurées sur avril–mai 2016 ;
- comparaison à une méthode de recommandation fondée sur la popularité ;
- présentation d'une analyse bootstrap exploratoire du gain de rappel.

## Données et méthodes

**Source :** jeu de données *Santander Product Recommendation* (Kaggle). L'échantillon de travail comporte **285 734 observations**, **20 000 clients**, **17 mois** (janvier 2015 à mai 2016) et **24 indicateurs de produits bancaires**.

Sept produits sont modélisés : prélèvements automatiques, domiciliation de pension, domiciliation de salaire, compte courant, carte de crédit, compte de paie et E-account.

Le système utilise **sept modèles de régression logistique calibrés**, un par produit. Les variables d'entrée comprennent des caractéristiques client et l'état de détention des produits. Pour chaque client, le système exclut les produits déjà détenus ou de statut inconnu, puis classe les produits restants selon leur score d'acquisition estimé.

**Découpage temporel :** entraînement sur 2015, calibration sur janvier–février 2016, puis évaluation sur les périodes ultérieures. Les résultats présentés ci-dessous portent sur avril–mai 2016.

## Résultats expérimentaux

| Indicateur | BankReco | Popularité |
|---|---:|---:|
| Précision globale@3 | 1,115 % | 0,987 % |
| Rappel global@3 | 90,50 % | 80,14 % |
| Hit Rate@3 | 95,29 % | 85,16 % |

L'évaluation porte sur **38 701 observations client-mois**, **19 411 clients distincts** et **1 410 acquisitions évaluables**. Le système a produit **114 445 recommandations**, dont **1 276 correspondances avec des acquisitions**.

Le gain observé de rappel global@3 par rapport à la popularité est d'environ **10,35 points de pourcentage**. Un bootstrap exploratoire de 2 000 rééchantillonnages a produit un intervalle de confiance à 95 % de **[8,459 ; 12,343] points**.

La précision reste faible : il faut donc éviter de présenter chaque recommandation comme une acquisition probable ou certaine.

## Prévisions pour juin 2016

À partir des profils de mai 2016, l'application dispose de **57 591 recommandations** pour **19 447 clients** :

| Recommandations par client | Nombre de clients |
|---|---:|
| 0 | 24 |
| 1 | 164 |
| 2 | 350 |
| 3 | 18 909 |

Les scores enregistrés dans le fichier CSV sont des probabilités sur l'échelle **0 à 1** ; ils sont multipliés par 100 pour un affichage en pourcentage.

## Vérification rapide après lancement

1. Ouvrir la page **Recommandations**, choisir un client et un mois, puis cliquer sur **Générer les recommandations**.
2. Vérifier que les produits déjà détenus ne sont pas recommandés et que trois produits au maximum sont affichés.
3. Ouvrir **Prévisions juin 2016**, sélectionner un client et vérifier l'affichage des recommandations.
4. Ouvrir **Tableau de bord** et vérifier la présence des indicateurs d'évaluation.

Si l'application ne démarre pas, vérifier le répertoire courant, les bibliothèques installées et la présence des fichiers mentionnés dans l'arborescence.

## Limites

- Échantillon limité à 20 000 clients et à sept produits modélisés ;
- acquisitions rares et précision@3 faible ;
- performances historiques qui ne garantissent pas les résultats futurs ;
- prévisions de juin 2016 non vérifiables sans données réelles correspondantes ;
- outil académique ne tenant pas lieu de validation réglementaire ou commerciale.

## Références

- [Kaggle — Santander Product Recommendation](https://www.kaggle.com/competitions/santander-product-recommendation)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation scikit-learn](https://scikit-learn.org/stable/)

## Licence et publication

Aucune licence logicielle n'est définie ici. Ajouter une licence uniquement après avoir choisi ses conditions et vérifié les droits de redistribution des fichiers inclus.

**Projet pédagogique INF-5103 — UQO, automne 2026.**
