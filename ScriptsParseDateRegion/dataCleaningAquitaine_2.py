import numpy as np
import pandas as pd

# This file will generate a step 2 clean csv dataset from the dataAquitaine_1 CSV

#########################################################################################################
# Import CSV and remove first column
df_dataAquitaine = pd.read_csv("/home/alauzettho/BOAMP/ScriptsParseDateRegion/dataAquitaine_1.csv")
print('------------------- DATA AQUITAINE IMPORTED -------------------')


#########################################################################################################
# Remove Index that we know contains useless data
listIndexToDrop = [ 'Unnamed: 0', 'CRITERE_SELECTION', 'POUVOIR_ADJUDICATEUR.AUTRE', 'AUTRES_CONDITIONS_PART_OUI',
                    'ADRESSES_COMPLEMENTAIRES.ADRESSE.DENOMINATION', 'NB_LOT_OFFRE_MAX', 'DECISION.DESCRIPTION',
                    'ADRESSES_COMPLEMENTAIRES.ADRESSE.CP', 'DENOMINATION', 'INFO_COMPLEMENTAIRE', 'DELEGATION.DATE_DEBUT',
                    'LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_COUT.CRITERE.@POIDS', 'DATE_FIN',
                    'LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_COUT.CRITERE.#text', 'DATE_LANCEMENT',
                    'LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_COUT.CRITERE', 'DECISION.NUM_MARCHE',
                    'LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_QUALITE.CRITERE.#text', 'DECISION.TITULAIRE.CORRESPONDANT',
                    'LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_QUALITE.CRITERE', 'DECISION.INTITULE',
                    'FORME_JURIDIQUE', 'CONDITIONS_REMISE_OFFRES', 'CONDITIONS_ET_MODE_PAIEMENT_OBTENIR_DOCUMENTS',
                    'DECISION.RENSEIGNEMENT.SOUSTRAITANCE_OUI.VALEUR.COUT', 'DECISION.RENSEIGNEMENT.OFFRE_BASSE.COUT',
                    'DECISION.RENSEIGNEMENT.OFFRE_ELEVEE.COUT', 'DECISION.RENSEIGNEMENT.NB_OFFRE_RECU_ELECT',
                    'DECISION.RENSEIGNEMENT.CONCOURS_PRIME.COUT', 'DECISION.TITULAIRE.DENOMINATION',
                    'LOTS.LOT.DESCRIPTION', 'DECISION.RENSEIGNEMENT.NB_OFFRE_RECU_NON_UE',
                    'LOTS.LOT.RENOUVELLEMENT_DESCRIPTION', 'DECISION.RENSEIGNEMENT.NB_OFFRE_RECU_UE',
                    'LOTS.LOT.OPTIONS_DESCRIPTION', 'DECISION.RENSEIGNEMENT.NB_OFFRE_RECU_PME',
                    'DECISION.RENSEIGNEMENT.SOUSTRAITANCE_OUI.DESCRIPTION']


df_dataAquitaine = df_dataAquitaine.drop(columns = listIndexToDrop)
print(df_dataAquitaine.shape)


