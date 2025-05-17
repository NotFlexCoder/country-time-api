from flask import Flask, request, jsonify
import pytz
from timezonefinder import TimezoneFinder
from datetime import datetime
import pycountry
import json

app = Flask(__name__)
tf = TimezoneFinder()

def get_cities_by_country(country_name):
    cities = []
    try:
        country = pycountry.countries.get(name=country_name)
        if not country:
            country = pycountry.countries.search_fuzzy(country_name)[0]
    except:
        return None
    country_code = country.alpha_2

    with open('cities.json') as f:
        data = json.load(f)

    for city in data:
        if city.get('country') == country_code:
            cities.append(city['name'])
    return cities

def get_timezone_for_city(city, country_code):
    with open('cities.json') as f:
        data = json.load(f)
    for c in data:
        if c['name'] == city and c['country'] == country_code:
            lat, lon = c['lat'], c['lng']
            tz = tf.timezone_at(lat=lat, lng=lon)
            return tz
    return None

@app.route('/time')
def time_by_country():
    country_name = request.args.get('country')
    if not country_name:
        return jsonify({"status":"error", "message":"Country parameter missing"}), 400

    cities = get_cities_by_country(country_name)
    if not cities:
        return jsonify({"status":"error", "message":"Country not found or no cities available"}), 404

    country = pycountry.countries.get(name=country_name)
    if not country:
        country = pycountry.countries.search_fuzzy(country_name)[0]
    country_code = country.alpha_2

    results = []
    for city in cities:
        tz_name = get_timezone_for_city(city, country_code)
        if not tz_name:
            continue
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        time_24 = now.strftime("%H:%M:%S")
        time_12 = now.strftime("%I:%M:%S %p")
        results.append({
            "city": city,
            "timezone": tz_name,
            "time_24h": time_24,
            "time_12h": time_12
        })

    return jsonify({"status":"success", "country":country_name, "data": results})

if __name__ == "__main__":
    app.run()
