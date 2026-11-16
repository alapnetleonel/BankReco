
from pathlib import Path
import importlib.metadata as metadata

BASE_DIR = Path(__file__).resolve().parent

print("=== Vérification du projet BankReco ===")

fichiers = [
    "app.py",
    "README.md",
    "requirements.txt",
    "data/santander_echantillon.csv",
    "modeles/modeles_bankreco.joblib",
    "modeles/variables_X.joblib",
    "modeles/noms_produits.joblib",
    "resultats/predictions_juin_2016.csv",
]

print("\n1. Vérification des fichiers")

manquants = []

for fichier in fichiers:
    chemin = BASE_DIR / fichier
    if chemin.is_file():
        print(f"[OK] {fichier}")
    else:
        print(f"[MANQUANT] {fichier}")
        manquants.append(fichier)

print("\n2. Versions des bibliothèques")

for paquet in [
    "streamlit",
    "pandas",
    "numpy",
    "scikit-learn",
    "joblib"
]:
    try:
        print(f"{paquet}: {metadata.version(paquet)}")
    except metadata.PackageNotFoundError:
        print(f"{paquet}: NON INSTALLÉ")

print("\n3. Résultat")

if manquants:
    print(f"{len(manquants)} fichier(s) manquant(s).")
else:
    print("Tous les fichiers attendus sont présents.")

print(
    "\nAttention : ce contrôle ne teste pas encore "
    "le chargement des modèles ni les prédictions."
)
