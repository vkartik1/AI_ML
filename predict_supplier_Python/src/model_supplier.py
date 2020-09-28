import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import re     # libraries for cleaning data
import nltk   # library for NLP
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pickle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from scipy.stats.stats import pearsonr
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import FeatureUnion

from utils import ItemSelector
from utils import CategorySelector
from utils import NumberSelector
from utils import Tokenizer

data_directory="data/"
data_file_name=data_directory+'input_data.txt'
test_file_name=data_directory+'test_data.txt'

nltk.download('stopwords', quiet=True, raise_on_error=True)
nltk.download('punkt')

tokenized_stop_words = stopwords.words('english')
#
# Dont Remove
#
stemmer=nltk.PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in tokenized_stop_words]

df=pd.read_csv(data_file_name, sep='\t')
print(data_file_name)

#
# Split into training and test data
#
X=df.drop(['SUPPLIER'], axis='columns')
y=df.loc[:,['SUPPLIER']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.40)

#
# Create a pipeline, fit the model, predict for test data and save in pickle
#

classifier = Pipeline([
    ('features', FeatureUnion([
        ('item', Pipeline([
            ('itemext', ItemSelector('ITEM_DESCRIPTION')),
            ('item_tfidf', TfidfVectorizer(tokenizer=Tokenizer, stop_words=stemmed_words)),
        ])),
        ('category', Pipeline([
            ('categoryext', CategorySelector('CATEGORY')),
            ('cat_tfidf', TfidfVectorizer(tokenizer=Tokenizer, stop_words=stemmed_words)),
#            ('cat_tfidf', TfidfVectorizer(tokenizer=Tokenizer, stop_words=stemmed_words, min_df=.0025, max_df=0.25, ngram_range=(1,3))),
        ]))
    ])),
    ('clf', RandomForestClassifier()),
    ])

# Create space of candidate learning algorithms and their hyperparameters
# We could also add 
#               'features__item__item_tfidf__ngram_range': [(1, 3)],
#               'features__item__item_tfidf__stop_words': [None, stemmed_words],
search_space = [
#                {'clf': [LogisticRegression()], 'clf__C': [10.0,  100.0]},
                {'clf': [RandomForestClassifier()] },
                {'clf': [MultinomialNB()] }
               ]

from sklearn.model_selection import GridSearchCV
gs_lr_tfidf = GridSearchCV(classifier, search_space, scoring='accuracy',
                           cv=5, verbose=1, n_jobs=-1)

model = gs_lr_tfidf.fit(X_train,y_train.values.ravel())
clf = gs_lr_tfidf.best_estimator_
score=clf.score(X_test, y_test)

print(gs_lr_tfidf.best_params_)
print(gs_lr_tfidf.best_score_)
print(gs_lr_tfidf.best_estimator_)
print(score)

# Predict for test data
y_pred=model.predict(X_test) 
from sklearn.metrics import confusion_matrix,accuracy_score
acc= accuracy_score(y_test,y_pred)
print(acc)
pickle.dump(model, open(r'supplier_predictions.pkl','wb'))


######### Prediction ##########
def predict(test_file_name):
  loadedModel = pickle.load(open("supplier_predictions.pkl","rb"))
  new_df=pd.read_csv(test_file_name, sep='\t')
  if 'SUPPLIER' in new_df.columns:
    new_items=new_df.drop(['SUPPLIER'], axis='columns')
  else:
    new_items=new_df
    
  new_y_pred=loadedModel.predict(new_items)  

  new_items["SUPPLIER"]=new_y_pred
  print(" ==== Here is our prediction ====")
  print(new_items)

if __name__ == '__main__':
    ItemSelector.__module__ = "model_supplier"
    CategorySelector.__module__ = "model_supplier"
    NumberSelector.__module__ = "model_supplier"
    predict(test_file_name)
