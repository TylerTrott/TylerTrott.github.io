import json
from collections import defaultdict
import os

# Load GeoJSON
file_path = os.path.join(os.path.dirname(__file__), 'Traffic_Volume.geojson')
with open(file_path) as f:
    data = json.load(f)

flows = defaultdict(lambda: {'in': 0, 'out': 0})

for feature in data['features']:
    coords = feature['geometry']['coordinates']
    start = tuple(coords[0])
    end = tuple(coords[-1])

    # Check if 'Label' exists and is not None
    label = feature['properties'].get('Label', None)
    if label is None:
        print(f"Skipping feature at {start} to {end} because 'Label' is missing or None")
        continue  # Skip this feature if Label is missing

    # Extract volume from label like "450(92)"
    volume_str = label.split('(')[0].strip()  # Get '450' from "450(92)"
    volume_str = volume_str.rstrip(')')  # Remove any trailing closing parenthesis
    try:
        volume = int(volume_str)  # Convert to integer
    except ValueError:
        print(f"Skipping feature at {start} to {end} because volume is invalid: {label}")
        continue  # Skip this feature if volume cannot be converted to integer

    # Check if the flow is going in the correct direction:
    if start != end:  # We only care about flows between different nodes
        flows[start]['out'] += volume  # Outflow from the start node
        flows[end]['in'] += volume  # Inflow to the end node
    else:
        # If start and end are the same, skip or treat as self-loop
        print(f"Skipping self-loop for node {start}")
        continue

# Example inflow-outflow balance
for node, values in flows.items():
    inflow = values['in']
    outflow = values['out']
    print(f"Node {node}: Inflow = {inflow}, Outflow = {outflow}, Δ = {inflow - outflow}")
