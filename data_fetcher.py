import json
import time
from pathlib import Path

import requests

REGION_NAME = 'Illinois, USA'
USER_AGENT = "CS411-Chicago-Search-Visualizer/1.0"
PROJECT_FOLDER = Path(__file__).resolve().parent

CITIES = ['Chicago, IL',
 'Aurora, IL',
 'Naperville, IL',
 'Joliet, IL',
 'Rockford, IL',
 'Springfield, IL',
 'Peoria, IL',
 'Elgin, IL',
 'Waukegan, IL',
 'Champaign, IL',
 'Bloomington, IL',
 'Decatur, IL',
 'Evanston, IL',
 'Schaumburg, IL',
 'Arlington Heights, IL',
 'Bolingbrook, IL',
 'Palatine, IL',
 'Skokie, IL',
 'Des Plaines, IL',
 'Orland Park, IL',
 'Kankakee, IL',
 'DeKalb, IL']

ROAD_CONNECTIONS = [('Chicago, IL', 'Evanston, IL'),
 ('Chicago, IL', 'Skokie, IL'),
 ('Chicago, IL', 'Des Plaines, IL'),
 ('Chicago, IL', 'Naperville, IL'),
 ('Chicago, IL', 'Joliet, IL'),
 ('Chicago, IL', 'Orland Park, IL'),
 ('Evanston, IL', 'Skokie, IL'),
 ('Skokie, IL', 'Des Plaines, IL'),
 ('Des Plaines, IL', 'Arlington Heights, IL'),
 ('Arlington Heights, IL', 'Palatine, IL'),
 ('Palatine, IL', 'Schaumburg, IL'),
 ('Schaumburg, IL', 'Elgin, IL'),
 ('Elgin, IL', 'DeKalb, IL'),
 ('DeKalb, IL', 'Rockford, IL'),
 ('Rockford, IL', 'Elgin, IL'),
 ('Arlington Heights, IL', 'Waukegan, IL'),
 ('Evanston, IL', 'Waukegan, IL'),
 ('Schaumburg, IL', 'Naperville, IL'),
 ('Naperville, IL', 'Aurora, IL'),
 ('Aurora, IL', 'DeKalb, IL'),
 ('Aurora, IL', 'Joliet, IL'),
 ('Naperville, IL', 'Bolingbrook, IL'),
 ('Bolingbrook, IL', 'Joliet, IL'),
 ('Joliet, IL', 'Orland Park, IL'),
 ('Joliet, IL', 'Kankakee, IL'),
 ('Kankakee, IL', 'Champaign, IL'),
 ('Joliet, IL', 'Bloomington, IL'),
 ('Rockford, IL', 'Peoria, IL'),
 ('Peoria, IL', 'Bloomington, IL'),
 ('Bloomington, IL', 'Champaign, IL'),
 ('Bloomington, IL', 'Decatur, IL'),
 ('Bloomington, IL', 'Springfield, IL'),
 ('Peoria, IL', 'Springfield, IL'),
 ('Springfield, IL', 'Decatur, IL'),
 ('Decatur, IL', 'Champaign, IL')]


def fetch_coordinates(city_name):
    """Fetch one city's coordinates from Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name + ", USA",
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "us",
    }
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    results = response.json()

    if not results:
        raise ValueError("No coordinates found for " + city_name)

    location = results[0]
    latitude = float(location["lat"])
    longitude = float(location["lon"])
    return {"lat": latitude, "lon": longitude}


def fetch_road_distance(coord1, coord2):
    """Fetch an OSRM road distance in kilometers; inputs are (lat, lon)."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    source_point = f"{lon1},{lat1}"
    destination_point = f"{lon2},{lat2}"
    url = "https://router.project-osrm.org/route/v1/driving/"
    url += source_point + ";" + destination_point
    response = requests.get(url, params={"overview": "false"}, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError("OSRM could not find a driving route.")

    routes = data.get("routes")
    if not routes:
        raise ValueError("OSRM did not return any routes.")

    distance_meters = routes[0]["distance"]
    distance_kilometers = distance_meters / 1000
    return distance_kilometers


def build_graph():
    """Build the graph using the starter's structure and the current app's format."""
    print("Building map graph for region:", REGION_NAME)
    cache_file = PROJECT_FOLDER / "coordinates_cache.json"

    try:
        with open(cache_file, "r") as file:
            locations = json.load(file)
        print("Loaded saved coordinates.")
    except FileNotFoundError:
        locations = {}
        for city in CITIES:
            locations[city] = fetch_coordinates(city)
            print(city, locations[city])
            time.sleep(1.1)
        with open(cache_file, "w") as file:
            json.dump(locations, file, indent=2)

    if set(locations) != set(CITIES):
        raise ValueError("The coordinate cache does not match the selected cities.")

    connections = {}
    for city in CITIES:
        connections[city] = []

    for source, destination in ROAD_CONNECTIONS:
        source_coordinate = (locations[source]["lat"], locations[source]["lon"])
        destination_coordinate = (locations[destination]["lat"], locations[destination]["lon"])

        distance = fetch_road_distance(source_coordinate, destination_coordinate)
        edge = {"node": destination, "distance": distance}
        connections[source].append(edge)
        print(source, "->", destination, distance, "km")
        time.sleep(1.1)

        reverse_distance = fetch_road_distance(destination_coordinate, source_coordinate)
        reverse_edge = {"node": source, "distance": reverse_distance}
        connections[destination].append(reverse_edge)
        print(destination, "->", source, reverse_distance, "km")
        time.sleep(1.1)

    map_data = {
        "region": REGION_NAME,
        "nodes": locations,
        "connections": connections,
    }
    with open(PROJECT_FOLDER / "map_data.json", "w") as file:
        json.dump(map_data, file, indent=2)

    print("Saved map_data.json with", len(locations), "cities.")


if __name__ == "__main__":
    build_graph()
