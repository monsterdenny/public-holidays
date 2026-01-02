from datetime import datetime
from lxml import html
import requests
import re

def output_format() -> str:
    return "%Y-%m-%d"

def getGovUkBankHolidays(url: str) -> list:
    """
    Fetches UK bank holidays from gov.uk website.
    Combines holidays from all regions (England and Wales, Scotland, Northern Ireland).
    
    Args:
        url: The gov.uk bank holidays URL (https://www.gov.uk/bank-holidays)
    
    Returns:
        List of holiday dictionaries with 'date' and 'holiday' fields
    """
    # Get HTML content
    response = requests.get(url)
    tree = html.fromstring(response.content)
    
    datas = []
    
    # Find all tables with bank holidays
    # Tables have headers with "Date", "Day of the week", "Bank holiday"
    tables = tree.xpath("//table[.//th[contains(text(), 'Date')] and .//th[contains(text(), 'Bank holiday')]]")
    
    for table in tables:
        # Find the region and year from the preceding heading
        # Look for headings like "Upcoming bank holidays in England and Wales 2026"
        year = None
        region = None
        
        # Try to find region and year in preceding headings (h2, h3, or strong tags)
        headings = table.xpath("./preceding::h2[1] | ./preceding::h3[1] | ./preceding::strong[1] | ./ancestor::*[self::h2 or self::h3 or self::strong][1]")
        
        for heading in headings:
            heading_text = heading.text_content()
            
            # Extract region from heading
            if not region:
                if "england and wales" in heading_text.lower():
                    region = "England and Wales"
                elif "scotland" in heading_text.lower():
                    region = "Scotland"
                elif "northern ireland" in heading_text.lower():
                    region = "Northern Ireland"
            
            # Extract 4-digit year from heading
            if not year:
                year_match = re.search(r'\b(20\d{2})\b', heading_text)
                if year_match:
                    year = int(year_match.group(1))
            
            if year and region:
                break
        
        # If no year found, try to find it from table caption or nearby text
        if not year:
            # Look for year in table's parent or sibling elements
            parent_text = table.xpath("./ancestor::*[position() < 5]//text()")
            for text in parent_text:
                year_match = re.search(r'\b(20\d{2})\b', text)
                if year_match:
                    year = int(year_match.group(1))
                    break
        
        # If still no year, use current year as fallback
        if not year:
            year = datetime.now().year
            print(f"Warning: Could not determine year for table, using {year}")
        
        # If no region found, default to "All" (shouldn't happen, but safety check)
        if not region:
            region = "All"
            print(f"Warning: Could not determine region for table, using 'All'")
        
        # Get all rows except header
        rows = table.xpath(".//tr[position() > 1]")
        
        for row in rows:
            # The date is in a th element, day and holiday are in td elements
            date_cell = row.xpath(".//th")
            data_cells = row.xpath(".//td")
            
            if len(date_cell) > 0 and len(data_cells) >= 2:
                # Extract date, day, and holiday name
                date_text = date_cell[0].text_content().strip()
                day_text = data_cells[0].text_content().strip() if len(data_cells) > 0 else ""
                holiday_name = data_cells[1].text_content().strip() if len(data_cells) > 1 else ""
                
                # Skip empty rows
                if not date_text or not holiday_name:
                    continue
                
                # Parse the date - format is like "3 April", "1 January", etc.
                try:
                    # Try parsing with the extracted year
                    date_str = f"{date_text} {year}"
                    date_obj = datetime.strptime(date_str, "%d %B %Y")
                    
                    # Format date and add to results
                    datas.append({
                        "date": date_obj.strftime(output_format()),
                        "holiday": holiday_name,
                        "region": region
                    })
                except ValueError:
                    # If parsing fails, try alternative formats or skip
                    print(f"Warning: Could not parse date '{date_text} {year}'")
                    continue
    
    # Group holidays by date and holiday name, combining regions
    # If same holiday appears in multiple regions, combine them
    holiday_map = {}
    for item in datas:
        key = (item["date"], item["holiday"])
        if key not in holiday_map:
            holiday_map[key] = {
                "date": item["date"],
                "holiday": item["holiday"],
                "region": [item["region"]]
            }
        else:
            # Add region if not already present
            if item["region"] not in holiday_map[key]["region"]:
                holiday_map[key]["region"].append(item["region"])
    
    # Convert to final format - keep regions as array
    unique_datas = []
    for key, value in holiday_map.items():
        # Sort regions and keep as array
        regions = sorted(value["region"])
        # If holiday appears in all 3 regions, use ["All"]
        # Otherwise, use the list of regions
        if len(regions) == 3:
            region_array = ["All"]
        else:
            region_array = regions
        
        unique_datas.append({
            "date": value["date"],
            "holiday": value["holiday"],
            "region": region_array
        })
    
    # Sort by date
    unique_datas.sort(key=lambda r: r["date"])
    
    print(f"Total records => {len(unique_datas)}\n")
    
    return unique_datas

