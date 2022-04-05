from geopy.geocoders import Nominatim
import csv

def get_locations():    

    locations = []

    with open("unique_cities.csv", "r") as f:
        unique_cities = csv.reader(f)

        geolocator = Nominatim(user_agent="ConestogaApp")

        for row in unique_cities:
            city = row[0]
            amount = row[1]
            print(f"Getting location for {city}")
            location = geolocator.geocode(city)
            
            lat = None
            longit = None

            if location is not None:
                lat = location.latitude
                longit = location.longitude

            locations.append((city, amount, lat, longit))

            # Comment out to test with the first city only 
            # break

    
    with open("cities_with_location.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(('City', 'Amount', 'Latitude', 'Longitude'))
        for loc in locations:
            writer.writerow(loc)


if __name__ == "__main__":
    get_locations()