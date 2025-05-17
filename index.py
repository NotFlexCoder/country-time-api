from flask import Flask, request, jsonify
import pytz
from datetime import datetime
import pycountry

app = Flask(__name__)

def get_time_formats(tz):
    now = datetime.now(tz)
    time_24 = now.strftime('%H:%M:%S')
    time_12 = now.strftime('%I:%M:%S %p')
    return time_24, time_12

def search_timezones_by_keyword(keyword):
    keyword = keyword.replace(' ', '_').lower()
    matches = []
    for tz_name in pytz.all_timezones:
        if keyword in tz_name.lower():
            try:
                tz = pytz.timezone(tz_name)
                t24, t12 = get_time_formats(tz)
                city = tz_name.split('/')[-1].replace('_', ' ')
                matches.append({
                    "city": city,
                    "status": "success",
                    "time_24hr": t24,
                    "time_12hr": t12
                })
            except Exception:
                matches.append({
                    "city": tz_name,
                    "status": "error",
                    "time_24hr": None,
                    "time_12hr": None
                })
    return matches

@app.route('/')
def timezone():
    city = request.args.get('city', '').strip()
    village = request.args.get('village', '').strip()
    country_name = request.args.get('country', '').strip()

    if city:
        results = search_timezones_by_keyword(city)
        if not results:
            return jsonify({"status": "error", "message": f"No timezones found matching city '{city}'"}), 404
        return jsonify({"status": "success", "query_type": "city", "query": city, "cities": results})

    if village:
        results = search_timezones_by_keyword(village)
        if not results:
            return jsonify({"status": "error", "message": f"No timezones found matching village '{village}'"}), 404
        return jsonify({"status": "success", "query_type": "village", "query": village, "cities": results})

    if country_name:
        try:
            country = pycountry.countries.lookup(country_name)
        except LookupError:
            return jsonify({"status": "error", "message": "Invalid country name"}), 400
        
        country_code = country.alpha_2
        timezones = [tz for tz in pytz.all_timezones if tz.startswith(country_code + '/') or (country_code in tz)]
        if not timezones:
            timezones = [tz for tz in pytz.all_timezones if country_name.replace(' ','_').lower() in tz.lower()]

        if not timezones:
            return jsonify({"status": "error", "message": "No timezones found for this country"}), 404
        
        city_times = []
        for tz_name in timezones:
            try:
                tz = pytz.timezone(tz_name)
                t24, t12 = get_time_formats(tz)
                city = tz_name.split('/')[-1].replace('_',' ')
                city_times.append({
                    "city": city,
                    "status": "success",
                    "time_24hr": t24,
                    "time_12hr": t12
                })
            except Exception:
                city_times.append({
                    "city": tz_name,
                    "status": "error",
                    "time_24hr": None,
                    "time_12hr": None
                })
        return jsonify({"status": "success", "query_type": "country", "query": country_name, "cities": city_times})

    return jsonify({"status": "error", "message": "Provide at least one query parameter: country, city, or village"}), 400

if __name__ == '__main__':
    app.run()
