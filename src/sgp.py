import requests
from functions import addMissingDayField, writeJsonIfChanged, createHolidayResult, getOutputPath

def getSgHolidayData(datesetId:str) -> list:
  
  url = "https://data.gov.sg/api/action/datastore_search?resource_id={}".format(datesetId)
        
  response = requests.get(url)
  jsonData = response.json()



  return jsonData['result']['records']

#singapore holiday source
collection_id = 691          
url = "https://api-production.data.gov.sg/v2/public/api/collections/{}/metadata".format(collection_id)
country_alpha3_code = "SGP"
outputPath = getOutputPath(country_alpha3_code)
        
response = requests.get(url)

datasets = response.json()

childDatasets = datasets['data']['collectionMetadata']['childDatasets']

datas = []
for datasetId in childDatasets:
  datas = datas + getSgHolidayData(datasetId)


# Iterate and remove the field _id and massage field
for item in datas:
  if "_id" in item:  # Check if the field exists before attempting to delete
    del item["_id"]
  
  if "date" in item:
    item['date'] = item['date'].strip()

  if "day" in item:
    item['day'] = item['day'].strip()
  
  if "holiday" in item:
    item['holiday'] = item['holiday'].strip()

#sort by date string
datas.sort(key=lambda row: row['date'])



# Create standardised result dictionary
result = createHolidayResult(
  source_url=url,
  country="Singapore",
  country_alpha2_code="SG",
  country_alpha3_code=country_alpha3_code,
  holidays_data=datas
)

# Add missing day fields
result = addMissingDayField(result)

# Write JSON file only if data has changed
writeJsonIfChanged(result, outputPath)
