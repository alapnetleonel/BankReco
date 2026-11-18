# Ã°Å¸ÂÂ¦ BankReco Ã¢â‚¬â€ Recommandation personnalisÃƒÂ©e de produits bancaires

**Projet de session INF-5103 Ã¢â‚¬â€ Concepts statistiques pour la science des donnÃƒÂ©es**
UniversitÃƒÂ© du QuÃƒÂ©bec en Outaouais (UQO) Ã‚Â· Automne 2026
**Auteur :** Leonel

## PrÃƒÂ©sentation

**BankReco** est une application Python avec interface graphique **Streamlit** qui exploite l'historique des produits bancaires pour recommander ÃƒÂ  un client jusqu'ÃƒÂ  **trois produits qu'il pourrait acquÃƒÂ©rir le mois suivant**. L'outil s'adresse, ÃƒÂ  titre de client reprÃƒÂ©sentatif, ÃƒÂ  un responsable du marketing et de la relation clientÃƒÂ¨le d'une banque de dÃƒÂ©tail. Il constitue une dÃƒÂ©monstration acadÃƒÂ©mique et non un outil officiel de Santander.

L'application permet de consulter les produits dÃƒÂ©tenus, l'ÃƒÂ©volution du portefeuille d'un client, les recommandations personnalisÃƒÂ©es, les prÃƒÂ©visions de juin 2016 et les indicateurs d'ÃƒÂ©valuation du systÃƒÂ¨me.

## Lancer l'application Ã¢â‚¬â€ commande unique

**Depuis le rÃƒÂ©pertoire racine du projet**, aprÃƒÂ¨s avoir installÃƒÂ© les dÃƒÂ©pendances et vÃƒÂ©rifiÃƒÂ© la prÃƒÂ©sence des fichiers de donnÃƒÂ©es et des modÃƒÂ¨les :

```powershell
python -m streamlit run app.py
```

Streamlit affiche normalement une adresse locale, gÃƒÂ©nÃƒÂ©ralement `http://localhost:8501`, ÃƒÂ  ouvrir dans un navigateur. Pour arrÃƒÂªter le serveur, utiliser `Ctrl+C` dans le terminal.

> **Important :** la commande ci-dessus lance l'application ; elle n'installe pas automatiquement Python, les bibliothÃƒÂ¨ques ni les modÃƒÂ¨les. La section suivante explique la prÃƒÂ©paration initiale.

## PrÃƒÂ©requis et installation initiale (Windows PowerShell)

- Python et un environnement disposant de `streamlit`, `pandas`, `numpy`, `scikit-learn` et `joblib` ;
- le fichier `app.py`, le jeu de donnÃƒÂ©es et les modÃƒÂ¨les entraÃƒÂ®nÃƒÂ©s aux emplacements indiquÃƒÂ©s ci-dessous ;
- un terminal ouvert dans le dossier racine du projet.

Exemple avec **Anaconda** et l'environnement utilisÃƒÂ© pendant le dÃƒÂ©veloppement :

```powershell
conda activate ml-project
cd C:\Users\alapn\PythonProjects\BankReco
python -m pip install streamlit pandas numpy scikit-learn joblib
python -m streamlit run app.py
```

Le chemin `C:\Users\alapn\PythonProjects\BankReco` est propre ÃƒÂ  l'ordinateur de dÃƒÂ©veloppement : **remplacez-le par le chemin rÃƒÂ©el du dossier tÃƒÂ©lÃƒÂ©chargÃƒÂ©**. Si les dÃƒÂ©pendances sont dÃƒÂ©jÃƒÂ  installÃƒÂ©es, seule la commande de lancement est nÃƒÂ©cessaire aprÃƒÂ¨s activation de l'environnement et positionnement dans le dossier du projet.

**CompatibilitÃƒÂ© :** les modÃƒÂ¨les sÃƒÂ©rialisÃƒÂ©s avec `joblib` peuvent nÃƒÂ©cessiter des versions de `scikit-learn` compatibles avec celles utilisÃƒÂ©es pour leur entraÃƒÂ®nement. Pour une reproduction fiable, publier un fichier `requirements.txt` avec les versions testÃƒÂ©es ou un fichier d'environnement Conda.

## Organisation du dÃƒÂ©pÃƒÂ´t

```text
BankReco/
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ app.py
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ README.md
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ data/
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ santander_echantillon.csv
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ modeles/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ modeles_bankreco.joblib
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ variables_X.joblib
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ noms_produits.joblib
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ resultats/
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ predictions_juin_2016.csv
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ notebooks/
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ 03_modelisation.ipynb
```

