
import requests

requ = requests.post('http://localhost:5000/sell/', json={
    "title": "Veitsi",
    "author": "Jo Nesbo",
    "year_of_publication": 2010
})

print(requ.status_code)
print(requ.json())
