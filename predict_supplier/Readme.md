## Predict Supplier, with probability, for a given Item and Category

We will create prediction REST API that will predict a supplier for a given item and category. We will try running the REST APi in differen ways - from running python command to using helm. 
1. We will first create a model and try running this via flask server using python command   
2. Then, instead of running the REST API using the python command, we will use Docker
3. We will then deploy the app on the kubernetes cluster running on 4 pods (replicas=4)
4. Lastly we will use helm - just for learning purpos. There is not really much value for helm, for this simple usecase

### Create a model and deploy it on a flask server
1. Generate the model pickle file and also print predictions for a sample data specified in, data/test_data.txt.  
&ensp;python src/model_supplier.py. 
2. Start a flask server for the predict API.  
&ensp;python src/predict_supplier.py. 
3. Invoke the REST API. This should return supplier(s) with probability.   
&ensp;http://127.0.0.1:5000/api/v1/sourcing/supplier_prediction?item='Street Bike'.   
Kill the Flask server (ctrl-c)
4. Run the automated test for the prediction api.   
&ensp;pytest. 

### Docker
1. Build a docker image.   
&ensp;docker-compose build. 
2. Bring up the server to process the Prediction REST API. Make sure to "ctrl-c" the server you brought up in earlier step.   
&ensp;docker-compose up. 
3. Now try invoking the same REST API url.    
&ensp;http://127.0.0.1:5000/api/v1/sourcing/supplier_prediction?item='Street Bike.   
kill the docker-compose (ctrl-c)

### Kubernetes support
1. Apply the deployment file which has the load balancer defined to run on port 6000.   
&ensp;kubectl apply -f deployment.yaml. 
2. make sure there are 4 pods running the supplier-prediction-app.   
&ensp;kubectl get pods. 
3. Run the prediction service (port 6000).   
&ensp;http://127.0.0.1:6000/api/v1/sourcing/supplier_prediction?item='Street Bike'.   
4. Delete the deployment. 
&ensp;kubectl delete deployment supplier-prediction-app

### Helm support
1. uninstall existing chart (for reruns) and install the new chart.   
&ensp;helm uninstall predict-suppplier-chart; helm install predict-suppplier-chart supplier-chart/ --values supplier-chart/values.yaml. 
2. Run the prediction service (port 6000).   
&ensp;http://127.0.0.1:6000/api/v1/sourcing/supplier_prediction?item='Street Bike'. 
3. Stop the prediction service.   
&ensp;helm uninstall predict-suppplier-chart 

Helm Note (optional read): This just describes what changes were done to generate the code. Feel free to skip this notes section. 
1. I have created the helm directories with the "helm create supplier-chart" command.   
2. The deployment.yaml that was created in previous section (Kubernetes support) is used instead of the default serices.yaml and deployment.yaml created by the helm create command. The deployment.yaml has been splt to deployment.yaml and service.yaml with variables instead of hardcoded values. 
3. Deleted other yaml files and modified the  values.yaml to keep the port#s consistent with the values used in previous steps: load balancer port=6000. 
4. Review the values.yaml for the comment "Modification", to see what changes were done. 