#########################################################################################################
# Things Interesting we have to drop (saisie libre ou autre)
listIndexToDrop = [ 'PRESTATION_RESERVEE_OUI', 'DEP_PRESTATION', 'DEP_PUBLICATION', 'DECISION.TITULAIRE',
                    'LIEU_OUVERTURE_OFFRES', 'CAUTIONNEMENT', 'FINANCEMENT', 'DECISION.TITULAIRE.CP',
                    'CAP_ECO', 'TITRE_MARCHE', 'REF_MARCHE', 'RECEPT_OFFRES', 'DECISION', 'DUREE_DELAI.DATE_EXECUTION',
                    'CAP_ECO_NIVEAU_MINI', 'REFERENCE_PUBLICATION.PUBLICATION_JOUE.DATE_PUBLICATION',
                    'REFERENCE_PUBLICATION.PUBLICATION_JOUE.NUM_PARUTION', 'DECISION.TITULAIRE.PAYS',
                    'REFERENCE_PUBLICATION.PUBLICATION_JOUE.NUM_ANNONCE', 'DECISION.NUM_LOT',
                    'CAP_TECH', 'CORRESPONDANT', 'CODE_IDENT_NATIONAL', 'REFERENCE_MARCHE',
                    'CAP_TECH_NIVEAU_MINI', 'TYPE_MARCHE.SERVICE', 'DUREE_DELAI.DATE_DEBUT', 'DUREE_DELAI.DATE_FIN',
                    'LOTS.LOT.DATE_DEBUT', 'LOTS.LOT.DATE_FIN', 'DUREE_DELAI.DATE_LIVRAISON',
                    'ACCORD_CADRE.VALEUR_MIN.COUT', 'ACCORD_CADRE.VALEUR_MAX.COUT',
                    'CARACTERISTIQUES.VALEUR_MIN.COUT', 'CARACTERISTIQUES.VALEUR_MAX.COUT']

df_dataAquitaine = df_dataAquitaine.drop(columns = listIndexToDrop)
print(df_dataAquitaine.shape)


#########################################################################################################
# CP

df_dataAquitaine = df_dataAquitaine.dropna(subset = ['CP'], axis = 0)
df_dataAquitaine['CP'] = df_dataAquitaine['CP'].astype(int)


#########################################################################################################
# Vocabulaire commun pour les marchés : CPV

df_classe1 = df_dataAquitaine[['CPV','IDWEB']].dropna(axis = 0)

CodeArray1 = []

for i in range(0, len(df_classe1.index)) :
    values = df_classe1['CPV'].iloc[i].split('OrderedDict')[1].split(',')
    CODE = values[1].replace(')', '').replace(']', '').replace('"', '').replace("'", '')
    CodeArray1.append(CODE)

df_classe1['CPV.PRINCIPAL'] = CodeArray1
df_dataAquitaine['CPV.PRINCIPAL'] = df_dataAquitaine['CPV.PRINCIPAL'].fillna(df_classe1['CPV.PRINCIPAL']).fillna(0)

df_dataAquitaine = df_dataAquitaine.drop(columns = ['LOTS.LOT.CPV.PRINCIPAL', 'LOTS.LOT.CPV.SUPPLEMENTAIRE', 'CPV.SUPPLEMENTAIRE', 'LOTS.LOT.CPV', 'CPV'])
df_dataAquitaine = df_dataAquitaine.rename(columns = {'CPV.PRINCIPAL' : 'CPV'})
df_dataAquitaine['CPV'].replace(0, np.nan, inplace = True)
df_dataAquitaine['CPV'] = df_dataAquitaine['CPV'].fillna(0).astype(int)


#########################################################################################################
# DESCRIPTEURS

df_classe1 = df_dataAquitaine[['DESCRIPTEURS.DESCRIPTEUR','IDWEB']].dropna(axis = 0)

CodeArray = []
LibeArray = []

for i in range(0, len(df_classe1.index)) :
    values = df_classe1['DESCRIPTEURS.DESCRIPTEUR'].iloc[i].split('OrderedDict')[1].split(',')
    CODE = values[1].replace(')', '').replace(']', '').replace('"', '').replace("'", '')
    LIBE = values[3].replace(')', '').replace(']', '').replace('"', '').replace("'", '')[1:]
    CodeArray.append(CODE)
    LibeArray.append(LIBE)

df_classe1['DESCRIPTEURS.DESCRIPTEUR.CODE'] = CodeArray
df_classe1['DESCRIPTEURS.DESCRIPTEUR.LIBELLE'] = LibeArray
df_dataAquitaine['DESCRIPTEURS.DESCRIPTEUR.CODE'] = df_dataAquitaine['DESCRIPTEURS.DESCRIPTEUR.CODE'].fillna(df_classe1['DESCRIPTEURS.DESCRIPTEUR.CODE']).astype(int)
df_dataAquitaine['DESCRIPTEURS.DESCRIPTEUR.LIBELLE'] = df_dataAquitaine['DESCRIPTEURS.DESCRIPTEUR.LIBELLE'].fillna(df_classe1['DESCRIPTEURS.DESCRIPTEUR.LIBELLE'])

