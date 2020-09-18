### Predict Supplier, with probability, for a given Item and Category
1. "python src/model_supplier.py": Create a pickle file and also print predictions for a sample data file,  data/test_data.txt.
2. "python src/predict_supplier.py": Start a flask server for the predict API. 
3. Invoke the REST API, http://127.0.0.1:5000/api/v1/sourcing/auction?item='Street Bike': This should return supplier(s) with probability
4. "pytest": this will run the automated test for the prediction api
