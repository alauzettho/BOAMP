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

# df_list = list(zip(df_dataAquitaine['CRITERES_ATTRIBUTION_1'].dropna(), df_dataAquitaine['CRITERES_ATTRIBUTION_2'].dropna()))
# df_pair = pd.DataFrame()
# df_pair['LABELS'] = df_list
# print(df_pair.value_counts())

# ax = sns.countplot(x = 'CRITERES_ATTRIBUTION_1', data = df_dataAquitaine, order = df_dataAquitaine['CRITERES_ATTRIBUTION_1'].value_counts().iloc[:4].index)
# ax.set(xlabel = 'CRITERES', ylabel = 'OCCURENCE')
# plt.show()



# ax = sns.countplot(x = 'DESCRIPTEUR_LIBELLE', data = df_dataAquitaine, order = df_dataAquitaine['DESCRIPTEUR_LIBELLE'].value_counts().iloc[:12].index)
# ax.set(xlabel = 'DESCRIPTEUR', ylabel = 'OCCURENCE')

# x = df_dataAquitaine['DESCRIPTEUR_LIBELLE'].value_counts().iloc[:12].index
# ax.set_xticklabels(labels = x, rotation=25)
# plt.show()


# ax = sns.countplot(x = 'DUREE_CONTRAT_MOIS', data = df_dataAquitaine, order = df_dataAquitaine['DUREE_CONTRAT_MOIS'].value_counts().iloc[:10].index)
# ax.set(xlabel = 'DUREE_CONTRAT_MOIS', ylabel = 'OCCURENCE')

# x = df_dataAquitaine['DUREE_CONTRAT_MOIS'].value_counts().iloc[:10].index
# ax.set_xticklabels(labels = x, rotation=30)
# plt.show()


df_duree = pd.DataFrame()
df_duree['DUREE'] = df_dataAquitaine['DUREE_CONTRAT_MOIS']

df_duree = df_duree.value_counts().rename_axis('DUREE_CONTRAT_MOIS').reset_index(name = 'OCCURENCE')
# df_duree = df_duree[df_duree['OCCURENCE'] > 325]
print(df_duree)
