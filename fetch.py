import requests
import json
import sys

# Format: South,West,North,East (Utah)
bbox = "36.99,-114.05,42.01,-109.04" 
query = f'[out:json][timeout:90];node["man_made"="surveillance"]({bbox});out;'

# 1. Add an ID badge so Overpass knows we aren't a spam bot
headers = {
    'User-Agent': 'Enterprise-Map-Sync/1.0 (Automated GitHub Action)'
}

print("Fetching data from OpenStreetMap...")
response = requests.get("https://overpass-api.de/api/interpreter", params={'data': query}, headers=headers)

# 2. Check if the server rejected us before we try to read the data
if response.status_code != 200:
    print(f"ERROR: The server rejected the request with code {response.status_code}.")
    print("Here is what the server said:")
    print(response.text)
    sys.exit(1) # Stop the script safely

# 3. Try to read the JSON safely
try:
    data = response.json()
except Exception as e:
    print("ERROR: Could not read the data as JSON. The server sent:")
    print(response.text)
    sys.exit(1)

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

print(f"Success! Saved {len(features)} cameras.")
