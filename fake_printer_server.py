from flask import Flask, jsonify

app = Flask(__name__)

# Simulated printer data
PRINTER_DATA = {
    "model": "HP LaserJet Pro MFP M227fdw",
    "manufacturer": "HP",
    "status": "Online",
    "connectionType": "WiFi",
    "macAddress": "00:1A:2B:3C:4D:5E",
    "duplex": True,
    "powerConsumption": 500,  # Watts
    "cartridges": [
        {"color": "Black", "status": "OK", "level": 85, "capacity_ml": 50},
        {"color": "Cyan", "status": "Low", "level": 15, "capacity_ml": 50},
        {"color": "Magenta", "status": "OK", "level": 60, "capacity_ml": 50},
        {"color": "Yellow", "status": "OK", "level": 70, "capacity_ml": 50}
    ],
    "paperTrays": [
        {"trayNumber": 1, "paperSize": "A4", "capacity": 200, "used": 50},
        {"trayNumber": 2, "paperSize": "Letter", "capacity": 150, "used": 30}
    ],
    "pageCount": 1500
}

@app.route("/api/pagecount", methods=["GET"])
def get_printer_data():
    """Simulated API endpoint to return printer details."""
    return jsonify(PRINTER_DATA)

if __name__ == "__main__":
    print("🚀 Fake Printer API Server is running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)