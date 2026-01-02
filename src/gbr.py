from functions import addMissingDayField, writeJsonIfChanged, createHolidayResult, getOutputPath
from parser.gov_uk import getGovUkBankHolidays

# Source
url = "https://www.gov.uk/bank-holidays"
country_alpha3_code = "GBR"
outputPath = getOutputPath(country_alpha3_code)

datas = getGovUkBankHolidays(url)

# Create standardised result dictionary
result = createHolidayResult(
  source_url=url,
  country="United Kingdom",
  country_alpha2_code="GB",
  country_alpha3_code=country_alpha3_code,
  holidays_data=datas,
  country_regions=["All", "Scotland", "England and Wales", "Northern Ireland"]
)

# Add missing day fields
result = addMissingDayField(result)

# Write JSON file only if data has changed
writeJsonIfChanged(result, outputPath)
