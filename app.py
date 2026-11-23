import streamlit as st
import pandas as pd
import numpy as np
import joblib
import altair as alt
from pathlib import Path

st.set_page_config(page_title='BankReco', page_icon='🏦', layout='wide')
BASE_DIR = Path(__file__).resolve().parent
MOIS_FR = ['', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']


def date_fr(date):
    return f'{MOIS_FR[date.month]} {date.year}'


st.sidebar.title('🏦 BankReco')
st.sidebar.caption('Projet INF-5103')
page = st.sidebar.radio('Navigation', ['Recommandations', 'Prévisions juin 2016', 'Tableau de bord'])


@st.cache_resource
def charger_modeles():
    dossier = BASE_DIR / 'modeles'
    return (joblib.load(dossier / 'modeles_bankreco.joblib'),
            joblib.load(dossier / 'variables_X.joblib'),
            joblib.load(dossier / 'noms_produits.joblib'))


@st.cache_data
def charger_donnees():
    donnees = pd.read_csv(
        BASE_DIR / 'data' / 'santander_echantillon.csv',
        low_memory=False
    )
    donnees['fecha_dato'] = pd.to_datetime(donnees['fecha_dato'])
    return donnees


@st.cache_data
def charger_previsions():
    chemin = BASE_DIR / 'resultats' / 'predictions_juin_2016.csv'
    donnees = pd.read_csv(chemin, encoding='utf-8-sig')
    colonnes = ['ncodpers', 'Nombre_recommandations']
    for rang in range(1, 4):
        colonnes.extend([f'Produit_{rang}', f'Probabilite_{rang}'])
    absentes = [col for col in colonnes if col not in donnees.columns]
    if absentes:
        raise ValueError('Colonnes manquantes dans le fichier de prévisions : ' + ', '.join(absentes))
    if donnees['ncodpers'].duplicated().any():
        raise ValueError('Plusieurs prévisions existent pour un même identifiant client.')
    for rang in range(1, 4):
        col = f'Probabilite_{rang}'
        donnees[col] = pd.to_numeric(donnees[col], errors='coerce')
    return donnees


try:
    modeles, variables_X, noms_produits = charger_modeles()
    df = charger_donnees()
except Exception as erreur:
    st.error(f'Erreur de chargement : {erreur}')
    st.stop()

tous_produits = [col for col in df.columns if col.endswith('_ult1')]
noms_complets = {
    p: noms_produits.get(p, p.replace('_ult1', '').replace('_', ' '))
    for p in tous_produits
}


def calculer_recommandations(profil, top_n=3):
    X_client = pd.DataFrame([profil])[variables_X]
    recommandations = []
    for produit, modele in modeles.items():
        detention = pd.to_numeric(profil[produit], errors='coerce')
        if pd.isna(detention) or detention != 0:
            continue
        score = float(modele.predict_proba(X_client)[0, 1])
        recommandations.append({
            'Produit': noms_produits.get(produit, produit),
            'Probabilité (%)': score * 100
        })
    recommandations.sort(key=lambda x: x['Probabilité (%)'], reverse=True)
    return pd.DataFrame(recommandations[:top_n], columns=['Produit', 'Probabilité (%)'])


def preparer_historique(historique_client):
    historique = historique_client.sort_values('fecha_dato').copy().reset_index(drop=True)
    valeurs = historique[tous_produits].apply(pd.to_numeric, errors='coerce')
    historique['Nombre de produits'] = valeurs.eq(1).sum(axis=1)
    historique['Mois'] = historique['fecha_dato'].apply(date_fr)
    acquisitions, abandons, mouvements_detail = [], [], []
    for i in range(len(historique)):
        acquis, abandonnes = [], []
        if i > 0:
            precedent_mois = historique.loc[i - 1, 'fecha_dato'].to_period('M')
            mois = historique.loc[i, 'fecha_dato'].to_period('M')
            if (mois - precedent_mois).n == 1:
                avant, apres = valeurs.iloc[i - 1], valeurs.iloc[i]
                connus = avant.notna() & apres.notna()
                acquis = [noms_complets[p] for p in tous_produits
                          if connus[p] and avant[p] == 0 and apres[p] == 1]
                abandonnes = [noms_complets[p] for p in tous_produits
                              if connus[p] and avant[p] == 1 and apres[p] == 0]
                acquisitions.append(len(acquis))
                abandons.append(len(abandonnes))
            else:
                acquisitions.append(np.nan)
                abandons.append(np.nan)
        else:
            acquisitions.append(np.nan)
            abandons.append(np.nan)
        mouvements_detail.append({
            'Mois': historique.loc[i, 'Mois'],
            'Produits acquis': ', '.join(acquis) if acquis else '—',
            'Produits abandonnés': ', '.join(abandonnes) if abandonnes else '—',
            'Acquisitions': acquisitions[-1],
            'Abandons': abandons[-1]
        })
    historique['Acquisitions'] = acquisitions
    historique['Abandons'] = abandons
    return historique, valeurs, pd.DataFrame(mouvements_detail)


if page == 'Recommandations':
    st.title('🏦 BankReco')
    st.write('Système de recommandation personnalisée de produits bancaires — Projet INF-5103.')
    st.header('1. Sélection du client')
    identifiants = sorted(df['ncodpers'].dropna().unique())
    client_id = st.selectbox('Choisir un identifiant client', identifiants)
    historique_client = df[df['ncodpers'] == client_id].sort_values('fecha_dato')
    dates = historique_client['fecha_dato'].dropna().tolist()
    date_selectionnee = st.selectbox('Choisir le mois du profil', dates, format_func=date_fr)
    profil = historique_client[historique_client['fecha_dato'] == date_selectionnee].iloc[0]
    st.header('2. Profil bancaire')
    col1, col2, col3 = st.columns(3)
    col1.metric('Identifiant client', str(client_id))
    col2.metric('Âge', str(profil['age']))
    col3.metric('Ancienneté', str(profil['antiguedad']))
    st.subheader('Produits déjà détenus')
    produits_detenus = [noms_complets[p] for p in tous_produits
                       if pd.to_numeric(profil[p], errors='coerce') == 1]
    if produits_detenus:
        st.write(f'**{len(produits_detenus)} produits détenus**')
        for nom in produits_detenus:
            st.write('✓', nom)
    else:
        st.info('Aucun produit détenu parmi les 24 produits Santander.')
    st.header('3. Recommandations personnalisées')
    if st.button('Générer les recommandations', type='primary'):
        recommandations = calculer_recommandations(profil)
        if not recommandations.empty:
            st.success('Recommandations générées avec succès.')
            st.dataframe(recommandations, hide_index=True, width="stretch",
                         column_config={'Probabilité (%)': st.column_config.NumberColumn(
                             'Probabilité (%)', format='%.2f %%')})
            st.bar_chart(recommandations.set_index('Produit'),
                         x_label='Produit bancaire', y_label='Probabilité estimée (%)')
            st.caption('Scores estimés pour une acquisition au mois suivant ; les produits détenus sont exclus.')
        else:
            st.warning('Aucun produit admissible à recommander.')
    st.header('4. Historique bancaire du client')
    historique, valeurs, details = preparer_historique(historique_client)
    c1, c2, c3 = st.columns(3)
    c1.metric('Mois observés', len(historique))
    c2.metric('Produits au dernier mois', int(historique['Nombre de produits'].iloc[-1]))
    c3.metric('Acquisitions observées', int(historique['Acquisitions'].sum()))
    # Axe catégoriel : un repère pour CHAQUE mois observé, y compris janvier.
    # Les libellés sont en français et l'ordre est strictement chronologique.
    mois_courts = ['', 'janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin',
                   'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
    graphique = historique.copy()
    graphique['Mois affiché'] = graphique['fecha_dato'].apply(
        lambda d: f'{mois_courts[d.month]} {d.year}')
    ordre_mois = graphique['Mois affiché'].tolist()
    axe_mois = alt.X(
        'Mois affiché:N',
        sort=ordre_mois,
        title='Mois',
        axis=alt.Axis(labelAngle=-55, labelOverlap=False, labelLimit=100,
                      labelFontSize=10, labelPadding=6))

    st.subheader('Évolution du nombre de produits détenus')
    courbe = (alt.Chart(graphique)
              .mark_line(point=alt.OverlayMarkDef(filled=True, size=65))
              .encode(
                  x=axe_mois,
                  y=alt.Y('Nombre de produits:Q', title='Nombre de produits',
                          scale=alt.Scale(zero=True)),
                  tooltip=[alt.Tooltip('Mois:N', title='Mois complet'),
                           alt.Tooltip('Nombre de produits:Q', title='Produits détenus')])
              .properties(height=360))
    st.altair_chart(courbe, use_container_width=True)
    st.caption('Chaque point représente un mois observé, de janvier 2015 à mai 2016 '
               'pour un client disposant de tout cet historique.')

    st.subheader('Acquisitions et abandons mensuels')
    mouvements_graphique = graphique.melt(
        id_vars=['Mois affiché', 'Mois'],
        value_vars=['Acquisitions', 'Abandons'],
        var_name='Mouvement', value_name='Nombre')
    barres = (alt.Chart(mouvements_graphique)
              .mark_bar()
              .encode(
                  x=axe_mois,
                  y=alt.Y('Nombre:Q', title='Nombre de produits'),
                  xOffset=alt.XOffset('Mouvement:N', sort=['Acquisitions', 'Abandons']),
                  color=alt.Color('Mouvement:N', title='Type de mouvement'),
                  tooltip=[alt.Tooltip('Mois:N', title='Mois complet'),
                           'Mouvement:N', alt.Tooltip('Nombre:Q', title='Nombre')])
              .properties(height=310))
    st.altair_chart(barres, use_container_width=True)
    st.caption('Les mouvements sont calculés uniquement entre deux mois consécutifs, sur les valeurs connues.')
    st.subheader('5. Quels produits ont été acquis ou abandonnés ?')
    mouvements_observes = details[(details['Acquisitions'].fillna(0) > 0) |
                                 (details['Abandons'].fillna(0) > 0)]
    if mouvements_observes.empty:
        st.info('Aucun changement de produit observé entre les mois consécutifs disponibles.')
    else:
        st.dataframe(mouvements_observes[['Mois', 'Produits acquis', 'Produits abandonnés']],
                     hide_index=True, width="stretch")
    with st.expander('Afficher tous les mois, y compris sans mouvement'):
        st.dataframe(details, hide_index=True, width="stretch")
    st.subheader('6. Matrice mensuelle des produits')
    matrice = valeurs.copy()
    matrice.columns = [noms_complets[p] for p in tous_produits]
    matrice.index = historique['Mois']
    st.dataframe(matrice, width="stretch")
    st.caption('1 = détenu ; 0 = non détenu ; cellule vide = information manquante.')
    st.subheader('Résumé mensuel du portefeuille')
    st.dataframe(historique[['Mois', 'Nombre de produits', 'Acquisitions', 'Abandons']],
                 hide_index=True, width="stretch")

elif page == 'Prévisions juin 2016':
    st.title('🔮 Prévisions des acquisitions — Juin 2016')
    st.write('Recommandations prospectives calculées à partir des profils bancaires de mai 2016.')
    try:
        previsions = charger_previsions()
    except Exception as erreur:
        st.error(f'Impossible de charger les prévisions : {erreur}')
        st.info('Vérifie la présence de resultats/predictions_juin_2016.csv dans le dossier BankReco.')
        st.stop()

    st.header('1. Synthèse des prévisions')
    total_clients = len(previsions)
    total_recommandations = int(previsions['Nombre_recommandations'].sum())
    clients_sans_recommandation = int((previsions['Nombre_recommandations'] == 0).sum())
    c1, c2, c3 = st.columns(3)
    c1.metric('Clients analysés', f'{total_clients:,}'.replace(',', ' '))
    c2.metric('Recommandations générées', f'{total_recommandations:,}'.replace(',', ' '))
    c3.metric('Clients sans recommandation', clients_sans_recommandation)

    st.header('2. Prévisions individuelles')
    identifiants = sorted(previsions['ncodpers'].dropna().unique())
    client_id = st.selectbox('Choisir un client', identifiants, key='client_prevision')
    client = previsions.loc[previsions['ncodpers'] == client_id].iloc[0]
    st.subheader(f'Produits recommandés pour le client {client_id}')
    recommandations_client = []
    for rang in range(1, 4):
        produit = client[f'Produit_{rang}']
        probabilite = client[f'Probabilite_{rang}']
        if pd.notna(produit) and pd.notna(probabilite):
            recommandations_client.append({
                'Rang': rang,
                'Produit': produit,
                'Probabilité (%)': float(probabilite) * 100
            })
    tableau_client = pd.DataFrame(recommandations_client,
                                  columns=['Rang', 'Produit', 'Probabilité (%)'])
    if tableau_client.empty:
        st.info('Aucun produit admissible à recommander pour ce client.')
    else:
        st.dataframe(tableau_client, hide_index=True, width="stretch",
                     column_config={'Probabilité (%)': st.column_config.NumberColumn(
                         'Probabilité (%)', format='%.2f %%')})
        st.bar_chart(tableau_client.set_index('Produit')[['Probabilité (%)']],
                     x_label='Produit bancaire', y_label="Probabilité d'acquisition (%)")
    st.caption('Les probabilités correspondent à des estimations, et non à des acquisitions confirmées.')

    st.header('3. Répartition des recommandations')
    repartition = (previsions['Nombre_recommandations'].value_counts()
                  .reindex(range(4), fill_value=0).sort_index()
                  .rename_axis('Nombre de recommandations')
                  .reset_index(name='Nombre de clients'))
    st.bar_chart(repartition.set_index('Nombre de recommandations'),
                 x_label='Nombre de recommandations', y_label='Nombre de clients')
    st.dataframe(repartition, hide_index=True, width="stretch")

    st.header('4. Tableau des prévisions')
    st.dataframe(previsions, hide_index=True, width="stretch",
                 column_config={f'Probabilite_{rang}': st.column_config.NumberColumn(
                     f'Probabilité {rang} (0–1)', format='%.6f') for rang in range(1, 4)})
    st.header('5. Exporter les prévisions')
    fichier_csv = previsions.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
    st.download_button('📥 Télécharger les prévisions de juin 2016', data=fichier_csv,
                       file_name='BankReco_previsions_juin_2016.csv', mime='text/csv')
    st.info('Les acquisitions réelles de juin 2016 ne figurent pas dans les données : '
            'aucune mesure de précision ou de rappel pour juin ne peut être calculée.')

elif page == 'Tableau de bord':
    st.title('📊 Tableau de bord BankReco')
    st.write('Évaluation sur les acquisitions d’avril et mai 2016.')
    st.subheader('Performances globales')
    c1, c2, c3 = st.columns(3)
    c1.metric('Précision globale@3', '1,115 %')
    c2.metric('Rappel global@3', '90,50 %')
    c3.metric('Taux de réussite@3 (Hit Rate)', '95,29 %')
    st.subheader('Comparaison avec le modèle de popularité')
    comparaison = pd.DataFrame({
        'Indicateur': ['Précision globale@3', 'Rappel global@3', 'Hit Rate@3'],
        'BankReco': [1.1149, 90.4965, 95.2941],
        'Popularité': [0.9874, 80.1418, 85.1584]
    })
    st.dataframe(comparaison, hide_index=True, width="stretch")
    st.bar_chart(comparaison.set_index('Indicateur'),
                 x_label='Indicateur', y_label='Performance (%)', stack=False)
    st.subheader('Validation statistique du gain de rappel')
    st.metric('Gain observé', '+10,355 points')
    st.write('**Intervalle de confiance bootstrap à 95 % :** [8,459 ; 12,343] points de pourcentage.')
    st.info('L’intervalle est entièrement positif. Cette analyse reste exploratoire.')
    st.subheader('Données d’évaluation')
    c1, c2 = st.columns(2)
    c1.metric('Clients distincts', '19 411')
    c2.metric('Observations client-mois', '38 701')
    c3, c4 = st.columns(2)
    c3.metric('Acquisitions évaluables', '1 410')
    c4.metric('Recommandations correctes', '1 276')
    st.caption('Indicateurs calculés dans 03_modelisation.ipynb.')
