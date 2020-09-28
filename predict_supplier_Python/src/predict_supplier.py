import pandas as pd
#from sklearn.base import BaseEstimator, TransformerMixin
import pickle
import numpy as np
from flask import jsonify

import flask
from flask import request, jsonify
#import pred_supplier_probability

from utils import ItemSelector
from utils import CategorySelector
from utils import NumberSelector
from utils import Tokenizer

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Sourcing Prediction</h1>
<p>Prediction usease for Sourcing.</p>'''

######### Get Request params and call the prediction API ##########
@app.route('/api/v1/sourcing/supplier_prediction', methods=['GET'])
def predict_supplier():
    # Check if an item was provided
    if 'item' in request.args:
        item = request.args['item']
    else:
        return "Error: No item provided. Please specify an item."
    if 'category' in request.args:
        category = request.args['category']
    else:
        category = ""
    
    # Create an empty list for our results
    results = []
    supplier=predict(item, category)
    results.append(supplier)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    print(results)
    return jsonify(results)

######### Prediction ##########
def predict(item, category):

    loadedModel = pickle.load(open("supplier_predictions.pkl","rb"))
    data={'ITEM_DESCRIPTION': [item], 'CATEGORY': [category]}
    items=pd.DataFrame(data)
    new_y_pred=loadedModel.predict(items)
        
    probabilities = loadedModel.predict_proba(items)
    top_preds = np.argsort(-probabilities, axis=1)[:,:2]
    top_preds = np.transpose(top_preds)
    probabilities = np.round(probabilities[0][top_preds], 2)
        
    suppliers = loadedModel.classes_[top_preds]
    data = { 'supplier': suppliers[:,0], 'probability': probabilities[:,0] }
    new_df = pd.DataFrame(data, columns= ['supplier', 'probability'])
    new_df=new_df[new_df.probability>0.1]
    print(new_df)
    
    return new_df.to_dict(orient="records")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
