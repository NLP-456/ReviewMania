import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.callbacks import ModelCheckpoint
import re


import glob
import io
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt



plt.ioff() #http://matplotlib.org/faq/usage_faq.html (interactive mode)
#Load data
contents = []
overalls = []
for filename in glob.iglob('./Review_Texts/*.dat', ):
#for filename in glob.iglob('./test_hotel/*.dat', ):
    with io.open(filename, 'r', encoding="utf8") as input_file:
        lines = input_file.readlines()
        
        for line in lines:
            #print(line)
            if '<Content>' in line:
                contents.append(line[9:].strip('\n'))
            if '<Overall>' in line:
                overalls.append(line[9:].strip('\n'))


#MAKE a Dataframe
df = pd.DataFrame(list(map(list, zip(contents, overalls))))
columns = ['review', 'score']
df.columns = columns

df.review = df.review.str.lower()
df.review = df.review.apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))

def filter(user):
    score = int(user)
    if (score <2):     
        return 'neg'
    elif (score >=2 and score <4):
        return 'neutral'
    else:
        return 'pos'

df['category'] = df['score'].apply(filter)


# Limiting # of positive reviews to 17K
short_pos = df.review[df['category'] == 'pos']
short_pos = short_pos[:17000]
print("\nLENGTH OF POSITIVE REVIEWS: ")
print(len(short_pos))
short_neg = df.review[df['category'] == 'neg']
print("\nLENGTH OF NEGATIVE REVIEWS: ")
print(len(short_neg))
print("\n")

#CREATE A NEW DF FOR NEGATIVE AND POSITIVE REVIEWS with SCORE COLUMN
neg_df = pd.DataFrame(short_neg)
neg_df['label'] = 0

pos_df = pd.DataFrame(short_pos)
pos_df['label'] = 1

from sklearn.utils import shuffle
new_df = pd.concat([neg_df, pos_df])

new_df = shuffle(new_df)

# KAGGLE CODE
for idx,row in new_df.iterrows():
    row[0] = row[0].replace('rt',' ')
    
max_features = 2000

#UNICODE FIX

import keras.preprocessing.text

def text_to_word_sequence(text,
                          filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                          lower=True, split=" "):
    if lower: text = text.lower()
    if type(text) == unicode:
        translate_table = {ord(c): ord(t) for c,t in zip(filters, split*len(filters)) }
    else:
        translate_table = maketrans(filters, split * len(filters))
    text = text.translate(translate_table)
    seq = text.split(split)
    return [i for i in seq if i]
    
keras.preprocessing.text.text_to_word_sequence = text_to_word_sequence

tokenizer = Tokenizer(nb_words=max_features, split=' ')

#UNICODE FIX


tokenizer.fit_on_texts(new_df['review'].values)
X = tokenizer.texts_to_sequences(new_df['review'].values)
X = pad_sequences(X)

embed_dim = 128
lstm_out = 128

def build_model(max_features, embed_dim, lstm_out):
	model = Sequential()
	model.add(Embedding(max_features, embed_dim,input_length = X.shape[1], dropout=0.2))
	model.add(LSTM(lstm_out, dropout_U=0.2, dropout_W=0.2))
	model.add(Dense(2,activation='softmax'))
	model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
	print(model.summary())
	return model

Y = pd.get_dummies(new_df['label']).values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.33, random_state = 42)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

batch_size = 32

model = build_model(max_features, embed_dim, lstm_out)

# serialize model to JSON
model_json = model.to_json()
with open("LSTM.json", "w") as json_file:
    json_file.write(model_json)

filepath="weightsLSTM.best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')

callbacks_list = [checkpoint]

#history = model.fit(X_train, Y_train, validation_split=0.1, nb_epoch=2, batch_size=128, verbose=2, callbacks=callbacks_list)
history = model.fit(X_train, Y_train, nb_epoch=3, batch_size=batch_size, verbose=2, callbacks=callbacks_list)

print("MODEL FIT DONE")
validation_size = 3000

X_validate = X_test[-validation_size:]
Y_validate = Y_test[-validation_size:]
X_test = X_test[:-validation_size]
Y_test = Y_test[:-validation_size]
score,acc = model.evaluate(X_test, Y_test, verbose = 2, batch_size = batch_size)
print("score: %.2f" % (score))
print("acc: %.2f" % (acc))