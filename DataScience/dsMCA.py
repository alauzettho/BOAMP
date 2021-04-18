import pandas as pd
import matplotlib.pyplot as plt
import prince

#########################################################################################################
df_dataAquitaine = pd.read_csv("/home/alauzettho/BOAMP/DataScience/data.csv")
df_dataAquitaine = df_dataAquitaine.drop(columns = 'Unnamed: 0')
print('------------------- DATA AQUITAINE IMPORTED -------------------')
#########################################################################################################


df = df_dataAquitaine[['CPV', 'CP', 'CLASSE_LIBELLE', 'CRITERES_ATTRIBUTION_1', 'CRITERES_ATTRIBUTION_2']]
df = df.dropna()
print(df.shape)

mca = prince.MCA(n_components = 2, n_iter = 3, copy = True, check_input = True, engine = 'auto', random_state=42)
mca = mca.fit(df)

ax = mca.plot_coordinates(X=df, ax=None, figsize=(6, 6),  \
            show_row_points=True, row_points_size=10, show_row_labels=False, show_column_points=True, \
            column_points_size=30, show_column_labels=False, legend_n_cols=1)

plt.show()