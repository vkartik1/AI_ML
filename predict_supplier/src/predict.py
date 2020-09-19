import requests


data = {'item': 'Street Bike'}

response = requests.get('http://127.0.0.1:5000//api/v1/sourcing/supplier_prediction', params=data)
print('Status code: {}'.format(response.status_code))
print('Payload:\n{}'.format(response.text))
