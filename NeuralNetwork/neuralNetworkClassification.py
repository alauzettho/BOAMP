from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pandas as pd
import numpy as np
import pickle

############################################################################################################
# Load Model

filepath = './NeuralNetworkModel'
model = load_model(filepath, compile = True)

with open('./NeuralNetworkModel/tokenizer.pickle', 'rb') as handle :
    loaded_tokenizer = pickle.load(handle)
print('----------------------- MODEL LOADED ------------------------')


############################################################################################################
# import Data

criteria_list = ['PRIX', 'TECHNIQUE', 'QUALITE', 'DELAI', 'AUTRE']
df_critere = pd.read_csv("/home/alauzettho/BOAMP/NN/critere_attribution_data.csv")
df_critere = df_critere.set_index('Unnamed: 0')
print('------------------- DATA CRITERE IMPORTED -------------------')


seq         = loaded_tokenizer.texts_to_sequences(df_critere['CRITERES_ATTRIBUTION_1'])
padded      = pad_sequences(seq, maxlen = 20, padding = 'post')
predictions = model.predict(padded)
classes1    = np.argmax(predictions, axis = 1)

seq         = loaded_tokenizer.texts_to_sequences(df_critere['CRITERES_ATTRIBUTION_2'])
padded      = pad_sequences(seq, maxlen = 20, padding = 'post')
predictions = model.predict(padded)
classes2    = np.argmax(predictions, axis = 1)


for i in range(0, len(df_critere.index)) :
    df_critere['CRITERES_ATTRIBUTION_1'].iloc[i] = criteria_list[classes1[i]]
    df_critere['CRITERES_ATTRIBUTION_2'].iloc[i] = criteria_list[classes2[i]]

print(df_critere)
df_critere.to_csv("critere_attribution_classified.csv")