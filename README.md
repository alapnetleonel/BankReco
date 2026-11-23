# 🏦 BankReco — Système de recommandation de produits bancaires

**Projet de session INF-5103 — Concepts statistiques pour la science des données**  
**Université du Québec en Outaouais (UQO) — Automne 2026**  
**Auteur :** Leonel Alapnet Zébazé

## 1. Présentation

**BankReco** est une application académique Python/Streamlit qui propose jusqu'à **trois produits bancaires** qu'un client pourrait acquérir le mois suivant, à partir de son profil et de son historique de détention. Le destinataire représentatif est un responsable du marketing et de la relation clientèle d'une banque de détail. BankReco n'est pas un service officiel de Santander et ne constitue pas un outil de décision bancaire en production.

L'application comprend trois pages :

- **Recommandations** : sélection d'un client et d'un mois, produits détenus, Top 3 personnalisé, probabilités estimées, évolution du portefeuille, acquisitions/abandons et matrice mensuelle.
- **Prévisions juin 2016** : recommandations calculées à partir des profils de mai 2016, consultation par client, graphiques, tableau et export CSV.
- **Tableau de bord** : indicateurs d'évaluation sur avril–mai 2016, comparaison à une méthode fondée sur la popularité et intervalle de confiance bootstrap exploratoire.

## 2. Lancement en une commande

**Une fois Python, les dépendances et les fichiers requis installés**, ouvrir un terminal dans le dossier racine `BankReco` avec le bon environnement Python activé, puis exécuter :

```powershell
python -m streamlit run app.py
```

Ouvrir l'adresse locale affichée par Streamlit (généralement <http://localhost:8501>). Arrêter le serveur avec `Ctrl+C`.

> Cette commande lance l'application ; la préparation initiale d'un nouvel ordinateur est décrite ci-dessous.

## 3. Installation initiale sur Windows PowerShell

### Prérequis

- Windows avec **Python 3.14** installé (version validée : **3.14.6**) et accessible par `py -3.14` ;
- connexion Internet pour l'installation initiale des dépendances ;
- fichiers de données, de prévisions et modèles aux emplacements indiqués à la section 4.

Ouvrir PowerShell dans le dossier `BankReco` téléchargé ou cloné, puis exécuter :

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe verification_bankreco.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Ces commandes utilisent directement Python dans `.venv`. Pour utiliser ensuite la commande unique de la section 2, activer l'environnement dans un terminal autorisant l'activation :

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

Si la politique PowerShell empêche l'activation, utiliser sans la modifier :

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Les versions directes épinglées dans `requirements.txt`, testées sur Windows/Python 3.14, sont :

| Bibliothèque | Version |
|---|---:|
| Streamlit | 1.67.0 |
| pandas | 3.1.1 |
| NumPy | 2.5.4 |
| scikit-learn | **1.9.1** |
| joblib | 1.6.0 |

**Compatibilité des modèles :** les fichiers `.joblib` ont été enregistrés avec scikit-learn **1.9.1**. Une autre version peut produire des avertissements ou des résultats incompatibles. Ne charger que des fichiers `.joblib` provenant d'une source de confiance.

## 4. Structure du projet

```text
BankReco/
├── .gitignore
├── README.md
├── requirements.txt
├── verification_bankreco.py
├── app.py
├── 03_modelisation.ipynb             # Notebook principal
├── notebooks/
│   ├── 01_exploration_donnees.ipynb
│   └── 02_preparation_donnees.ipynb
├── data/
│   └── santander_echantillon.csv     
├── modeles/
│   ├── modeles_bankreco.joblib
│   ├── variables_X.joblib
│   └── noms_produits.joblib
└── resultats/
    └── predictions_juin_2016.csv
```

### Important : disponibilité des données

L'application lit obligatoirement `data/santander_echantillon.csv` (environ **46,41 Mo**).
Le script `verification_bankreco.py` vérifie la présence des fichiers et affiche les versions installées. **Il ne vérifie pas à lui seul les prédictions ni l'exactitude statistique des résultats.**

## 5. Données et méthode statistique

