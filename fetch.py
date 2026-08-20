import requests
import json

# Format: South,West,North,East
bbox = "36.99,-114.05,42.01,-109.04" 
query = f'[out:json][timeout:25];node["man_made"="surveillance"]({bbox});out;'

print("Fetching data from OpenStreetMap...")
response = requests.get("https://overpass-api.de/api/interpreter", params={'data': query})
data = response.json()

features = []
for elem in data.get('elements', []):
    if elem.get('type') == 'node':
        tags = elem.get('tags', {})
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [elem['lon'], elem['lat']]
            },
            "properties": {
                "osm_id": elem['id'],
                "type": tags.get('surveillance', 'Camera'),
                "operator": tags.get('operator', 'Unknown')
            }
        })

# Save the data
with open('cameras.geojson', 'w') as f:
    json.dump({"type": "FeatureCollection", "features": features}, f)

print(f"Saved {len(features)} cameras.")
