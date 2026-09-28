import json
import time
import requests

REGION = "Chicago metropolitan area, Illinois, USA"

CITIES = [
    "Chicago",
    "Chicago Heights",
    "Harvey",
    "Glenwood",
    "Matteson",
    "Arlington Heights",
    "Schaumburg",
    "Frankfort",
    "Oak Park",
    "Elmhurst",
    "Lombard",
    "Wheaton",
    "Naperville",
    "Aurora",
    "Flossmoor",
    "Bolingbrook",
    "Joliet",
    "Orland Park",
    "Tinley Park",
    "Oak Lawn",
]

ROAD_CONNECTIONS = [
    ("Chicago", "Oak Park"),
    ("Chicago", "Oak Lawn"),
    ("Chicago", "Harvey"),

    ("Oak Park", "Elmhurst"),
    ("Elmhurst", "Lombard"),
    ("Elmhurst", "Schaumburg"),
    ("Schaumburg", "Arlington Heights"),
    ("Lombard", "Wheaton"),
    ("Wheaton", "Naperville"),
    ("Naperville", "Aurora"),
    ("Naperville", "Bolingbrook"),
    ("Aurora", "Joliet"),
    ("Bolingbrook", "Joliet"),

    ("Joliet", "Frankfort"),
    ("Frankfort", "Matteson"),
    ("Frankfort", "Orland Park"),
    ("Orland Park", "Tinley Park"),
    ("Orland Park", "Oak Lawn"),
    ("Oak Lawn", "Harvey"),
    ("Tinley Park", "Matteson"),

    ("Matteson", "Flossmoor"),
    ("Flossmoor", "Chicago Heights"),
    ("Chicago Heights", "Glenwood"),
    ("Glenwood", "Harvey"),
    ("Harvey", "Flossmoor"),
]



def fetch_coordinates(city):
    """Find the latitude and longitude of one Illinois city."""

    url = "https://nominatim.openstreetmap.org/search"

    # Include the state and country to make the search more specific.
    search_query = city + ", Illinois, USA"

    params = {
        "q": search_query,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "us",
    }

    headers = {
        "User-Agent": "CS411-Chicago-Search-Visualizer/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=20,
    )

    response.raise_for_status()
    results = response.json()

    if len(results) == 0:
        error_message = "No coordinates found for " + city
        raise ValueError(error_message)

    first_location = results[0]
    latitude_text = first_location["lat"]
    longitude_text = first_location["lon"]

    latitude = float(latitude_text)
    longitude = float(longitude_text)
    coordinates = {
        "lat": latitude,
        "lon": longitude,
    }

    return coordinates

def fetch_road_distance(source, destination):

    source_latitude = source["lat"]
    source_longitude = source["lon"]

    destination_latitude = destination["lat"]
    destination_longitude = destination["lon"]

    source_point = f"{source_longitude},{source_latitude}"
    destination_point = (
        f"{destination_longitude},{destination_latitude}"
    )

    coordinate_pair = source_point + ";" + destination_point

    base_url = "https://router.project-osrm.org/route/v1/driving/"
    url = base_url + coordinate_pair

    params = {
        "overview": "false"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    response_code = data.get("code")

    if response_code != "Ok":
        raise ValueError("OSRM could not find a driving route.")

    routes = data.get("routes")

    if not routes:
        raise ValueError("OSRM did not return any routes.")

    first_route = routes[0]

    distance_meters = first_route["distance"]
    distance_kilometers = distance_meters / 1000

    return distance_kilometers


def main():
    try:
        with open("coordinates_cache.json", "r") as cache_file:
            nodes = json.load(cache_file)

        print("Loaded saved coordinates.")

    except FileNotFoundError:
        nodes = {}

        for city in CITIES:
            city_coordinates = fetch_coordinates(city)

            nodes[city] = city_coordinates

            print(city, city_coordinates)

            time.sleep(1.1)

        with open("coordinates_cache.json", "w") as cache_file:
            json.dump(nodes, cache_file, indent=2)

        print("Saved coordinates_cache.json")

    total_locations = len(nodes)
    print("Total locations:", total_locations)

    connections = {}

    for city in CITIES:
        connections[city] = []

    for source_city, destination_city in ROAD_CONNECTIONS:
        source_coordinates = nodes[source_city]
        destination_coordinates = nodes[destination_city]

        forward_distance = fetch_road_distance(
            source_coordinates,
            destination_coordinates,
        )

        forward_connection = {
            "node": destination_city,
            "distance": forward_distance,
        }

        connections[source_city].append(forward_connection)

        print(
            source_city,
            "->",
            destination_city,
            forward_distance,
            "km",
        )

        time.sleep(1.1)

        reverse_distance = fetch_road_distance(
            destination_coordinates,
            source_coordinates,
        )

        reverse_connection = {
            "node": source_city,
            "distance": reverse_distance,
        }

        connections[destination_city].append(reverse_connection)

        print(
            destination_city,
            "->",
            source_city,
            reverse_distance,
            "km",
        )

        time.sleep(1.1)

    graph = {
        "region": REGION,
        "nodes": nodes,
        "connections": connections,
    }

    with open("map_data.json", "w") as graph_file:
        json.dump(graph, graph_file, indent=2)

    print("Saved map_data.json")


if __name__ == "__main__":
    main()





    