**Source :** jeu de données [Santander Product Recommendation (Kaggle)](https://www.kaggle.com/competitions/santander-product-recommendation).

L'échantillon de travail comprend **285 734 observations**, **20 000 clients**, **17 mois** (janvier 2015 à mai 2016) et **24 indicateurs de détention de produits**.

Sept produits sont modélisés : prélèvements automatiques, domiciliation de pension, domiciliation de salaire, compte courant, carte de crédit, compte de paie et E-account.

BankReco utilise **sept modèles de régression logistique calibrés**, un par produit, pour estimer l'acquisition au mois suivant. Les variables comprennent des caractéristiques des clients et leurs produits détenus. Les produits déjà détenus ou dont le statut est inconnu sont exclus du classement.

Le découpage est temporel : entraînement sur **2015**, calibration sur **janvier–février 2016** et évaluation sur les mois ultérieurs. Les résultats du tableau de bord concernent **avril–mai 2016**. Le notebook `03_modelisation.ipynb` documente la démarche de modélisation.

## 6. Résultats expérimentaux

| Indicateur | BankReco | Popularité |
|---|---:|---:|
| Précision globale@3 | 1,115 % | 0,987 % |
| Rappel global@3 | 90,50 % | 80,14 % |
| Hit Rate@3 | 95,29 % | 85,16 % |

L'évaluation porte sur **38 701 observations client-mois**, **19 411 clients distincts** et **1 410 acquisitions évaluables**. Sur **114 445 recommandations**, **1 276** correspondent à des acquisitions observées.

Le gain observé de rappel global@3 par rapport à la popularité est d'environ **10,35 points de pourcentage**. Un bootstrap exploratoire de **2 000 rééchantillonnages** donne un intervalle de confiance à 95 % de **[8,459 ; 12,343] points**. Ces résultats historiques ne garantissent pas la performance future ; la précision reste faible.

## 7. Prévisions pour juin 2016

À partir des profils de mai 2016, le fichier `resultats/predictions_juin_2016.csv` contient **57 591 recommandations** pour **19 447 clients**.

| Nombre de recommandations | Nombre de clients |
|---|---:|
| 0 | 24 |
| 1 | 164 |
| 2 | 350 |
| 3 | 18 909 |

Les probabilités du CSV sont enregistrées entre **0 et 1** et converties en pourcentages dans l'interface. Les acquisitions réelles de juin 2016 ne sont pas disponibles dans cet échantillon : **aucune performance réelle de juin ne peut être calculée**.

## 8. Vérification de fonctionnement

1. Lancer `verification_bankreco.py` et vérifier que les fichiers requis sont présents.
2. Lancer Streamlit ; ouvrir **Recommandations**, choisir un client et un mois, puis cliquer sur **Générer les recommandations**.
3. Vérifier que les produits détenus sont exclus et que le Top 3 contient au plus trois produits.
4. Consulter l'historique, les acquisitions/abandons et la matrice mensuelle.
5. Ouvrir **Prévisions juin 2016**, afficher les prévisions d'un client et tester l'export CSV.
6. Ouvrir **Tableau de bord** et vérifier l'affichage des indicateurs.

L'installation des dépendances, le chargement des **sept modèles** et le démarrage de Streamlit ont été validés sous Windows/Python 3.14.6 dans un environnement virtuel neuf. Cela **ne remplace pas** un essai de clonage et d'exécution sur un autre ordinateur.

## 9. Limites et précautions

- Échantillon de 20 000 clients et seulement sept produits modélisés parmi 24 indicateurs ;
- événements d'acquisition rares et précision@3 faible ;
- généralisation à d'autres périodes ou banques non démontrée ;
- absence de données réelles de juin 2016 pour valider les prévisions correspondantes ;
- nécessité de contrôler les droits de redistribution des données et les informations éventuellement présentes dans les notebooks et exports ;
- application académique, sans validation réglementaire ou déploiement en production.

## 10. Références

- [Kaggle — Santander Product Recommendation](https://www.kaggle.com/competitions/santander-product-recommendation)
- [Streamlit — Documentation](https://docs.streamlit.io/)
- [scikit-learn — Documentation](https://scikit-learn.org/stable/)

## 11. Publication

 **Lien GitHub : (https://github.com/alapnetleonel/BankReco).**

*Projet pédagogique INF-5103 — UQO, automne 2026.*
