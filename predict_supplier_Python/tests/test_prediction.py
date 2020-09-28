# test_prediction.py
import sys, os
src_path=os.path.join(sys.path[0],'../src')
sys.path.append(src_path)
import json
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem import PorterStemmer
import re     # librarie for cleaning data
import pickle
import numpy as np
from flask import jsonify

#from utils import ItemSelector
#from utils import CategorySelector
#from utils import NumberSelector
#from utils import Tokenizer
#from utils import all_stopwords

from predict_supplier import app

def test_single_api_call():
    data = {'item': 'yellow bike', 'category': 'sports'}

    # expected_response = [[{'supplier': 'REI', 'probability': 0.37}, {'supplier': 'Olympia Sporting Goods', 'probability': 0.26}]]

    with app.test_client() as client:
        # Test client uses "query_string" instead of "params"
        response = client.get('/api/v1/sourcing/supplier_prediction', query_string=data)
        data = json.loads(response.data)
        print(data)
        assert response.status_code == 200
        assert ((data[0][0]["supplier"] == 'REI' and data[0][0]["probability"] >= 0.10) or (data[0][1]["supplier"] == 'REI' and data[0][1]["probability"] >= 0.10 ))
        assert ((data[0][0]["supplier"] == 'Olympia Sporting Goods' and data[0][0]["probability"] >= 0.10) or (data[0][1]["supplier"] == 'Olympia Sporting Goods'and data[0][1]["probability"] >= 0.10 ))
     
        # response.data returns bytes, convert to a dict.
        # assert json.loads(response.data) == expected_response

#if __name__ == '__main__':
#    app.run(debug=True)
