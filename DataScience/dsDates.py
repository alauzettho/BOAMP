import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#########################################################################################################
df_dataAquitaine = pd.read_csv("/home/alauzettho/BOAMP/DataScience/data.csv")
df_dataAquitaine = df_dataAquitaine.drop(columns = 'Unnamed: 0')
print('------------------- DATA AQUITAINE IMPORTED -------------------')
# print(df_dataAquitaine.shape)

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

df_date = df_dataAquitaine[['DATE_PUBLICATION']]
df_date['DATE_PUBLICATION'] = pd.to_datetime(df_date['DATE_PUBLICATION'], format='%Y-%m', errors='coerce').dt.to_period('Q')

