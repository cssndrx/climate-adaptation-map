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
        name = row['Company Name']
        description = row['Description']
        category = row['Drawdown Category']
        website = row['Website']
        employees = row['Number of employees']
        active_jobs = row['Number of active jobs']

        datum = {'name': name}
        # Escape single quotes in the description for JavaScript compatibility
        try:
            description = description.replace("'", "\\'")
        except AttributeError:
            description = ''

        # Append the data as a dictionary to the list in the correct category
        if pd.notna(description):
            datum['description'] = description
        if pd.notna(website):
            datum['website'] = website
        if pd.notna(employees):
            datum['employees'] = employees
        if pd.notna(active_jobs):
            datum['active_jobs'] = active_jobs
        categorized_data[category].append(datum)

    # Sort alphabetically
    for category in categorized_data:
        categorized_data[category] = sorted(categorized_data[category], key=lambda x: x['name'])

    # Convert Python dictionary to JSON string that is JavaScript compatible
    js_object = json.dumps(categorized_data, indent=2)
    return js_object


# Usage example
csv_file_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTZ1PwInqh0KBOa_EemXo-_ZVOrHPYXD8dAmwaa88kikPvE2YQkOaxjbjcLHuJvgkbQs_gPbWB_XKKn/pub?gid=1919626651&single=true&output=csv'
js_output = process_csv_to_js_object(csv_file_path)

# Print the JavaScript object
with open('mapping.js', 'w') as f:
    f.write(f"const mapping = {js_output};")