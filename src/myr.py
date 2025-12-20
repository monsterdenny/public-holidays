import requests
from datetime import datetime
from lxml import html
from functions import addMissingDayField, writeJsonIfChanged

def crawlData(year:int) -> list:
  
  crawlURL = "https://www.officeholidays.com/countries/malaysia/{}".format(year)
  response = requests.get(crawlURL)

  #print(response.content)
  # Parse using lxml
  tree = html.fromstring(response.content)

  # and .//tbody/tr/td[contains(text(),'National')] 
  # Get the h2 tags for yyyy-public-holidays
  dates = tree.xpath("//table[contains(@class,'country-table')]/tbody/tr[./td[position() = 4 and text() = 'National Holiday']]/td[2]/time/@datetime")

  names = tree.xpath("//table[contains(@class,'country-table')]/tbody/tr[./td[position() = 4 and text() = 'National Holiday']]/td[3]/*/text()")




  if len(dates) != len(names):
    print("Range don't match")
    exit(1)

  data = [{'date': dates[i], 'holiday': names[i]} for i in range(len(dates))]

  return data

#malaysia holiday source
url = "https://www.officeholidays.com/countries/malaysia"

startYear = datetime.now().year
endYear = startYear + 1
dataYears = [startYear,endYear]

finalData = []
for yearToCrawl in dataYears:
  finalData += crawlData(yearToCrawl)

# Output to file in json format
result = {
  "source": url,
  "country": "Malaysia",
  "countryAlpha2Code": "MY",
  "countryAlpha3Code": "MYR",
  "holidays": finalData,
  "updated_on": datetime.now().replace(microsecond=0).isoformat()
}

# Add missing day fields
result = addMissingDayField(result)

# Write JSON file only if data has changed
writeJsonIfChanged(result, '../data/myr.json')
