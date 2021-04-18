from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, save_model, load_model
from keras.layers.core import Activation, Dropout, Dense
from keras.layers import Flatten, LSTM, SimpleRNN, GRU
from keras.layers import MaxPooling1D
from keras.models import Model
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
from keras.layers import Input
from keras.layers.merge import Concatenate
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import os
import pickle


criteres = pd.read_csv("/home/alauzettho/BOAMP/NeuralNetwork/critere_attribution_train.csv")

print("Import Done")





filter = criteres["CRITERE"] != ""
criteres = criteres[filter].dropna()
criteres_labels = criteres[["PRIX", "TECHNIQUE", "QUALITE", "DELAI", "AUTRE"]]


def preprocess_text(sen):
    sentence = re.sub('[^a-zA-Z]', ' ', sen)
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence



X = []
sentences = list(criteres["CRITERE"])
for sen in sentences:
    X.append(preprocess_text(sen))

y = criteres_labels.values


tokenizer   = Tokenizer(num_words = 5000)
tokenizer.fit_on_texts(X)
X_train     = tokenizer.texts_to_sequences(X)
vocab_size  = len(tokenizer.word_index) + 1
maxlen      = 20
X_train     = pad_sequences(X_train, padding = 'post', maxlen = maxlen)




glove_file = open('/home/alauzettho/BOAMP/NeuralNetwork/glove.6B.100d.txt', encoding = "utf8")
embeddings_dictionary = dict()

for line in glove_file:
    records = line.split()
    word = records[0]
    vector_dimensions = np.asarray(records[1:], dtype = 'float32')
    embeddings_dictionary[word] = vector_dimensions
glove_file.close()

embedding_matrix = np.zeros((vocab_size, 100))
for word, index in tokenizer.word_index.items():
    embedding_vector = embeddings_dictionary.get(word)
    if embedding_vector is not None:
        embedding_matrix[index] = embedding_vector





print("setup NN")

deep_inputs     = Input(shape = (maxlen,))
embedding_layer = Embedding(vocab_size, 100, weights = [embedding_matrix], trainable = False)(deep_inputs)
rnn_layer       = LSTM(128)(embedding_layer)
drop_2          = Dropout(0.3)(rnn_layer)
dense_layer_2   = Dense(5, activation = 'sigmoid')(drop_2)
model           = Model(inputs = deep_inputs, outputs = dense_layer_2)

model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['acc'])

print(model.summary())


history = model.fit(X_train, y, batch_size = 5, epochs = 40, verbose = 1, validation_split = 0.3, shuffle = True)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train','test'], loc = 'upper left')
plt.show()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','test'], loc = 'upper left')
plt.show()




# Save the token
with open('./NeuralNetworkModel/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Save the model
filepath = './NeuralNetworkModel'
save_model(model, filepath)