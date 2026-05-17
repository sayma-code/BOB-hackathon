import pandas as pd
import requests
import time
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# World Bank API base URL
BASE_URL = "https://api.worldbank.org/v2/country"

# Developed countries - USA and major European economies
COUNTRIES = {
    # North America
    'USA': 'United States',
    'CAN': 'Canada',
    
    # Western Europe
    'DEU': 'Germany',
    'FRA': 'France',
    'GBR': 'United Kingdom',
    'ITA': 'Italy',
    'ESP': 'Spain',
    'NLD': 'Netherlands',
    'BEL': 'Belgium',
    'AUT': 'Austria',
    'CHE': 'Switzerland',
    'SWE': 'Sweden',
    'DNK': 'Denmark',
    'NOR': 'Norway',
    'FIN': 'Finland',
    'IRL': 'Ireland',
    'PRT': 'Portugal',
    'GRC': 'Greece',
    
    # Eastern Europe
    'POL': 'Poland',
    'CZE': 'Czech Republic',
    'HUN': 'Hungary',
    'ROU': 'Romania',
    
    # For comparison - include Bangladesh
    'BGD': 'Bangladesh',
    
    # Other developed
    'AUS': 'Australia',
    'NZL': 'New Zealand',
    'JPN': 'Japan',
    'KOR': 'South Korea',
}

# Key indicators for comparison
INDICATORS = {
    # Debt indicators
    'DT.DOD.DECT.GN.ZS': 'External debt stocks (% of GNI)',
    'GC.DOD.TOTL.GD.ZS': 'Central government debt, total (% of GDP)',
    
    # Agricultural indicators
    'NV.AGR.TOTL.ZS': 'Agriculture, forestry, and fishing, value added (% of GDP)',
    'NV.AGR.TOTL.CD': 'Agriculture, forestry, and fishing, value added (current US$)',
    'SL.AGR.EMPL.ZS': 'Employment in agriculture (% of total employment)',
    
    # Economic indicators
    'NY.GDP.MKTP.CD': 'GDP (current US$)',
    'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
    'NY.GDP.MKTP.KD.ZG': 'GDP growth (annual %)',
    
    # Labor force
    'SL.TLF.TOTL.IN': 'Labor force, total',
    
    # Productivity
    'AG.PRD.CROP.XD': 'Crop production index (2014-2016 = 100)',
    'AG.YLD.CREL.KG': 'Cereal yield (kg per hectare)',
    
    # Additional metrics
    'AG.LND.AGRI.K2': 'Agricultural land (sq. km)',
    'AG.CON.FERT.ZS': 'Fertilizer consumption (kilograms per hectare of arable land)',
}

def fetch_multi_country_data(indicator_code, indicator_name):
    """Fetch data for multiple countries for a specific indicator"""
    country_codes = ';'.join(COUNTRIES.keys())
    url = f"{BASE_URL}/{country_codes}/indicator/{indicator_code}"
    params = {
        'format': 'json',
        'per_page': 1000,
        'date': '2020:2024'  # Focus on recent years
    }
    
    try:
        print(f"Fetching: {indicator_name}...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if len(data) > 1 and data[1]:
            records = []
            for item in data[1]:
                if item['value'] is not None:
                    records.append({
                        'country_code': item['countryiso3code'],
                        'country_name': COUNTRIES.get(item['countryiso3code'], item['country']['value']),
                        'year': int(item['date']),
                        'indicator_code': indicator_code,
                        'indicator_name': indicator_name,
                        'value': float(item['value'])
                    })
            return records
        else:
            print(f"  No data available for {indicator_name}")
            return []
            
    except Exception as e:
        print(f"  Error fetching {indicator_name}: {str(e)}")
        return []

def main():
    print("=" * 80)
    print("Fetching USA & European Countries Agricultural Data")
    print("=" * 80)
    print(f"\nCountries included: {len(COUNTRIES)}")
    
    # Group by region
    regions = {
        'North America': ['USA', 'CAN'],
        'Western Europe': ['DEU', 'FRA', 'GBR', 'ITA', 'ESP', 'NLD', 'BEL', 'AUT', 'CHE', 'SWE', 'DNK', 'NOR', 'FIN', 'IRL', 'PRT', 'GRC'],
        'Eastern Europe': ['POL', 'CZE', 'HUN', 'ROU'],
        'Asia-Pacific': ['AUS', 'NZL', 'JPN', 'KOR'],
        'South Asia': ['BGD']
    }
    
    for region, codes in regions.items():
        print(f"\n{region}:")
        for code in codes:
            print(f"  - {COUNTRIES[code]} ({code})")
    print()
    
    all_data = []
    
    # Fetch data for each indicator
    for indicator_code, indicator_name in INDICATORS.items():
        records = fetch_multi_country_data(indicator_code, indicator_name)
        all_data.extend(records)
        time.sleep(0.5)  # Be respectful to the API
    
    # Create DataFrame
    if all_data:
        df = pd.DataFrame(all_data)
        df = df.sort_values(['country_code', 'year', 'indicator_code'])
        
        # Save raw data
        output_file = 'data/raw/developed_countries_data.csv'
        df.to_csv(output_file, index=False)
        print()
        print(f"✓ Data saved to {output_file}")
        print(f"  Total records: {len(df)}")
        print(f"  Countries: {df['country_code'].nunique()}")
        print(f"  Years covered: {df['year'].min()} - {df['year'].max()}")
        print(f"  Indicators: {df['indicator_code'].nunique()}")
        
        # Create summary by country and year
        print()
        print("=" * 80)
        print("Data Availability Summary")
        print("=" * 80)
        
        summary = df.groupby(['country_name', 'year']).size().reset_index(name='indicators_count')
        pivot_summary = summary.pivot(index='country_name', columns='year', values='indicators_count')
        print(pivot_summary)
        
    else:
        print("No data was fetched. Please check your internet connection and try again.")

if __name__ == "__main__":
    main()

# Made with Bob