Cette arborescence prÃƒÂ©sente les **fichiers nÃƒÂ©cessaires ou utilisÃƒÂ©s dans le dÃƒÂ©veloppement**. VÃƒÂ©rifiez que les noms correspondent aux fichiers rÃƒÂ©ellement prÃƒÂ©sents dans le dÃƒÂ©pÃƒÂ´t avant publication. Le notebook sert ÃƒÂ  documenter les expÃƒÂ©rimentations ; l'application charge directement les fichiers `joblib` et le CSV.

> **DonnÃƒÂ©es et taille du dÃƒÂ©pÃƒÂ´t :** le fichier `santander_echantillon.csv` reprÃƒÂ©sente environ 46 Mo dans l'environnement de dÃƒÂ©veloppement. VÃƒÂ©rifiez les rÃƒÂ¨gles de redistribution des donnÃƒÂ©es et la taille des fichiers avant leur publication. Si un fichier n'est pas inclus dans GitHub, indiquez prÃƒÂ©cisÃƒÂ©ment comment l'obtenir et oÃƒÂ¹ le placer ; sinon, la commande de lancement ne suffira pas ÃƒÂ  reproduire l'application.

## FonctionnalitÃƒÂ©s

### 1. Recommandations

- SÃƒÂ©lection d'un client et d'un mois d'observation ;
- affichage du profil et des produits dÃƒÂ©jÃƒÂ  dÃƒÂ©tenus ;
- gÃƒÂ©nÃƒÂ©ration d'un **Top 3** de produits admissibles avec probabilitÃƒÂ©s estimÃƒÂ©es ;
- visualisation de l'ÃƒÂ©volution mensuelle du nombre de produits ;
- consultation des acquisitions et abandons observÃƒÂ©s et de la matrice de dÃƒÂ©tention des produits.

### 2. PrÃƒÂ©visions juin 2016

- Consultation des prÃƒÂ©visions ÃƒÂ©tablies ÃƒÂ  partir des profils de mai 2016 ;
- sÃƒÂ©lection d'un client pour afficher ses recommandations et scores ;
- visualisation de la rÃƒÂ©partition du nombre de recommandations ;
- consultation et exportation des prÃƒÂ©visions en CSV.

**Attention :** les acquisitions rÃƒÂ©elles de juin 2016 ne figurent pas dans l'ÃƒÂ©chantillon utilisÃƒÂ© ; les prÃƒÂ©visions de juin ne peuvent donc pas ÃƒÂªtre ÃƒÂ©valuÃƒÂ©es directement.

### 3. Tableau de bord

- PrÃƒÂ©sentation des performances mesurÃƒÂ©es sur avrilÃ¢â‚¬â€œmai 2016 ;
- comparaison ÃƒÂ  une mÃƒÂ©thode de recommandation fondÃƒÂ©e sur la popularitÃƒÂ© ;
- prÃƒÂ©sentation d'une analyse bootstrap exploratoire du gain de rappel.

## DonnÃƒÂ©es et mÃƒÂ©thodes

**Source :** jeu de donnÃƒÂ©es *Santander Product Recommendation* (Kaggle). L'ÃƒÂ©chantillon de travail comporte **285 734 observations**, **20 000 clients**, **17 mois** (janvier 2015 ÃƒÂ  mai 2016) et **24 indicateurs de produits bancaires**.

Sept produits sont modÃƒÂ©lisÃƒÂ©s : prÃƒÂ©lÃƒÂ¨vements automatiques, domiciliation de pension, domiciliation de salaire, compte courant, carte de crÃƒÂ©dit, compte de paie et E-account.

Le systÃƒÂ¨me utilise **sept modÃƒÂ¨les de rÃƒÂ©gression logistique calibrÃƒÂ©s**, un par produit. Les variables d'entrÃƒÂ©e comprennent des caractÃƒÂ©ristiques client et l'ÃƒÂ©tat de dÃƒÂ©tention des produits. Pour chaque client, le systÃƒÂ¨me exclut les produits dÃƒÂ©jÃƒÂ  dÃƒÂ©tenus ou de statut inconnu, puis classe les produits restants selon leur score d'acquisition estimÃƒÂ©.

