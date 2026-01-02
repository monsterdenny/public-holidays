
from functions import addMissingDayField, writeJsonIfChanged, createHolidayResult, getOutputPath
from parser.holidays_calendar import getHolidaysCalendarData

# Source
url = "https://holidays-calendar.net/calendar_en/vietnam_en.html"
country_alpha3_code = "VNM"
outputPath = getOutputPath(country_alpha3_code)

datas = getHolidaysCalendarData(url)


# Create standardised result dictionary
result = createHolidayResult(
  source_url=url,
  country="Vietnam",
  country_alpha2_code="VN",
  country_alpha3_code=country_alpha3_code,
  holidays_data=datas
)

# Add missing day fields
result = addMissingDayField(result)

# Write JSON file only if data has changed
writeJsonIfChanged(result, outputPath)
