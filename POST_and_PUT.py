import requests
import json

# api
api_url = "https://api.restful-api.dev/objects"

new_product = {
            'name': 'Playstation 5',
            'data': {'Generation': 'slim', 
                     'Price': '749.99', 
                     'Capacity': '500 GB'}}

# Request POST
response = requests.post(api_url, json=new_product)
created_product = response.json()
product_id = created_product["id"] # server generates id number

if response.status_code in (200, 201): 
    print("Data was added successfully")
else:
    print("Error in POST-request: ", response.status_code, response.text)

####### tehtävä 5 #########

update_product = {'id': product_id,
            'name': 'Playstation 5 pro',    # name changed
            'data': {'Generation': 'pro',  # slim to pro
                     'Price': '949.99',    # Price updated too
                     'Capacity': '1 TB'}}

put_url = f"{api_url}/{product_id}"         # forms an put url with combining api_url and product id with /

payload = json.dumps(update_product)           # data to be sended to server formated to json
headers = {"content-type": "application/json"} # tells to server that data is in json format

put_response = requests.put(put_url, data=payload, headers=headers) 

if put_response.status_code in (200, 204):
    print("Product updated successfully")
else:
    print("Error updating product", put_response.status_code, put_response.text)