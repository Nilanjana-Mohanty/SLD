from flask import Flask, render_template, request, jsonify
import requests
import csv
import os
from datetime import datetime

app = Flask(__name__)

ESP32_IP = "http://192.168.137.122"  # <-- Replace with your ESP32 IP
RAW_FILE = "raw_data.csv"
AVG_FILE = "averages.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    label = request.json.get('label')
    try:
        r = requests.get(f"{ESP32_IP}/capture", params={'label': label}, timeout=20)
        data = r.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    samples = data['samples']
    average = data['average']

    # --- Save raw data ---
    raw_exists = os.path.isfile(RAW_FILE)
    with open(RAW_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not raw_exists:
            header = ["timestamp", "label", "sample_index"] + [f"sensor{i+1}" for i in range(len(samples[0]))]
            writer.writerow(header)
        for i, s in enumerate(samples):
            writer.writerow([timestamp, label, i+1] + s)

    # --- Save averages ---
    avg_exists = os.path.isfile(AVG_FILE)
    with open(AVG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not avg_exists:
            header = ["timestamp", "label"] + [f"avg_sensor{i+1}" for i in range(len(average))]
            writer.writerow(header)
        writer.writerow([timestamp, label] + average)

    return jsonify({"label": label, "average": average, "samples": samples})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
