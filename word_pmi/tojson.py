import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # Create an empty list to store the data
    data = []

    # Open the CSV file for reading
    with open(csv_file_path, encoding='gbk') as csvf:
        # Load the CSV data using DictReader
        csv_reader = csv.DictReader(csvf)

        # Convert each row into a dictionary and add it to data
        for row in csv_reader:
            data.append(row)

    # Open the JSON file for writing
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        # Write the data as a JSON file
        jsonf.write(json.dumps(data, indent=4))

# Example usage
csv_file_path = '1.csv'
json_file_path = 'output.json'
csv_to_json(csv_file_path, json_file_path)
