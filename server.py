from flask import Flask, request, jsonify
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

# File path to the CSV storing product keys, days of activation, activation status, and activation date
keys_csv_file = 'C:/Users/archi/Desktop/ADSAS/Untitled Folder/bypass/keys.csv'

def read_keys_from_csv(filename):
    """Read product keys, days of activation, activation status, and activation date from CSV file."""
    keys = {}
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key = row[0]
            days_of_activation = int(row[1])
            activation_status = bool(int(row[2]))  # Convert '0' or '1' to False or True
            activation_date = row[3] if row[3] != 'NaN' else None  # Store date if available
            keys[key] = {
                'days_of_activation': days_of_activation,
                'activated': activation_status,
                'activation_date': activation_date
            }
    return keys

def write_keys_to_csv(filename, keys):
    """Write product keys, days of activation, activation status, and activation date to CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, info in keys.items():
            activation_date = info['activation_date'] if info['activation_date'] else 'NaN'
            writer.writerow([key, info['days_of_activation'], int(info['activated']), activation_date])  # Convert False or True to '0' or '1'

@app.route('/activate', methods=['POST'])
def activate():
    data = request.json
    product_key = data.get('product_key')
    device_id = data.get('device_id')

    valid_keys = read_keys_from_csv(keys_csv_file)
    
    if product_key in valid_keys:
        key_info = valid_keys[product_key]
        if not key_info['activated']:
            # Mark the product key as activated, calculate expiration date, and save activation date
            activation_date = datetime.now().strftime('%Y-%m-%d')
            expiration_date = datetime.now() + timedelta(days=key_info['days_of_activation'])
            key_info['activated'] = True
            key_info['activation_date'] = activation_date
            write_keys_to_csv(keys_csv_file, valid_keys)  # Update CSV file
            return jsonify({"status": "success", "message": "Product activated successfully!", "expiry_date": expiration_date.strftime('%Y-%m-%d')}), 200
        else:
            return jsonify({"status": "error", "message": "Product key is already used."}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid product key."}), 400

if __name__ == '__main__':
    app.run()


#ngrok http --domain=leading-kind-panther.ngrok-free.app 5000
