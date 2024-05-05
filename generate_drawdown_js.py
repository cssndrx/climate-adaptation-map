import csv

# Define the path to your CSV file
csv_file_path = 'drawdown.csv'

# List to hold the converted data
solutions = []

# Open the CSV file and read its contents
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract the necessary fields and convert numerical values properly
        name = row['SOLUTION']
        sectors = row['SECTORS']
        impact = float(row['SCENARIO 1'])

        # Add each solution as a dictionary to the list
        solution = {
            'name': name,
            'sector': sectors,
            'impact': impact
        }
        solutions.append(solution)

# Print the JavaScript variable declaration
print("const solutions = [")
for solution in solutions:
    print(f"  {{name: '{solution['name']}', sector: '{solution['sector']}', impact: {solution['impact']}}},")
print("];")