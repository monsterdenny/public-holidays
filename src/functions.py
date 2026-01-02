

from datetime import datetime
import json
import os


def getOutputPath(country_alpha3_code: str) -> str:
  """
  Generates the output path for a holiday JSON file based on country alpha-3 code.
  
  Args:
    country_alpha3_code: ISO 3166-1 alpha-3 country code (e.g., "SGP", "FRA")
    
  Returns:
    Output path string in format '../data/{code}.json' (lowercase)
  """
  return '../data/{}.json'.format(country_alpha3_code.lower())


def createHolidayResult(source_url: str, country: str, country_alpha2_code: str, country_alpha3_code: str, holidays_data: list, country_regions: list = None) -> dict:
  """
  Creates a standardised holiday result dictionary.
  
  Args:
    source_url: Source URL where the holiday data was crawled from
    country: Country name
    country_alpha2_code: ISO 3166-1 alpha-2 country code (e.g., "SG", "FR")
    country_alpha3_code: ISO 3166-1 alpha-3 country code (e.g., "SGP", "FRA")
    holidays_data: List of holiday dictionaries with 'date' and 'holiday' fields
    country_regions: Optional list of country regions (e.g., ["All", "Scotland", "England and Wales", "Northern Ireland"])
    
  Returns:
    Dictionary with standardised holiday data structure
  """
  result = {
    "source": source_url,
    "country": country,
    "countryAlpha2Code": country_alpha2_code,
    "countryAlpha3Code": country_alpha3_code,
    "holidays": holidays_data,
    "updated_on": datetime.now().replace(microsecond=0).isoformat()
  }
  
  # Add countryRegions if provided
  if country_regions:
    result["countryRegions"] = country_regions
  
  return result







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
      
      # Compare entire holiday objects (full payload comparison)
      existing_holidays_list = existing_data.get('holidays', [])
      new_holidays_list = result.get('holidays', [])
      
      # Sort both lists by date for comparison
      def sort_by_date(holidays):
        return sorted(holidays, key=lambda h: h.get('date', ''))
      
      existing_sorted = sort_by_date(existing_holidays_list)
      new_sorted = sort_by_date(new_holidays_list)
      
      # Compare the full holiday objects
      if existing_sorted == new_sorted:
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

