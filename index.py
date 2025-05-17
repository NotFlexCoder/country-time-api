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

@app.route('/')
def timezone():
    country_name = request.args.get('country', '').strip()
    if not country_name:
        return jsonify({"status": "error", "message": "country parameter is required"}), 400

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

    return jsonify({
        "status": "success",
        "query_type": "country",
        "query": country_name,
        "cities": city_times
    })

if __name__ == '__main__':
    app.run()
