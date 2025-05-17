import express from "express"
import fetch from "node-fetch"

const app = express()
app.use(express.json())

app.get("/", async (req, res) => {
  const country = req.query.country
  if (!country) return res.json({ status: "error", message: "No country provided" })

  try {
    const zonesRes = await fetch("https://timeapi.io/api/TimeZone/AvailableTimeZones")
    const zones = await zonesRes.json()

    const filteredZones = zones.filter(zone => zone.toLowerCase().includes(country.toLowerCase()))
    if (filteredZones.length === 0) return res.json({ status: "error", message: "No cities found for this country" })

    const timePromises = filteredZones.map(async zone => {
      try {
        const timeRes = await fetch(`https://timeapi.io/api/Time/current/zone?timeZone=${encodeURIComponent(zone)}`)
        const timeData = await timeRes.json()
        const date = new Date(`${timeData.date}T${timeData.time}`)
        return {
          city: zone.split("/").slice(1).join("/").replace("_", " "),
          time_24hr: date.toTimeString().split(" ")[0],
          time_12hr: date.toLocaleTimeString("en-US", { hour: "numeric", minute: "numeric", second: "numeric", hour12: true }),
          status: "success"
        }
      } catch {
        return {
          city: zone.split("/").slice(1).join("/").replace("_", " "),
          status: "error"
        }
      }
    })

    const result = await Promise.all(timePromises)
    res.json(result)
  } catch {
    res.json({ status: "error", message: "Something went wrong" })
  }
})

export default app
