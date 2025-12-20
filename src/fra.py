from datetime import datetime
from functions import getHolidayData, getYearLinks, addMissingDayField, writeJsonIfChanged

# Date time format
outputFormat = "%Y-%m-%d"

# Source
url = "https://holidays-calendar.net/calendar_en/france_en.html"

yearLinks = getYearLinks(url)

datas = [];

for link in yearLinks:
  
  # grab the data
  print("\n\nworking on ", link);
  data = getHolidayData(link)

  datas = datas + data

# sort by dates
datas.sort(key=lambda r: r["date"])

for item in datas:
    item["date"] = item["date"].strftime(outputFormat)


# Output to file in json format
result = {
  "source": url,
  "country": "France",
  "countryAlpha2Code": "FR",
  "countryAlpha3Code": "FRA",
  "holidays": datas,
  "updated_on": datetime.now().replace(microsecond=0).isoformat()
}

# Add missing day fields
result = addMissingDayField(result)

# Write JSON file only if data has changed
writeJsonIfChanged(result, '../data/fra.json')
