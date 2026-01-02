from datetime import datetime

from lxml import html
from datetime import datetime, timedelta
import requests

def output_format() -> str:
    return "%Y-%m-%d"

def getHolidaysCalendarData(url: str) -> list:

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
        item["date"] = item["date"].strftime(output_format())
    
    return datas;


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