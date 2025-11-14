import requests

# api
api_url = "https://api.restful-api.dev/objects"

# Request
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()

# print with all info
for prod in data:
    print(prod)

products = [product['name'] for product in data] # makes a list of product names

# Print only the name of the product
for i in products: 
    print(i)