import json
import csv

all_rekts = []

for page_num in range(1, 79):
    filename = f'page{page_num}.json'
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            rekts = data['data']['rekts']
            
            for rekt in rekts:
                token = rekt.get('token', {})
                token_name = token.get('name', '')
                token_addresses = ','.join(token.get('addresses', []))
                
                # ========== FIX STARTS HERE ==========
                # Get chaindIds as a list (preserve original type)
                chaind_ids_list = rekt.get('chaindIds', [])
                
                # Convert all elements to strings and join with commas
                chaind_ids = ','.join(map(str, chaind_ids_list))  # Force string conversion
                # ========== FIX ENDS HERE ==========
                
                flattened = {
                    'id': rekt.get('id', ''),
                    'projectName': rekt.get('projectName', ''),
                    'description': rekt.get('description', ''),
                    'date': rekt.get('date', ''),
                    'fundsLost': rekt.get('fundsLost', ''),
                    'fundsReturned': rekt.get('fundsReturned', ''),
                    'chaindIds': chaind_ids,  # Now a string like "1,3"
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

# Write to CSV (unchanged)
csv_columns = [
    'id', 'projectName', 'description', 'date', 'fundsLost',
    'fundsReturned', 'chaindIds', 'category', 'issueType',
    'token_name', 'token_addresses'
]

with open('combined_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(all_rekts)

print("CSV file created: combined_data.csv")