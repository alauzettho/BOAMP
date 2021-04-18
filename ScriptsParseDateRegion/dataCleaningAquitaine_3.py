import pandas as pd
import numpy as np

# This file will generate a step 3 clean csv dataset from the dataAquitaine_2 CSV

#########################################################################################################
# Import CSV and remove first column
df_dataAquitaine = pd.read_csv("/home/alauzettho/BOAMP/ScriptsParseDateRegion/dataAquitaine_2.csv")
print('------------------- DATA AQUITAINE IMPORTED -------------------')


#########################################################################################################
# Remove Index that we know contains useless data
listIndexToDrop = [ 'Unnamed: 0', 'RENS_COMPLEMENT', 'OBJET_COMPLET', 'LOTS.LOT.LIEU_PRINCIPAL', 'LOTS.LOT.INFO_COMPL',
                    'CARACTERISTIQUES.RECONDUCTIONS.DUREE_MOIS', 'CARACTERISTIQUES.RECONDUCTIONS.CALENDRIER',
                    'LOTS.LOT.INTITULE', 'CARACTERISTIQUES.QUANTITE', 'CARACTERISTIQUES.PRINCIPALES',
                    'CONDITION_PARTICULIERE_EXECUTION', 'NB_CANDIDATS.LIMITATION_CANDIDATS',
                    'NB_CANDIDATS.NB_MIN_OFFRE', 'LOTS.LOT', 'LOTS.LOT.NUM',
                    'NB_CANDIDATS.NB_MAX_OFFRE', 'DATE_DECISION',
                    'NB_CANDIDATS.NB_OFFRE']

df_dataAquitaine = df_dataAquitaine.drop(columns = listIndexToDrop)
print(df_dataAquitaine.shape)


#########################################################################################################
# Format
df_dataAquitaine = df_dataAquitaine.rename(columns = {\
    'CARACTERISTIQUES.RECONDUCTIONS.NB_RECONDUCTIONS' : 'NB_RECONDUCTIONS',
    'DECISION.RENSEIGNEMENT.NB_OFFRE_RECU' : 'NB_OFFRE_RECU',
    'CLASSES.CLASSE.CODE' : 'CLASSE_CODE', 'CLASSES.CLASSE.LIBELLE' : 'CLASSE_LIBELLE',
    'VALIDITE_OFFRE.DUREE_MOIS' : 'VALIDITE_OFFRE_DUREE_MOIS',
    'DUREE_DELAI.DUREE_MOIS' : 'DUREE_CONTRAT_MOIS',
    'DECISION.RENSEIGNEMENT.DATE_ATTRIBUTION' : 'DATE_ATTRIBUTION'})


#########################################################################################################
# Clean
df_dataAquitaine['NB_RECONDUCTIONS'] = df_dataAquitaine['NB_RECONDUCTIONS'].astype('Int32')
df_dataAquitaine['NB_OFFRE_RECU'] = df_dataAquitaine['NB_OFFRE_RECU'].astype('Int32')
df_dataAquitaine['CLASSE_CODE'] = df_dataAquitaine['CLASSE_CODE'].astype('Int32')
df_dataAquitaine['NB_LOT_ATTRIB_MAX'] = df_dataAquitaine['NB_LOT_ATTRIB_MAX'].astype('Int32')