df_dataAquitaine = df_dataAquitaine.drop(columns = 'DESCRIPTEURS.DESCRIPTEUR')
df_dataAquitaine = df_dataAquitaine.rename(columns = {'DESCRIPTEURS.DESCRIPTEUR.CODE' : 'DESCRIPTEUR_CODE', 'DESCRIPTEURS.DESCRIPTEUR.LIBELLE' : 'DESCRIPTEUR_LIBELLE'})


#########################################################################################################
# ACCORD_CADRE

df_dataAquitaine['ACCORD_CADRE.DUREE_MOIS'] = df_dataAquitaine['ACCORD_CADRE.DUREE_MOIS'].fillna(df_dataAquitaine['ACCORD_CADRE.DUREE_AN']*12)
df_dataAquitaine = df_dataAquitaine.drop(columns = 'ACCORD_CADRE.DUREE_AN')

df_dataAquitaine['CLASSES.CLASSE.CODE'] = df_dataAquitaine['CLASSES.CLASSE.CODE'].replace(0.0, np.nan)
df_dataAquitaine['ACCORD_CADRE.VALEUR.COUT'] = df_dataAquitaine['ACCORD_CADRE.VALEUR.COUT'].replace(0.0, np.nan)
print(df_dataAquitaine.shape)

#########################################################################################################
# CRITERES_ATTRIBUTION

# LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_PRIX.POIDS
# LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_QUALITE.CRITERE.@POIDS
# CRITERES_ATTRIBUTION.CRITERES_PONDERES.CRITERE
# CRITERES_ATTRIBUTION.CRITERES_PRIORITES.CRITERE
# CRITERES_ATTRIBUTION.CRITERES_LIBRE
# Devient
# CRITERES_ATTRIBUTION_1 et CRITERES_ATTRIBUTION_2


# I) Clean CRITERES_ATTRIBUTION.CRITERES_PONDERES.CRITERE

df_classe1 = df_dataAquitaine[['CRITERES_ATTRIBUTION.CRITERES_PONDERES.CRITERE','IDWEB']].dropna(axis = 0)

CRIT_1_ARRAY = []
CRIT_2_ARRAY = []

for i in range(0, len(df_classe1.index)) :
    values = df_classe1['CRITERES_ATTRIBUTION.CRITERES_PONDERES.CRITERE'].iloc[i].replace(']', '').replace('"', '').replace('[', '')
    value1 = values.split('OrderedDict')[1].split(',')
    value2 = values.split('OrderedDict')[2].split(',')
    CRIT1P = int(value1[1].replace(')', '').replace(']', '').replace('"', '').replace("'", ''))
    CRIT2P = int(value2[1].replace(')', '').replace(']', '').replace('"', '').replace("'", ''))
    CRIT1T = (value1[3].replace(')', '').replace(']', '').replace('"', '').replace("'", '')[1:])
    CRIT2T = (value2[3].replace(')', '').replace(']', '').replace('"', '').replace("'", '')[1:])
    if CRIT1P < CRIT2P :
        CRIT_1_ARRAY.append(CRIT2T)
        CRIT_2_ARRAY.append(CRIT1T)
    else :
        CRIT_1_ARRAY.append(CRIT1T)
        CRIT_2_ARRAY.append(CRIT2T)


