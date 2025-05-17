from flask import Flask, request, jsonify
import pytz
from datetime import datetime
import pycountry

app = Flask(__name__)

def get_time_formats(tz):
    now = datetime.now(tz)
    return now.strftime('%H:%M:%S'), now.strftime('%I:%M:%S %p')

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
    args = request.args
    country_name = args.get('country', '').strip()
    if country_name:
        try:
            country = pycountry.countries.lookup(country_name)
        except LookupError:
            return jsonify({"status": "error", "message": "Invalid country name"}), 400
        country_code = country.alpha_2
        timezones = pytz.country_timezones.get(country_code)
        if not timezones:
            return jsonify({"status": "error", "message": "No timezones found for this country"}), 404
        city_times = []
        for tz_name in timezones:
            try:
                tz = pytz.timezone(tz_name)
                t24, t12 = get_time_formats(tz)
                city = tz_name.split('/')[-1].replace('_', ' ')
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

    keywords = {k: v.strip() for k, v in args.items() if k != 'country' and v.strip()}
    if not keywords:
        return jsonify({"status": "error", "message": "Provide at least one query parameter: country, city, state, village, etc."}), 400

    results = []
    for key, val in keywords.items():
        found = search_timezones_by_keyword(val)
        if found:
            results.extend(found)

    if not results:
        first_key = list(keywords.keys())[0]
        return jsonify({"status": "error", "message": f"No timezones found matching {first_key}"}), 404

    # remove duplicates by city name
    seen = set()
    unique_results = []
    for r in results:
        if r["city"].lower() not in seen:
            seen.add(r["city"].lower())
            unique_results.append(r)

    first_key = list(keywords.keys())[0]
    first_val = keywords[first_key]
    return jsonify({"status": "success", "query_type": first_key, "query": first_val, "cities": unique_results})

if __name__ == '__main__':
    app.run()
