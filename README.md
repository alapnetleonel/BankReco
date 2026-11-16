# ðŸ¦ BankReco â€” Recommandation personnalisÃ©e de produits bancaires

**Projet de session INF-5103 â€” Concepts statistiques pour la science des donnÃ©es**
UniversitÃ© du QuÃ©bec en Outaouais (UQO) Â· Automne 2026
**Auteur :** Leonel

## PrÃ©sentation

**BankReco** est une application Python avec interface graphique **Streamlit** qui exploite l'historique des produits bancaires pour recommander Ã  un client jusqu'Ã  **trois produits qu'il pourrait acquÃ©rir le mois suivant**. L'outil s'adresse, Ã  titre de client reprÃ©sentatif, Ã  un responsable du marketing et de la relation clientÃ¨le d'une banque de dÃ©tail. Il constitue une dÃ©monstration acadÃ©mique et non un outil officiel de Santander.

L'application permet de consulter les produits dÃ©tenus, l'Ã©volution du portefeuille d'un client, les recommandations personnalisÃ©es, les prÃ©visions de juin 2016 et les indicateurs d'Ã©valuation du systÃ¨me.

## Lancer l'application â€” commande unique

**Depuis le rÃ©pertoire racine du projet**, aprÃ¨s avoir installÃ© les dÃ©pendances et vÃ©rifiÃ© la prÃ©sence des fichiers de donnÃ©es et des modÃ¨les :

```powershell
python -m streamlit run app.py
```

Streamlit affiche normalement une adresse locale, gÃ©nÃ©ralement `http://localhost:8501`, Ã  ouvrir dans un navigateur. Pour arrÃªter le serveur, utiliser `Ctrl+C` dans le terminal.

> **Important :** la commande ci-dessus lance l'application ; elle n'installe pas automatiquement Python, les bibliothÃ¨ques ni les modÃ¨les. La section suivante explique la prÃ©paration initiale.

## PrÃ©requis et installation initiale (Windows PowerShell)

- Python et un environnement disposant de `streamlit`, `pandas`, `numpy`, `scikit-learn` et `joblib` ;
- le fichier `app.py`, le jeu de donnÃ©es et les modÃ¨les entraÃ®nÃ©s aux emplacements indiquÃ©s ci-dessous ;
- un terminal ouvert dans le dossier racine du projet.

Exemple avec **Anaconda** et l'environnement utilisÃ© pendant le dÃ©veloppement :

```powershell
conda activate ml-project
cd C:\Users\alapn\PythonProjects\BankReco
python -m pip install streamlit pandas numpy scikit-learn joblib
python -m streamlit run app.py
```

Le chemin `C:\Users\alapn\PythonProjects\BankReco` est propre Ã  l'ordinateur de dÃ©veloppement : **remplacez-le par le chemin rÃ©el du dossier tÃ©lÃ©chargÃ©**. Si les dÃ©pendances sont dÃ©jÃ  installÃ©es, seule la commande de lancement est nÃ©cessaire aprÃ¨s activation de l'environnement et positionnement dans le dossier du projet.

**CompatibilitÃ© :** les modÃ¨les sÃ©rialisÃ©s avec `joblib` peuvent nÃ©cessiter des versions de `scikit-learn` compatibles avec celles utilisÃ©es pour leur entraÃ®nement. Pour une reproduction fiable, publier un fichier `requirements.txt` avec les versions testÃ©es ou un fichier d'environnement Conda.

## Organisation du dÃ©pÃ´t

```text
BankReco/
â”œâ”€â”€ app.py
â”œâ”€â”€ README.md
â”œâ”€â”€ data/
â”‚   â””â”€â”€ santander_echantillon.csv
â”œâ”€â”€ modeles/
â”‚   â”œâ”€â”€ modeles_bankreco.joblib
â”‚   â”œâ”€â”€ variables_X.joblib
â”‚   â””â”€â”€ noms_produits.joblib
â”œâ”€â”€ resultats/
â”‚   â””â”€â”€ predictions_juin_2016.csv
â””â”€â”€ notebooks/
    â””â”€â”€ 03_modelisation.ipynb
```

Cette arborescence prÃ©sente les **fichiers nÃ©cessaires ou utilisÃ©s dans le dÃ©veloppement**. VÃ©rifiez que les noms correspondent aux fichiers rÃ©ellement prÃ©sents dans le dÃ©pÃ´t avant publication. Le notebook sert Ã  documenter les expÃ©rimentations ; l'application charge directement les fichiers `joblib` et le CSV.

> **DonnÃ©es et taille du dÃ©pÃ´t :** le fichier `santander_echantillon.csv` reprÃ©sente environ 46 Mo dans l'environnement de dÃ©veloppement. VÃ©rifiez les rÃ¨gles de redistribution des donnÃ©es et la taille des fichiers avant leur publication. Si un fichier n'est pas inclus dans GitHub, indiquez prÃ©cisÃ©ment comment l'obtenir et oÃ¹ le placer ; sinon, la commande de lancement ne suffira pas Ã  reproduire l'application.

## FonctionnalitÃ©s

### 1. Recommandations

- SÃ©lection d'un client et d'un mois d'observation ;
- affichage du profil et des produits dÃ©jÃ  dÃ©tenus ;
- gÃ©nÃ©ration d'un **Top 3** de produits admissibles avec probabilitÃ©s estimÃ©es ;
- visualisation de l'Ã©volution mensuelle du nombre de produits ;
- consultation des acquisitions et abandons observÃ©s et de la matrice de dÃ©tention des produits.

### 2. PrÃ©visions juin 2016

