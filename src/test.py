

import requests
from lxml import html,etree
import json

# sgp test
def sgpTest():
  with open('sgp.json', 'r') as f:
    data = json.load(f)
  
  # object reference
  holidays = data['holidays']
  
  # Iterate and remove the field _id and massage field
  for item in holidays:
    if "_id" in item:  # Check if the field exists before attempting to delete
      del item["_id"]
    
    if "date" in item:
      item['date'] = item['date'].strip()

    if "day" in item:
      item['day'] = item['day'].strip()
    
    if "holiday" in item:
      item['holiday'] = item['holiday'].strip()
  
  
  with open('sgp.json', 'w') as f:
    json.dump(data, f, indent=4)

    

sgpTest()

# xpath test
def test1():
  tree = html.parse("test.html")

  br_elements = tree.xpath("//br")

  # Iterate and drop each <br> tag
  for br in br_elements:
      br.drop_tag()

  # # Grab the holiday data
  # selector = "//div[ contains(@class, 'details') and not(.//span/span[contains(text(), 'Regional')]) ]"

  # holidays = tree.xpath(selector + "/div/span/span[1]//text()")

  # holidayText = tree.xpath(selector + "/div/span/span[2]//text()")
  # print(holidays)
  # print(holidayText)

  # if isinstance(holidayText,list):
  #   holidayText = [item.strip() for item in holidayText]
  #   holidayText = " ".join(holidayText)
    
  # print(holidayText)


  # Key Value Pair
  values = tree.xpath("//div[contains(@class, 'details')] ! map{'key': div/span/span[1]/text(), 'value': div/span/span[2]/text()}")

  print(values)