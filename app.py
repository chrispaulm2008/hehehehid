from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = requests.get(f"http://ip-api.com/json/{user_ip}")

    if response.status_code == 200:
        location_data = response.json()
        city = location_data.get("city", "Unknown")
        country = location_data.get("country", "Unknown")
        region = location_data.get("regionName", "Unknown")
        return jsonify({
            "ip": user_ip,
            "city": city,
            "region": region,
            "country": country
        })
    else:
        return jsonify({"error": "Unable to retrieve location data"}), 500

if __name__ == "__main__":
    app.run(debug=True)