df_dataAquitaine = df_dataAquitaine[(df_dataAquitaine['CP'] // 1000 == 64) | (df_dataAquitaine['CP'] // 1000 == 40) | \
                                    (df_dataAquitaine['CP'] // 1000 == 33) | (df_dataAquitaine['CP'] // 1000 == 47)]

df_dataAquitaine['CPV'] = df_dataAquitaine['CPV'].replace(0, np.nan).astype('Int32')
print(df_dataAquitaine.shape)


#########################################################################################################
# DATES / DUREE

# Merge VALIDITE_OFFRE.DUREE_MOIS + VALIDITE_OFFRE.DUREE_JOUR
df_dataAquitaine['VALIDITE_OFFRE_DUREE_MOIS'] = df_dataAquitaine['VALIDITE_OFFRE_DUREE_MOIS']. \
    fillna(df_dataAquitaine['VALIDITE_OFFRE.DUREE_JOUR'] / 30).fillna(0).astype(np.int64, errors='ignore').replace(0, np.nan).astype('Int32')
df_dataAquitaine = df_dataAquitaine.drop(columns = 'VALIDITE_OFFRE.DUREE_JOUR')

# Fusion DUREE_DELAI.DUREE_MOIS + DUREE_DELAI.DUREE_JOURS
df_dataAquitaine['DUREE_CONTRAT_MOIS'] = df_dataAquitaine['DUREE_CONTRAT_MOIS']. \
    fillna(df_dataAquitaine['DUREE_DELAI.DUREE_JOURS'] / 30).fillna(0).astype(np.int64, errors='ignore').replace(0, np.nan).astype('Int32')
df_dataAquitaine = df_dataAquitaine.drop(columns = 'DUREE_DELAI.DUREE_JOURS')

# Fusion : ACCORD_CADRE.DUREE_MOIS + DUREE_CONTRAT_MOIS
df_dataAquitaine['DUREE_CONTRAT_MOIS'] = df_dataAquitaine['DUREE_CONTRAT_MOIS']. \
    fillna(df_dataAquitaine['ACCORD_CADRE.DUREE_MOIS']).fillna(0).astype(np.int64, errors='ignore').replace(0, np.nan).astype('Int32')
df_dataAquitaine = df_dataAquitaine.drop(columns = 'ACCORD_CADRE.DUREE_MOIS')

# Fusion LOTS.LOT.DUREE_MOIS + DUREE_CONTRAT_MOIS
df_dataAquitaine['DUREE_CONTRAT_MOIS'] = df_dataAquitaine['DUREE_CONTRAT_MOIS']. \
    fillna(df_dataAquitaine['LOTS.LOT.DUREE_MOIS']).fillna(0).astype(np.int64, errors='ignore').replace(0, np.nan).astype('Int32')
df_dataAquitaine = df_dataAquitaine.drop(columns = 'LOTS.LOT.DUREE_MOIS')
print(df_dataAquitaine.shape)


#########################################################################################################
# Format

df_dataAquitaine['DATE_ATTRIBUTION'] = pd.to_datetime(df_dataAquitaine['DATE_ATTRIBUTION'], format = '%Y-%m-%d')
df_dataAquitaine['DATE_PUBLICATION'] = pd.to_datetime(df_dataAquitaine['DATE_PUBLICATION'], format = '%Y-%m-%d')
df_dataAquitaine['DATE_OUVERTURE_OFFRES'] = pd.to_datetime(df_dataAquitaine['DATE_OUVERTURE_OFFRES'], format = '%Y-%m-%d')

df_dataAquitaine['CP'] = df_dataAquitaine['CP'].astype('Int32')
df_dataAquitaine['DESCRIPTEUR_CODE'] = df_dataAquitaine['DESCRIPTEUR_CODE'].astype('Int32')


#########################################################################################################
# ORDER
df_dataAquitaine = df_dataAquitaine[[ \
    'IDWEB',
    'DATE_PUBLICATION',
    'CP',
    'RESUME_OBJET',
    'DESCRIPTEUR_CODE',
    'DESCRIPTEUR_LIBELLE',
    'CPV',
    'VALIDITE_OFFRE_DUREE_MOIS',
    'CRITERES_ATTRIBUTION_1',
    'CRITERES_ATTRIBUTION_2',
    'DUREE_CONTRAT_MOIS',
    'VALEUR_TOTALE',
    'CLASSE_CODE',
    'CLASSE_LIBELLE',
    'DATE_OUVERTURE_OFFRES',
    'DATE_ATTRIBUTION',
    'NB_OFFRE_RECU',
    'NB_RECONDUCTIONS',
    'ESTIMATION_INITIALE',
    'NB_LOT_ATTRIB_MAX']]

print(df_dataAquitaine['CRITERES_ATTRIBUTION_1'].dropna())

# IDWEB                     str     51482
# DATE_PUBLICATION          date    51482
# CP                        int     51482
# RESUME_OBJET              str     51482
# DESCRIPTEUR_CODE          int     51482
# DESCRIPTEUR_LIBELLE       str     51482
# CPV                       int     36640
# VALIDITE_OFFRE_DUREE_MOIS int     26001
# CRITERES_ATTRIBUTION_1    PRIX    17046
# CRITERES_ATTRIBUTION_2    PRIX    17046
# DUREE_CONTRAT_MOIS        int     16529
# VALEUR_TOTALE             float   11114
# CLASSE_CODE               int     9781
# CLASSE_LIBELLE            str     9781
# DATE_OUVERTURE_OFFRES     date    7487
# DATE_ATTRIBUTION          date    4942
# NB_OFFRE_RECU             int     4117
# NB_RECONDUCTIONS          int     2067
# ESTIMATION_INITIALE       float   901
# NB_LOT_ATTRIB_MAX         int     564


#########################################################################################################
# Generate Step 3 file

fileName = "/home/alauzettho/BOAMP/ScriptsParseDateRegion/dataAquitaine_3.csv"
df_dataAquitaine.to_csv(fileName)