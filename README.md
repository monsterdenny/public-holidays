# Public Holidays Crawler

A Python-based repository for crawling and maintaining public holidays data from various countries. This repository contains scripts to fetch public holidays data and stores them in a standardised JSON format for easy reference and integration.

## 📁 Repository Structure

```
public-holidays/
├── src/              # Python scripts for crawling holidays
│   ├── sgp.py        # Singapore holidays
│   ├── fra.py        # France holidays
│   ├── chn.py        # China holidays
│   ├── myr.py        # Malaysia holidays
│   ├── vnm.py        # Vietnam holidays
│   └── functions.py  # Shared utility functions
├── data/             # Generated JSON files with holiday data
│   ├── sgp.json
│   ├── fra.json
│   └── ...
└── .github/
    └── workflows/
        └── crawl-holidays.yml  # Automated monthly crawler
```

## 🎯 Purpose

This repository helps you:
- **Crawl public holidays** from various countries using Python scripts
- **Access standardised holiday data** in JSON format from the `data/` folder
- **Contribute** by adding scripts for your country's public holidays

## 📊 Using the Data

All holiday data is stored in the `data/` folder as JSON files. Each file follows a standardised format:

```json
{
    "source": "https://example.com/holidays",
    "country": "Singapore",
    "countryAlpha2Code": "SG",
    "countryAlpha3Code": "SGP",
    "holidays": [
        {
            "date": "2024-01-01",
            "holiday": "New Year's Day"
        }
    ],
    "updated_on": "2024-01-01T00:00:00"
}
```

You can easily reference these JSON files in your projects or integrate them via API endpoints.

## 🤖 Automated Updates

This repository uses GitHub Actions to automatically crawl and update holiday data:
- **Schedule**: Runs on the 1st of every month at 00:00 UTC
- **Manual Trigger**: Can be triggered manually via GitHub Actions UI
- **Auto-commit**: Automatically commits updated JSON files to the repository

## 🚀 Running Scripts Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run a specific script:**
   ```bash
   cd src
   python sgp.py  # Example: Run Singapore holidays crawler
   ```

3. **Output:**
   The generated JSON files will be saved in the `data/` folder.

## 🤝 Contributing

We welcome contributions! If you'd like to add public holidays for your country:

1. **Fork the repository**

2. **Create a new Python script** in the `src/` folder following the naming convention:
   - Use the country's ISO 3166-1 alpha-3 code (e.g., `usa.py`, `gbr.py`, `jpn.py`)
   - Or use a descriptive name if the code is unclear

3. **Follow the existing script pattern:**
   - Crawl holiday data from a reliable source
   - Format the data consistently
   - Output to `../data/[country-code].json`
   - Include metadata: source URL, country name, country codes, and update timestamp

4. **Example script structure:**
   ```python
   from datetime import datetime
   import json
   
   # Your crawling logic here
   datas = []
   
   result = {
       "source": "https://your-source-url.com",
       "country": "Your Country",
       "countryAlpha2Code": "XX",
       "countryAlpha3Code": "XXX",
       "holidays": datas,
       "updated_on": datetime.now().replace(microsecond=0).isoformat()
   }
   
   with open('../data/xxx.json', 'w') as f:
       json.dump(result, f, indent=4)
   ```

5. **Test your script:**
   ```bash
   cd src
   python your-country.py
   ```

6. **Submit a Pull Request** with:
   - Your new Python script in `src/`
   - The generated JSON file in `data/`
   - A brief description of your data source

## 📝 Currently Supported Countries

- 🇸🇬 Singapore (`sgp.json`)
- 🇫🇷 France (`fra.json`)
- 🇨🇳 China (`chn.py`)
- 🇲🇾 Malaysia (`myr.py`)
- 🇻🇳 Vietnam (`vnm.py`)

*Note: Some scripts may be available but not yet generating data files. Feel free to help complete them!*

## 📄 Licence

This project is open source. Please check the licence file for more details.

## 🙏 Acknowledgments

Thank you to all contributors who help maintain and expand this public holidays database!

