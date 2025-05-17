import express from "express"
import fetch from "node-fetch"

const app = express()

app.get("/", async (req, res) => {
  const country = req.query.country
  if (!country) return res.json({ status: "error", message: "No country provided" })

  try {
    const zonesRes = await fetch("https://api.timezonedb.com/v2.1/list-time-zone?format=json&fields=zoneName,countryName")
    const zonesData = await zonesRes.json()
    if (zonesData.status !== "OK") return res.json({ status: "error", message: "Failed to get zones" })

    const filteredZones = zonesData.zones.filter(z => z.countryName.toLowerCase().includes(country.toLowerCase()))
    if (filteredZones.length === 0) return res.json({ status: "error", message: "No matching zones found" })

    const timeResults = await Promise.all(filteredZones.map(async zone => {
      try {
        const timeRes = await fetch(`http://worldclockapi.com/api/json/utc/now`)
        const timeData = await timeRes.json()
        const now = new Date(timeData.currentDateTime)
        return {
          city: zone.zoneName,
          time_24hr: now.toTimeString().split(" ")[0],
          time_12hr: now.toLocaleTimeString("en-US", { hour12: true })
        }
      } catch {
        return null
      }
    }))

    const results = timeResults.filter(r => r !== null)
    if (results.length === 0) return res.json({ status: "error", message: "No valid timezones retrieved" })

    res.json({ status: "success", data: results })
  } catch {
    res.json({ status: "error", message: "Internal error" })
  }
})

export default app
