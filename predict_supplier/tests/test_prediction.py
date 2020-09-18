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
        print('start')
        # Test client uses "query_string" instead of "params"
        response = client.get('/api/v1/sourcing/auction', query_string=data)
        print(response)
        # Check that we got "200 OK" back.
        assert response.status_code == 200
        # response.data returns bytes, convert to a dict.
        assert json.loads(response.data) == expected_response

#if __name__ == '__main__':
#    ItemSelector.__module__ = "model_supplier"
#    CategorySelector.__module__ = "model_supplier"
#    NumberSelector.__module__ = "model_supplier"

if __name__ == '__main__':
    app.run(debug=True)