# Concat resuls on main df
df_classe1['CRITERES_ATTRIBUTION_1'] = CRIT_1_ARRAY
df_classe1['CRITERES_ATTRIBUTION_2'] = CRIT_2_ARRAY
df_classe1 = df_classe1.drop(columns = ['CRITERES_ATTRIBUTION.CRITERES_PONDERES.CRITERE', 'IDWEB'])
df_dataAquitaine = pd.concat([df_dataAquitaine, df_classe1], axis = 1)
df_dataAquitaine = df_dataAquitaine.drop(columns = 'CRITERES_ATTRIBUTION.CRITERES_PONDERES.CRITERE')


# II) Clean CRITERES_ATTRIBUTION.CRITERES_PRIORITES.CRITERE

df_classe1 = df_dataAquitaine[['CRITERES_ATTRIBUTION.CRITERES_PRIORITES.CRITERE','IDWEB']].dropna(axis = 0)

CRIT_1_ARRAY = []
CRIT_2_ARRAY = []

for i in range(0, len(df_classe1.index)) :
    values = df_classe1['CRITERES_ATTRIBUTION.CRITERES_PRIORITES.CRITERE'].iloc[i].replace(']', '').replace('"', '').replace('[', '')
    value1 = values.split('OrderedDict')[1].split(',')
    value2 = values.split('OrderedDict')[2].split(',')
    CRIT1T = (value1[3].replace(')', '').replace(']', '').replace('"', '').replace("'", '')[1:])
    CRIT2T = (value2[3].replace(')', '').replace(']', '').replace('"', '').replace("'", '')[1:])
    CRIT_1_ARRAY.append(CRIT1T)
    CRIT_2_ARRAY.append(CRIT2T)

# Merge resuls on main df
df_classe1['CRITERES_ATTRIBUTION_1'] = CRIT_1_ARRAY
df_classe1['CRITERES_ATTRIBUTION_2'] = CRIT_2_ARRAY
df_classe1 = df_classe1.drop(columns = ['CRITERES_ATTRIBUTION.CRITERES_PRIORITES.CRITERE', 'IDWEB'])
df_dataAquitaine = df_dataAquitaine.drop(columns = 'CRITERES_ATTRIBUTION.CRITERES_PRIORITES.CRITERE')
df_dataAquitaine['CRITERES_ATTRIBUTION_1'] = df_dataAquitaine['CRITERES_ATTRIBUTION_1'].fillna(df_classe1['CRITERES_ATTRIBUTION_1'])
df_dataAquitaine['CRITERES_ATTRIBUTION_2'] = df_dataAquitaine['CRITERES_ATTRIBUTION_2'].fillna(df_classe1['CRITERES_ATTRIBUTION_2'])


# III) CRITERES_ATTRIBUTION.CRITERES_LIBRE

df_dataAquitaine = df_dataAquitaine.drop(columns = 'CRITERES_ATTRIBUTION.CRITERES_LIBRE')


# IV) Export data for training NN
# df_criteres = pd.DataFrame()
# df_criteres['CRITERE'] = pd.concat([df_dataAquitaine['CRITERES_ATTRIBUTION_1'].dropna(), df_dataAquitaine['CRITERES_ATTRIBUTION_2'].dropna()], axis = 0, ignore_index = True) 
# df_criteres = df_criteres[df_criteres['CRITERE'] != "Prix"]
# df_criteres['PRIX']         = 0
# df_criteres['TECHNIQUE']    = 0
# df_criteres['QUALITE']      = 0
# df_criteres['DELAI']        = 0
# df_criteres['AUTRE']        = 0
# df_criteres = df_criteres.sample(n = 250)
# df_criteres.to_csv("critere_attribution_train_bis.csv")


# V) Export CRITERES_ATTRIBUTION_1 and CRITERES_ATTRIBUTION_2
# df_criteres = df_dataAquitaine[['CRITERES_ATTRIBUTION_1', 'CRITERES_ATTRIBUTION_2']].dropna(axis = 0)
# df_criteres.to_csv("NN/critere_attribution_data.csv")


# VI) Import new data from NN
df_critere = pd.read_csv("/home/alauzettho/BOAMP/NN/critere_attribution_classified.csv")
df_critere = df_critere.set_index('Unnamed: 0')

