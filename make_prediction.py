import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.feature_extraction.text import TfidfVectorizer
filename = 'RandomForest_model.sav'
saved_vectorizer = 'vectorizer.pk'
saved_lsa = 'lsa.pk'
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
loaded_lsa = pickle.load(open(saved_lsa, 'rb'))
loaded_vectorizer = pickle.load(open(saved_vectorizer, 'rb'))

#REPLACE TEST STRING WITH YOURS
test1 = ["Wonderful time- even with the snow! What a great experience! From the goldfish in the room (which my daughter loved) to the fact that the valet parking staff who put on my chains on for me it was fabulous. The staff was attentive and went above and beyond to make our stay enjoyable. Oh, and about the parking: the charge is about what you would pay at any garage or lot- and I bet they wouldn't help you out in the snow! ", "perfect this hotel is perfect for staying at before or after a cruise, we were only staying one day and the room was ready early and it was clean and they were helpful. if you need a shuttle at an after hours time you just have to call them and they will take care of it! it's way better than the best value inn in renton! i would stay here a again in a minute. ", 
         "perfect this hotel is perfect for staying at before or after a cruise, we were only staying one day and the room was ready early and it was clean and they were helpful. if you need a shuttle at an after hours time you just have to call them and they will take care of it! it's way better than the best value inn in renton! i would stay here a again in a minute. "]

test1_transformed = loaded_vectorizer.transform(test1)
test1_lsa= loaded_lsa.transform(test1_transformed)
loaded_model.predict(test1_lsa)