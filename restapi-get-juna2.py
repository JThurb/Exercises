# Ohjelma hakee Digitrafficin datasta, annetun päivämäärän kaikki junat, jotka on määritetty tyypiltään IC eli Inter City ja kategorialtaan Long Distance. 
# Junien Lähtö- ja päätepysäkit tulostetaan junanumeron kanssa. 

import requests

päivä = "2025-12-01"
url = f"https://rata.digitraffic.fi/api/v1/trains/{päivä}"

response = requests.get(url)


if response.status_code == 200:  # Jos GET-pyyntö on onnistunut
    data = response.json()
    
    # Käydään saatu data läpi ja tallennetaan muutujiin
    for train in data:
        traintype = train.get("trainType")
        traincategory = train.get("trainCategory")
        trainnumber = train.get("trainNumber")
        
        # Määritetään tyyppi ja kategoria ja muodostetaan lista nimeltä rows
        if traintype == "IC" and traincategory == "Long-distance":
            rows = train.get("timeTableRows", [])
            
            # Etsitään lähtöasema
            lähtö_rivi = next(r for r in rows if r["type"] == "DEPARTURE")
            lähtöasema = lähtö_rivi["stationShortCode"]
            
            # Etsitään määränpääasema
            määränpää_row = [r for r in rows if r["type"] == "ARRIVAL"][-1]
            määränpää_asema = määränpää_row["stationShortCode"]

            print(f"Juna: {trainnumber} {lähtöasema} -> {määränpää_asema}")

else:
    print(f"Tapahtui virhe GET-pyynnössä. Koodi: {response.status_code}")



