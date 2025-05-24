import json
import csv

# List to hold all flattened entries
all_rekts = []

# Process each JSON file from page1.json to page78.json
for page_num in range(1, 79):
    filename = f'page{page_num}.json'
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            rekts = data['data']['rekts']
            
            # Flatten each entry
            for rekt in rekts:
                # Flatten token data
                token = rekt.get('token', {})
                token_name = token.get('name', '')
                token_addresses = ','.join(token.get('addresses', []))
                
                # Flatten chaindIds (note the typo in the JSON key)
                chaind_ids = ','.join(map(str, rekt.get('chaindIds', [])))
                
                # Create a flattened entry
                flattened = {
                    'id': rekt.get('id', ''),
                    'projectName': rekt.get('projectName', ''),
                    'description': rekt.get('description', ''),
                    'date': rekt.get('date', ''),
                    'fundsLost': rekt.get('fundsLost', ''),
                    'fundsReturned': rekt.get('fundsReturned', ''),
                    'chaindIds': chaind_ids,
                    'category': rekt.get('category', ''),
                    'issueType': rekt.get('issueType', ''),
                    'token_name': token_name,
                    'token_addresses': token_addresses
                }
                all_rekts.append(flattened)
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Skipping.")
    except KeyError as e:
        print(f"Error: {filename} has invalid structure. Key {e} not found.")

# Define CSV columns (order matters)
csv_columns = [
    'id', 'projectName', 'description', 'date', 'fundsLost',
    'fundsReturned', 'chaindIds', 'category', 'issueType',
    'token_name', 'token_addresses'
]

# Write to CSV
with open('combined_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(all_rekts)

print("CSV file created: combined_data.csv")