- Consultation des prÃ©visions Ã©tablies Ã  partir des profils de mai 2016 ;
- sÃ©lection d'un client pour afficher ses recommandations et scores ;
- visualisation de la rÃ©partition du nombre de recommandations ;
- consultation et exportation des prÃ©visions en CSV.

**Attention :** les acquisitions rÃ©elles de juin 2016 ne figurent pas dans l'Ã©chantillon utilisÃ© ; les prÃ©visions de juin ne peuvent donc pas Ãªtre Ã©valuÃ©es directement.

### 3. Tableau de bord

- PrÃ©sentation des performances mesurÃ©es sur avrilâ€“mai 2016 ;
- comparaison Ã  une mÃ©thode de recommandation fondÃ©e sur la popularitÃ© ;
- prÃ©sentation d'une analyse bootstrap exploratoire du gain de rappel.

## DonnÃ©es et mÃ©thodes

**Source :** jeu de donnÃ©es *Santander Product Recommendation* (Kaggle). L'Ã©chantillon de travail comporte **285 734 observations**, **20 000 clients**, **17 mois** (janvier 2015 Ã  mai 2016) et **24 indicateurs de produits bancaires**.

Sept produits sont modÃ©lisÃ©s : prÃ©lÃ¨vements automatiques, domiciliation de pension, domiciliation de salaire, compte courant, carte de crÃ©dit, compte de paie et E-account.

Le systÃ¨me utilise **sept modÃ¨les de rÃ©gression logistique calibrÃ©s**, un par produit. Les variables d'entrÃ©e comprennent des caractÃ©ristiques client et l'Ã©tat de dÃ©tention des produits. Pour chaque client, le systÃ¨me exclut les produits dÃ©jÃ  dÃ©tenus ou de statut inconnu, puis classe les produits restants selon leur score d'acquisition estimÃ©.

**DÃ©coupage temporel :** entraÃ®nement sur 2015, calibration sur janvierâ€“fÃ©vrier 2016, puis Ã©valuation sur les pÃ©riodes ultÃ©rieures. Les rÃ©sultats prÃ©sentÃ©s ci-dessous portent sur avrilâ€“mai 2016.

## RÃ©sultats expÃ©rimentaux

| Indicateur | BankReco | PopularitÃ© |
|---|---:|---:|
| PrÃ©cision globale@3 | 1,115 % | 0,987 % |
| Rappel global@3 | 90,50 % | 80,14 % |
| Hit Rate@3 | 95,29 % | 85,16 % |

L'Ã©valuation porte sur **38 701 observations client-mois**, **19 411 clients distincts** et **1 410 acquisitions Ã©valuables**. Le systÃ¨me a produit **114 445 recommandations**, dont **1 276 correspondances avec des acquisitions**.

Le gain observÃ© de rappel global@3 par rapport Ã  la popularitÃ© est d'environ **10,35 points de pourcentage**. Un bootstrap exploratoire de 2 000 rÃ©Ã©chantillonnages a produit un intervalle de confiance Ã  95 % de **[8,459 ; 12,343] points**.

La prÃ©cision reste faible : il faut donc Ã©viter de prÃ©senter chaque recommandation comme une acquisition probable ou certaine.

## PrÃ©visions pour juin 2016

Ã€ partir des profils de mai 2016, l'application dispose de **57 591 recommandations** pour **19 447 clients** :

| Recommandations par client | Nombre de clients |
|---|---:|
| 0 | 24 |
| 1 | 164 |
| 2 | 350 |
| 3 | 18 909 |

Les scores enregistrÃ©s dans le fichier CSV sont des probabilitÃ©s sur l'Ã©chelle **0 Ã  1** ; ils sont multipliÃ©s par 100 pour un affichage en pourcentage.

## VÃ©rification rapide aprÃ¨s lancement

1. Ouvrir la page **Recommandations**, choisir un client et un mois, puis cliquer sur **GÃ©nÃ©rer les recommandations**.
2. VÃ©rifier que les produits dÃ©jÃ  dÃ©tenus ne sont pas recommandÃ©s et que trois produits au maximum sont affichÃ©s.
3. Ouvrir **PrÃ©visions juin 2016**, sÃ©lectionner un client et vÃ©rifier l'affichage des recommandations.
4. Ouvrir **Tableau de bord** et vÃ©rifier la prÃ©sence des indicateurs d'Ã©valuation.

Si l'application ne dÃ©marre pas, vÃ©rifier le rÃ©pertoire courant, les bibliothÃ¨ques installÃ©es et la prÃ©sence des fichiers mentionnÃ©s dans l'arborescence.

## Limites

- Ã‰chantillon limitÃ© Ã  20 000 clients et Ã  sept produits modÃ©lisÃ©s ;
- acquisitions rares et prÃ©cision@3 faible ;
- performances historiques qui ne garantissent pas les rÃ©sultats futurs ;
- prÃ©visions de juin 2016 non vÃ©rifiables sans donnÃ©es rÃ©elles correspondantes ;
- outil acadÃ©mique ne tenant pas lieu de validation rÃ©glementaire ou commerciale.

## RÃ©fÃ©rences

- [Kaggle â€” Santander Product Recommendation](https://www.kaggle.com/competitions/santander-product-recommendation)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation scikit-learn](https://scikit-learn.org/stable/)

## Licence et publication

Aucune licence logicielle n'est dÃ©finie ici. Ajouter une licence uniquement aprÃ¨s avoir choisi ses conditions et vÃ©rifiÃ© les droits de redistribution des fichiers inclus.

**Projet pÃ©dagogique INF-5103 â€” UQO, automne 2026.**
