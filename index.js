import express from "express"
import fetch from "node-fetch"

const app = express()

app.get("/", async (req, res) => {
  const country = req.query.country
  if (!country) {
    return res.json({ status: "error", message: "No country provided" })
  }

  try {
    const zonesRes = await fetch("https://worldtimeapi.org/api/timezone")
    const allZones = await zonesRes.json()

    const matchedZones = allZones.filter(zone => zone.toLowerCase().includes(country.toLowerCase()))
    if (matchedZones.length === 0) {
      return res.json({ status: "error", message: "No matching timezones found" })
    }

    const timeResults = await Promise.all(
      matchedZones.map(async zone => {
        try {
          const timeRes = await fetch(`https://worldtimeapi.org/api/timezone/${zone}`)
          const timeData = await timeRes.json()

          const date = new Date(timeData.datetime)
          return {
            city: zone,
            time_24hr: date.toTimeString().split(" ")[0],
            time_12hr: date.toLocaleTimeString("en-US", { hour12: true }),
          }
        } catch {
          return null
        }
      })
    )

    const filteredResults = timeResults.filter(item => item !== null)
    if (filteredResults.length === 0) {
      return res.json({ status: "error", message: "No valid timezones retrieved" })
    }

    res.json({
      status: "success",
      data: filteredResults
    })
  } catch {
    res.json({ status: "error", message: "Internal error occurred" })
  }
})

export default app
