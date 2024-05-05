import csv
from collections import defaultdict
import json
import pandas as pd

def process_csv_to_js_object(file_path):
    # Read the CSV file using pandas
    df = pd.read_csv(file_path, encoding='utf-8', dtype=str)

    # Create a dictionary to hold the categories and their corresponding items
    categorized_data = defaultdict(list)

    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        name = str(row['Name'])
        if not name:
            continue

        description = row['Description']
        themes = row['Themes']
        subthemes = row['Sub-themes']
        tech = row['Tech']
        distribution = row['Distribution']
        website = row['Site']

        datum = {'name': name}
        # Escape single quotes in the description for JavaScript compatibility
        try:
            description = description.replace("'", "\\'")
        except AttributeError:
            description = ''

        if pd.notna(themes):
            themes = themes.split(',')
        else:
            themes = []
        if pd.notna(subthemes):
            subthemes = subthemes.split(',')
        else:
            subthemes = []

        # Append the data as a dictionary to the list in the correct category
        for var_name in ['description', 'themes', 'subthemes', 'tech', 'distribution', 'website']:
            if pd.notna(var_name):
                datum[var_name] = locals().get(var_name)

        all_themes = themes + subthemes
        all_themes = [theme.strip().strip('"').lower() for theme in all_themes]
        all_themes = set(all_themes)
        for theme in all_themes:
            try:
                categorized_data[theme].append(datum)
            except TypeError:
                breakpoint()

    # Sort alphabetically
    for category in categorized_data:
        categorized_data[category] = sorted(categorized_data[category], key=lambda x: x['name'])

    # Convert Python dictionary to JSON string that is JavaScript compatible
    js_object = json.dumps(categorized_data, indent=2)
    return js_object


# Usage example
csv_file_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTTFQRxrkPg9v9SQEUmXVbrnWPbAf3mRlrfeZhflxWT334vtpuSZ4mGmKSmG3foN3UKm1o0RYPnYOmb/pub?gid=0&single=true&output=csv'
js_output = process_csv_to_js_object(csv_file_path)

# Print the JavaScript object
with open('mapping.js', 'w') as f:
    f.write(f"const mapping = {js_output};")