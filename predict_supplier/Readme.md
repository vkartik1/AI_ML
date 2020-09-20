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
3. Now try invoking the same REST API url 
      http://127.0.0.1:5000/api/v1/sourcing/supplier_prediction?item='Street Bike

### Kubernetes support
1. Apply the deployment file which has the load balancer defined to run on port 6000
      kubectl apply -f deployment.yaml
2. make sure there are 4 pods running the supplier-prediction-app
      kubectl get pods
3. Run the prediction service (port 6000)
      http://127.0.0.1:6000/api/v1/sourcing/supplier_prediction?item='Street Bike'

### Helm support
1. uninstall existing chart (for reruns) and install the new chart
      helm uninstall predict-suppplier-chart; helm install predict-suppplier-chart supplier-chart/ --values supplier-chart/values.yaml
2. Run the prediction service (port 6000)
      http://127.0.0.1:6000/api/v1/sourcing/supplier_prediction?item='Street Bike'

Helm Note (optional read): This just describes what changes were done to generate the code. Feel free to skip this notes section
1. I have created the helm directories with the "helm create supplier-chart" command. 
2. The deployment.yaml that was created in previous section (Kubernetes support) is used instead of the default serices.yaml and deployment.yaml created by the helm create command. The deployment.yaml has been splt to deployment.yaml and service.yaml with variables instead of hardcoded values.
3. Deleted other yaml files and modified the  values.yaml to keep the port#s consistent with the values used in previous steps: load balancer port=6000
4. Review the values.yaml for the comment "Modification", to see what changes were done

