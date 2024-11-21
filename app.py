from flask import Flask, request, render_template
import requests
import random

app = Flask(__name__)

# Random topics
TOPICS = ["Science", "Technology", "History", "Art", "Nature"]

# Logs to store data
logs = []

# Geolocation API
GEO_API_URL = "http://ip-api.com/json/"

# Helper to exclude localhost
def is_local(ip):
    return ip in ["127.0.0.1", "::1"]

@app.route('/')
def index():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    if is_local(client_ip):
        return render_template("index.html", message="Localhost access is not logged.")
    
    try:
        # Fetch geolocation data
        geo_response = requests.get(f"{GEO_API_URL}{client_ip}").json()
        city = geo_response.get("city", "Unknown City")
        country = geo_response.get("country", "Unknown Country")
        
        # Log the data
        logs.append({"ip": client_ip, "city": city, "country": country, "time": str(request.date)})
        
        # Choose a random topic
        random_topic = random.choice(TOPICS)
        return render_template("index.html", message=f"Your random topic is: {random_topic}")
    except Exception as e:
        return render_template("index.html", message="Error fetching geolocation data.")

@app.route('/logs')
def view_logs():
    return {"logs": logs}, 200

if __name__ == '__main__':
    app.run(debug=True)
