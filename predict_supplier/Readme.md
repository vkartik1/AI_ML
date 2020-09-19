## Predict Supplier, with probability, for a given Item and Category

### Create a model and deploy it on a flask server
1. Create a pickle file and also print predictions for a sample data file,  data/test_data.txt.
      python src/model_supplier.py
2. Start a flask server for the predict API. 
      python src/predict_supplier.py
3. Invoke the REST API. This should return supplier(s) with probability
      http://127.0.0.1:5000/api/v1/sourcing/supplier_prediction?item='Street Bike'
4. Run the automated test for the prediction api
      pytest

### Docker
1. Build a docker image
      docker-compose build
2. Bring up the server to process the Prediction REST API. Make sure to "ctrl-c" the server you brought up in earlier step
      docker-compose up
   Now try invoking the same REST API url provided earlier

