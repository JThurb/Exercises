import requests

päivä = "2025-12-01"
url = f"https://rata.digitraffic.fi/api/v1/trains/{päivä}"

response = requests.get(url)


if response.status_code == 200:
    data = response.json()

    for train in data:
        traintype = train.get("trainType")
        traincategory = train.get("trainCategory")
        trainnumber = train.get("trainNumber")

        if traintype == "IC" and traincategory == "Long-distance":
            rows = train.get("timeTableRows", [])
            
            # lähtöasema
            lähtö_rivi = next(r for r in rows if r["type"] == "DEPARTURE")
            lähtöasema = lähtö_rivi["stationShortCode"]
            
            # määränpääasema
            määränpää_row = [r for r in rows if r["type"] == "ARRIVAL"][-1]
            määränpää_station = määränpää_row["stationShortCode"]

            print(f"Juna: {trainnumber} {lähtöasema} -> {määränpää_station}")

else:
    print(f"GET response faulty. Code: {response.status_code}")


