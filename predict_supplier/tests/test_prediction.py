# test_prediction.py
import sys
sys.path.append('./prediction/')
import json
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem import PorterStemmer
import re     # librarie for cleaning data
import pickle
import numpy as np
from flask import jsonify

from utils import ItemSelector
from utils import CategorySelector
from utils import NumberSelector
from utils import Tokenizer
from utils import all_stopwords

from predict_supplier import app

def test_single_api_call():
    print('start')
    data = {'item': 'Bike'}

    expected_response = [[{'supplier': 'REI', 'probability': 0.37}, {'supplier': 'Olympia Sporting Goods', 'probability': 0.26}]]

    with app.test_client() as client:
        # Test client uses "query_string" instead of "params"
        response = client.get('/api/v1/sourcing/auction', query_string=data)
        assert response.status_code == 200
        data = json.loads(response.data)
        print(data)
        assert (data[0][0]["supplier"]) == 'REI'
        assert (data[0][0]["probability"] >= 0.30 )
        assert (data[0][1]["supplier"] == 'Olympia Sporting Goods')
        assert (data[0][1]["probability"] >= 0.20)
     
        # response.data returns bytes, convert to a dict.
        # assert json.loads(response.data) == expected_response

#if __name__ == '__main__':
#    app.run(debug=True)