**DÃƒÂ©coupage temporel :** entraÃƒÂ®nement sur 2015, calibration sur janvierÃ¢â‚¬â€œfÃƒÂ©vrier 2016, puis ÃƒÂ©valuation sur les pÃƒÂ©riodes ultÃƒÂ©rieures. Les rÃƒÂ©sultats prÃƒÂ©sentÃƒÂ©s ci-dessous portent sur avrilÃ¢â‚¬â€œmai 2016.

## RÃƒÂ©sultats expÃƒÂ©rimentaux

| Indicateur | BankReco | PopularitÃƒÂ© |
|---|---:|---:|
| PrÃƒÂ©cision globale@3 | 1,115 % | 0,987 % |
| Rappel global@3 | 90,50 % | 80,14 % |
| Hit Rate@3 | 95,29 % | 85,16 % |

L'ÃƒÂ©valuation porte sur **38 701 observations client-mois**, **19 411 clients distincts** et **1 410 acquisitions ÃƒÂ©valuables**. Le systÃƒÂ¨me a produit **114 445 recommandations**, dont **1 276 correspondances avec des acquisitions**.

Le gain observÃƒÂ© de rappel global@3 par rapport ÃƒÂ  la popularitÃƒÂ© est d'environ **10,35 points de pourcentage**. Un bootstrap exploratoire de 2 000 rÃƒÂ©ÃƒÂ©chantillonnages a produit un intervalle de confiance ÃƒÂ  95 % de **[8,459 ; 12,343] points**.

La prÃƒÂ©cision reste faible : il faut donc ÃƒÂ©viter de prÃƒÂ©senter chaque recommandation comme une acquisition probable ou certaine.

## PrÃƒÂ©visions pour juin 2016

Ãƒâ‚¬ partir des profils de mai 2016, l'application dispose de **57 591 recommandations** pour **19 447 clients** :

| Recommandations par client | Nombre de clients |
|---|---:|
| 0 | 24 |
| 1 | 164 |
| 2 | 350 |
| 3 | 18 909 |

Les scores enregistrÃƒÂ©s dans le fichier CSV sont des probabilitÃƒÂ©s sur l'ÃƒÂ©chelle **0 ÃƒÂ  1** ; ils sont multipliÃƒÂ©s par 100 pour un affichage en pourcentage.

## VÃƒÂ©rification rapide aprÃƒÂ¨s lancement

1. Ouvrir la page **Recommandations**, choisir un client et un mois, puis cliquer sur **GÃƒÂ©nÃƒÂ©rer les recommandations**.
2. VÃƒÂ©rifier que les produits dÃƒÂ©jÃƒÂ  dÃƒÂ©tenus ne sont pas recommandÃƒÂ©s et que trois produits au maximum sont affichÃƒÂ©s.
3. Ouvrir **PrÃƒÂ©visions juin 2016**, sÃƒÂ©lectionner un client et vÃƒÂ©rifier l'affichage des recommandations.
4. Ouvrir **Tableau de bord** et vÃƒÂ©rifier la prÃƒÂ©sence des indicateurs d'ÃƒÂ©valuation.

Si l'application ne dÃƒÂ©marre pas, vÃƒÂ©rifier le rÃƒÂ©pertoire courant, les bibliothÃƒÂ¨ques installÃƒÂ©es et la prÃƒÂ©sence des fichiers mentionnÃƒÂ©s dans l'arborescence.

## Limites

- Ãƒâ€°chantillon limitÃƒÂ© ÃƒÂ  20 000 clients et ÃƒÂ  sept produits modÃƒÂ©lisÃƒÂ©s ;
- acquisitions rares et prÃƒÂ©cision@3 faible ;
- performances historiques qui ne garantissent pas les rÃƒÂ©sultats futurs ;
- prÃƒÂ©visions de juin 2016 non vÃƒÂ©rifiables sans donnÃƒÂ©es rÃƒÂ©elles correspondantes ;
- outil acadÃƒÂ©mique ne tenant pas lieu de validation rÃƒÂ©glementaire ou commerciale.

## RÃƒÂ©fÃƒÂ©rences

- [Kaggle Ã¢â‚¬â€ Santander Product Recommendation](https://www.kaggle.com/competitions/santander-product-recommendation)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation scikit-learn](https://scikit-learn.org/stable/)

## Licence et publication

Aucune licence logicielle n'est dÃƒÂ©finie ici. Ajouter une licence uniquement aprÃƒÂ¨s avoir choisi ses conditions et vÃƒÂ©rifiÃƒÂ© les droits de redistribution des fichiers inclus.

**Projet pÃƒÂ©dagogique INF-5103 Ã¢â‚¬â€ UQO, automne 2026.**
