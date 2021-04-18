import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FactorAnalysis


#########################################################################################################
df_dataAquitaine = pd.read_csv("/home/alauzettho/BOAMP/DataScience/data.csv")
df_dataAquitaine = df_dataAquitaine.drop(columns = 'Unnamed: 0')
print('------------------- DATA AQUITAINE IMPORTED -------------------')
#########################################################################################################


target      = 'CRITERES_ATTRIBUTION_1'
features    = ['CPV', 'DUREE_CONTRAT_MOIS', 'CRITERES_ATTRIBUTION_2']

df = df_dataAquitaine[[target, 'CPV', 'DUREE_CONTRAT_MOIS', 'CRITERES_ATTRIBUTION_2']]
df = df.rename(columns = {target : 'target'})

print(df.shape)
df = df.dropna()
print(df.shape)

# CPV                       int     36640
# VALIDITE_OFFRE_DUREE_MOIS int     26001
# CRITERES_ATTRIBUTION_1    PRIX    17046
# CRITERES_ATTRIBUTION_2    PRIX    17046
# DUREE_CONTRAT_MOIS        int     16529
# VALEUR_TOTALE             float   11114





# Separating out the features
x = df.loc[:, features].values
# Separating out the target
y = df.loc[:,['target']].values
# Standardizing the features
x = StandardScaler().fit_transform(x)


pca = FactorAnalysis(n_components = 2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
# principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1'])


finalDf = pd.concat([principalDf, df[['target']]], axis = 1)


fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = df['target'].unique()
colors = ['r', 'g', 'b', 'w', 'y', 'g']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()
plt.show()

# print(pca.explained_variance_ratio_)