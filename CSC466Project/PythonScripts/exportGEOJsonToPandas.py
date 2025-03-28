import json
import pandas as pd
import re

# Load GeoJSON file
with open("./Traffic_Volume.geojson", "r") as f:
    data = json.load(f)

# Extract features
features = data["features"]
rows = []

for feature in features:
    properties = feature["properties"]
    geometry = feature["geometry"]

    # Safely handle the Label field
    label = properties.get("Label", "")  # Use empty string if Label is None
    traffic_volume = None  # Default to None if no valid match is found
    if label:
        traffic_volume_match = re.search(r"^\d+", label)
        if traffic_volume_match:
            traffic_volume = int(traffic_volume_match.group())
    
    # Extract Year safely
    year_str = properties["Year"]
    if isinstance(year_str, str):  # Ensure it's a string before processing
        if re.match(r"^\d{4}$", year_str):  # Already a 4-digit year
            year = int(year_str)
        elif re.match(r".*/.*/\d{4}$", year_str):  # If it's a date, extract the year
            year = int(year_str.split("/")[-1])
        else:
            year = None  # Handle unexpected cases
    else:
        year = int(year_str) if isinstance(year_str, int) else None  # Handle numbers properly

    # Extract start and end coordinates
    coordinates = geometry["coordinates"]
    start_coordinates = tuple(coordinates[0]) if coordinates else None
    end_coordinates = tuple(coordinates[-1]) if coordinates else None

    # Add row to the list
    row = {
        "OBJECTID": properties["OBJECTID"],
        "Traffic_Volume": traffic_volume,
        "Direction": properties["Direction"],
        "Segment_Length": properties["SHAPE_Length"],
        "Year": year,
        "Start_Coordinates": start_coordinates,
        "End_Coordinates": end_coordinates,
    }
    
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Display the first few rows
print(df.head())

# Save as CSV (optional)
df.to_csv("traffic_data.csv", index=False)
