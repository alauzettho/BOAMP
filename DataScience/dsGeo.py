import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt

#########################################################################################################
df_dataAquitaine = pd.read_csv("/home/alauzettho/BOAMP/DataScience/data.csv")
df_dataAquitaine = df_dataAquitaine.drop(columns = 'Unnamed: 0')
print('------------------- DATA AQUITAINE IMPORTED -------------------')

#########################################################################################################

fp = "/home/alauzettho/BOAMP/DataScience/codes_postaux_V5/codes_postaux_region.shp"
df_map = gpd.read_file(fp)
df_map = df_map.to_crs(epsg = 3857)
df_map = df_map[(df_map['DEP'] == '40') | (df_map['DEP'] == '33') | (df_map['DEP'] == '47') | (df_map['DEP'] == '64')]
df_map['ID'] = df_map['ID'].astype(int)
df_map = df_map.rename(columns = {'ID': 'CP'})
df_map = df_map[['CP', 'geometry']]

variable = 'VALEUR_TOTALE'

listDelta = [33001, 33006, 33007, 33023, 33025, 33028, 33041, 33043, 33045, 33046, 33049
, 33052, 33053, 33056, 33059, 33060, 33062, 33063, 33068, 33072, 33073, 33074, 33075
, 33076, 33077, 33078, 33080, 33081, 33082, 33085, 33088, 33090, 33116, 33151, 33152
, 33164, 33166, 33167, 33173, 33175, 33192, 33213, 33271, 33294, 33305, 33311, 33313
, 33321, 33327, 33391, 33394, 33401, 33402, 33404, 33405, 33451, 33452, 33491, 33502
, 33503, 33505, 33523, 33563, 33564, 33603, 33604, 33607, 33608, 33611, 33612, 33615
, 33652, 33688, 33693, 33705, 33882, 33883, 40001, 40002, 40003, 40004, 40005, 40006
, 40011, 40013, 40023, 40024, 40025, 40102, 40107, 40115, 40161, 40231, 40511, 40601
, 40705, 40992, 40994, 47003, 47006, 47007, 47008, 47031, 47207, 47213, 47305, 47307
, 47501, 47502, 47551, 47901, 47914, 47916, 47922, 47923, 64001, 64006, 64010, 64012
, 64017, 64021, 64022, 64032, 64034, 64036, 64039, 64046, 64051, 64053, 64058, 64075
, 64104, 64105, 64108, 64109, 64111, 64115, 64141, 64144, 64146, 64183, 64185, 64202
, 64204, 64238, 64301, 64404, 64502, 64603, 64701, 33050]

df_data = df_dataAquitaine[['CP', variable]].dropna()

for i in range(0, len(df_data.index)) :
    cp = df_data['CP'].iloc[i]
    if cp in listDelta :
        df_data['CP'].iloc[i] = (cp // 100 * 100)

df_data = df_data.groupby('CP', as_index = False).mean()
df_data = df_data[df_data[variable] < 1.0e7]
df_merged = pd.merge(df_map, df_data, how = "left", on = ["CP"])



fig, ax = plt.subplots(1, 1)
plt.axis('off')
df_merged.plot(column = variable, ax = ax, legend = True, cmap = "Spectral", missing_kwds = {"color": "lightgrey"}, edgecolor = 'black')
plt.show()