df_dataAquitaine['CRITERES_ATTRIBUTION_1'] = df_critere['CRITERES_ATTRIBUTION_1']
df_dataAquitaine['CRITERES_ATTRIBUTION_2'] = df_critere['CRITERES_ATTRIBUTION_2']


# VII) LOTS

df_dataAquitaine = df_dataAquitaine.rename(columns = { \
    'LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_PRIX.POIDS' : 'CRITERES_PRIX', \
    'LOTS.LOT.CRITERES_ATTRIBUTION.CRITERES_QUALITE.CRITERE.@POIDS' : 'CRITERES_QUAL'})

df_dataAquitaine['CRITERES_PRIX'] = pd.to_numeric(df_dataAquitaine['CRITERES_PRIX'], errors = 'coerce').fillna(0).astype(int)
df_dataAquitaine['CRITERES_QUAL'] = pd.to_numeric(df_dataAquitaine['CRITERES_QUAL'], errors = 'coerce').fillna(0).astype(int)


for i in range(0, len(df_dataAquitaine.index)) :
    prix = df_dataAquitaine['CRITERES_PRIX'].iloc[i]
    qual = df_dataAquitaine['CRITERES_QUAL'].iloc[i]
    
    if (prix > qual and qual > 0) :
        df_dataAquitaine.iloc[i, df_dataAquitaine.columns.get_loc('CRITERES_ATTRIBUTION_1')] = "PRIX"
        df_dataAquitaine.iloc[i, df_dataAquitaine.columns.get_loc('CRITERES_ATTRIBUTION_2')] = "QUALITE"
    if (qual > prix and prix > 0) :
        df_dataAquitaine.iloc[i, df_dataAquitaine.columns.get_loc('CRITERES_ATTRIBUTION_1')] = "QUALITE"
        df_dataAquitaine.iloc[i, df_dataAquitaine.columns.get_loc('CRITERES_ATTRIBUTION_2')] = "PRIX"

df_dataAquitaine = df_dataAquitaine.drop(columns = ['CRITERES_PRIX', 'CRITERES_QUAL'])
print(df_dataAquitaine.shape)


#########################################################################################################
# COUT

df_dataAquitaine['VALEUR_TOTALE.COUT'] = df_dataAquitaine['VALEUR_TOTALE.COUT'].\
    fillna(df_dataAquitaine['CARACTERISTIQUES.VALEUR_TOTALE.COUT']).\
    fillna(df_dataAquitaine['DECISION.RENSEIGNEMENT.MONTANT.COUT']).\
    fillna(df_dataAquitaine['LOTS.LOT.VALEUR.COUT']).\
    fillna(df_dataAquitaine['ACCORD_CADRE.VALEUR.COUT']).\
    fillna(df_dataAquitaine['CARACTERISTIQUES.VALEUR.COUT'])

df_dataAquitaine = df_dataAquitaine.drop(columns = ['CARACTERISTIQUES.VALEUR.COUT', 'LOTS.LOT.VALEUR.COUT', 'CARACTERISTIQUES.VALEUR_TOTALE.COUT', 'DECISION.RENSEIGNEMENT.MONTANT.COUT', 'ACCORD_CADRE.VALEUR.COUT'])
df_dataAquitaine = df_dataAquitaine.drop(index = df_dataAquitaine[df_dataAquitaine['VALEUR_TOTALE.COUT'] < 100].index)
df_dataAquitaine = df_dataAquitaine.rename(columns = {'DECISION.RENSEIGNEMENT.ESTIMATION_INITIALE.COUT' : 'ESTIMATION_INITIALE', 'VALEUR_TOTALE.COUT' : 'VALEUR_TOTALE'})
print(df_dataAquitaine.shape)


#########################################################################################################
# Generate Step 2 file

fileName = "/home/alauzettho/BOAMP/ScriptsParseDateRegion/dataAquitaine_2.csv"
df_dataAquitaine.to_csv(fileName)