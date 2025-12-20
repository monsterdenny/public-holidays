import requests
from lxml import html
from datetime import datetime, timedelta
import json
import os

def getYearLinks(url: str) -> list:
  # Get html content from source
  response = requests.get(url)

  # Parse using lxml
  tree = html.fromstring(response.content)

  # Resolve all relative links to be absolute
  tree.make_links_absolute(url)



  # Determine number of years to scrape
  yearLinks = tree.xpath("//div[contains(@class, 'year-menu')]/ul/li[not(contains(@class, 'holTBD'))]/a/@href")

  return yearLinks




def getHolidayData(url: str) -> list:
  # Date formats
  input_format = "%B %d %Y"
  output_format = "%Y-%m-%d"

  # Get html content from source
  response = requests.get(url)

  # Parse using lxml
  tree = html.fromstring(response.content)
  
  br_elements = tree.xpath("//br")

  # Iterate and drop each <br> tag
  for br in br_elements:
    br.drop_tag()

  # Grab the page title
  title = tree.xpath('//title/text()')[0] if tree.xpath('//title/text()') else "No title found"

  # extract year from title (Eg, "France Publich Holidays 2025")
  year = "".join([char for char in title if char.isdigit()])

  # Grab the holiday data
  selector = "//div[ contains(@class, 'details') and not(.//span/span[contains(text(), 'Regional')]) ]"

  holidays = tree.xpath(selector + "/div/span/span[1]/text()")

  holidayText = tree.xpath(selector + "/div/span/span[2]/text()")

  if len(holidays) != len(holidayText):
    print("Exception array length does not match")
    exit(1)

  datas = []
  for i in range(len(holidays)):
    dateString = holidays[i].strip()

    holidayName = holidayText[i].strip()

    

    # check if holiday span across few days
    if "–" in dateString:
      dates = dateString.split("–")
      if len(dates) != 2:
        print("Error unable to parse date range ",dateString)
        exit(1)
    
      startDate = dates[0].strip()
      endDate = dates[1].strip()

      if not(" " in endDate):
        #no month
        month = startDate.split(" ")[0]
        endDate = month + " " + endDate
    
      #Loop from start date till end date, append to array
      start = datetime.strptime(startDate + " " + year, input_format)
      end = datetime.strptime(endDate + " " + year, input_format)

      currentDate  = start
      while currentDate <= end:
        datas.append({"date": currentDate,"holiday":holidayName})

        currentDate += timedelta(days=1)

    else:

      # not date range
      datas.append({"date":datetime.strptime(dateString + " " + year, input_format),"holiday":holidayName})



    
  



  # dates = [{"holiday": datetime.strptime(holidays[i].strip() + " " + year, input_format).strftime(output_format) ,"holidayName": holidayText[i].strip()} for i in range(len(holidays))]

  print(f"Total records => {len(datas)}\n")

  #print("Dates\n",dates)

  return datas


def addMissingDayField(data: dict) -> dict:
  """
  Adds missing 'day' field to holiday entries by calculating the day of the week from the date.
  
  Args:
    data: Dictionary containing holiday data with 'holidays' array
    
  Returns:
    Updated dictionary with 'day' fields added where missing
  """
  if 'holidays' not in data:
    return data
  
  day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  
  for holiday in data['holidays']:
    if 'date' in holiday and 'day' not in holiday:
      try:
        # Parse the date string (format: YYYY-MM-DD)
        date_obj = datetime.strptime(holiday['date'], '%Y-%m-%d')
        # Get day of week (0 = Monday, 6 = Sunday)
        day_index = date_obj.weekday()
        holiday['day'] = day_names[day_index]
      except (ValueError, KeyError) as e:
        print(f"Warning: Could not parse date '{holiday.get('date', 'N/A')}': {e}")
        continue
  
  return data


def writeJsonIfChanged(result: dict, json_file_path: str) -> None:
  """
  Writes JSON file only if the holidays data has changed compared to existing file.
  
  Args:
    result: Dictionary containing holiday data with 'holidays' array
    json_file_path: Path to the JSON file to write (relative to script location)
  """
  file_exists = os.path.exists(json_file_path)
  
  if file_exists:
    try:
      with open(json_file_path, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
      
      # Normalize both datasets for comparison (sort by date and convert to comparable format)
      def normalize_holidays(holidays):
        # Create a list of tuples (date, holiday) for comparison, ignoring 'day' field
        return sorted([(h.get('date', ''), h.get('holiday', '')) for h in holidays])
      
      existing_holidays = normalize_holidays(existing_data.get('holidays', []))
      new_holidays = normalize_holidays(result.get('holidays', []))
      
      # Compare holidays data
      if existing_holidays == new_holidays:
        print("No changes detected. Keeping existing file.")
        print(f"Existing file last updated: {existing_data.get('updated_on', 'N/A')}")
      else:
        print("Changes detected. Updating file.")
        with open(json_file_path, 'w', encoding='utf-8') as f:
          json.dump(result, f, indent=4)
        print(f"File updated: {result['updated_on']}")
    except (json.JSONDecodeError, KeyError, IOError) as e:
      print(f"Error reading existing file: {e}. Overwriting with new data.")
      with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)
      print(f"File created/updated: {result['updated_on']}")
  else:
    print("File does not exist. Creating new file.")
    with open(json_file_path, 'w', encoding='utf-8') as f:
      json.dump(result, f, indent=4)
    print(f"File created: {result['updated_on']}")

