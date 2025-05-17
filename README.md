# 🌍 Country Timezone API

A lightweight Flask-based API that provides the current time (in both 24-hour and 12-hour formats) for all cities in a given country using Python libraries like `pytz` and `pycountry`.

Perfect for integration into bots, world clocks, international apps, or location-based services.

---

## 🚀 Features

- 🕓 Get current time for **every timezone** in a country.
- 🔍 Automatically resolves country names to ISO codes.
- 🕰️ Returns both 24-hour and 12-hour time formats.
- ❌ Handles invalid input gracefully with clear error messages.
- ⚙️ Built with Flask – easy to deploy and customize.

---

## 🛠️ Requirements

- Python 3.7 or higher
- Flask
- pytz
- pycountry

Install dependencies using:

```bash
pip install Flask pytz pycountry
```

---

## 📡 Usage

### 1. **Run the server**:

```bash
python app.py
```

> By default, it runs on: `http://127.0.0.1:5000/`

---

### 2. **Make a GET request**:

**Endpoint**: `/`  
**Parameter**: `country` (required)

#### Example:

```bash
curl "http://127.0.0.1:5000/?country=India"
```

---

## 📄 Example Response

```json
{
  "status": "success",
  "query_type": "country",
  "query": "India",
  "cities": [
    {
      "city": "Kolkata",
      "status": "success",
      "time_24hr": "16:35:12",
      "time_12hr": "04:35:12 PM"
    }
  ]
}
```

---

## ⚠️ Error Handling

- **Missing Country Parameter**:
```json
{
  "status": "error",
  "message": "country parameter is required"
}
```

- **Invalid Country Name**:
```json
{
  "status": "error",
  "message": "Invalid country name"
}
```

- **No Timezones Found**:
```json
{
  "status": "error",
  "message": "No timezones found for this country"
}
```

---

## 📝 License

This project is licensed under the MIT License – see the [LICENSE](https://github.com/NotFlexCoder/timezone-api/blob/main/LICENSE) file for details.
