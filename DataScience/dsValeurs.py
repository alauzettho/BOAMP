import sklearn
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#########################################################################################################
df_dataAquitaine = pd.read_csv("/home/alauzettho/BOAMP/DataScience/data.csv")
df_dataAquitaine = df_dataAquitaine.drop(columns = 'Unnamed: 0')
print('------------------- DATA AQUITAINE IMPORTED -------------------')

# 'DATE_PUBLICATION'
# CP                        int     51482
# CPV                       int     36640
# VALEUR_TOTALE             float   11114
# NB_OFFRE_RECU             int     4117
# NB_RECONDUCTIONS          int     2067
# ESTIMATION_INITIALE       float   901
# NB_LOT_ATTRIB_MAX         int     564

#########################################################################################################

# df_estim = df_dataAquitaine[df_dataAquitaine['ESTIMATION_INITIALE'] > 0]
# df_diff = pd.DataFrame()
# df_diff['Différence'] = df_estim['VALEUR_TOTALE'].subtract(df_estim['ESTIMATION_INITIALE']).dropna()

# ax = sns.histplot(data = df_diff, x = "Différence")
# ax.set_xlim([-1000000, 1000000])
# ax.set_yscale('log')
# plt.show()

#########################################################################################################

df_prix = df_dataAquitaine[['VALEUR_TOTALE', 'DATE_PUBLICATION']]
df_prix = df_prix[df_prix['VALEUR_TOTALE'] < 1.0e6]
df_prix['DATE_PUBLICATION'] = pd.to_datetime(df_prix['DATE_PUBLICATION'], format='%Y-%m', errors='coerce').dt.to_period('Q')


boxplot = df_prix.boxplot(column = ['VALEUR_TOTALE'], by = "DATE_PUBLICATION", grid = False)
boxplot.plot()
plt.show()