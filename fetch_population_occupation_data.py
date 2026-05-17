import pandas as pd
import requests
import time
import sys
from datetime import datetime

# Fix encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# World Bank API base URL
BASE_URL = "https://api.worldbank.org/v2/country/BGD/indicator"

# Define indicators for population, employment, and earnings
INDICATORS = {
    # Population indicators
    'SP.POP.TOTL': 'Total Population',
    'SP.POP.GROW': 'Population Growth (annual %)',
    'SP.URB.TOTL': 'Urban Population',
    'SP.RUR.TOTL': 'Rural Population',
    'SP.POP.0014.TO.ZS': 'Population ages 0-14 (% of total)',
    'SP.POP.1564.TO.ZS': 'Population ages 15-64 (% of total)',
    'SP.POP.65UP.TO.ZS': 'Population ages 65 and above (% of total)',
    
    # Labor force and employment
    'SL.TLF.TOTL.IN': 'Labor Force, Total',
    'SL.EMP.TOTL.SP.ZS': 'Employment to Population Ratio (%)',
    'SL.UEM.TOTL.ZS': 'Unemployment Rate (%)',
    
    # Employment by sector
    'SL.AGR.EMPL.ZS': 'Employment in Agriculture (% of total employment)',
    'SL.IND.EMPL.ZS': 'Employment in Industry (% of total employment)',
    'SL.SRV.EMPL.ZS': 'Employment in Services (% of total employment)',
    
    # Wage and earnings indicators
    'SL.EMP.WORK.ZS': 'Wage and Salaried Workers (% of total employment)',
    'SL.EMP.SELF.ZS': 'Self-employed (% of total employment)',
    'SL.EMP.VULN.ZS': 'Vulnerable Employment (% of total employment)',
    
    # Income and GDP per capita
    'NY.GDP.PCAP.CD': 'GDP per Capita (current US$)',
    'NY.GDP.PCAP.KD.ZG': 'GDP per Capita Growth (annual %)',
    'NY.ADJ.NNTY.PC.CD': 'Adjusted Net National Income per Capita (current US$)',
    
    # Additional economic indicators
    'SI.POV.NAHC': 'Poverty Headcount Ratio at National Poverty Lines (% of population)',
    'SI.POV.GINI': 'GINI Index (World Bank estimate)',
}

def fetch_indicator_data(indicator_code, indicator_name):
    """Fetch data for a specific indicator from World Bank API"""
    url = f"{BASE_URL}/{indicator_code}"
    params = {
        'format': 'json',
        'per_page': 100,
        'date': '2000:2024'
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
    print("Fetching Population, Occupation, and Earnings Data for Bangladesh")
    print("=" * 80)
    print()
    
    all_data = []
    
    # Fetch data for each indicator
    for indicator_code, indicator_name in INDICATORS.items():
        records = fetch_indicator_data(indicator_code, indicator_name)
        all_data.extend(records)
        time.sleep(0.5)  # Be respectful to the API
    
    # Create DataFrame
    if all_data:
        df = pd.DataFrame(all_data)
        df = df.sort_values(['year', 'indicator_code'])
        
        # Save raw data
        output_file = 'data/raw/population_occupation_earnings_data.csv'
        df.to_csv(output_file, index=False)
        print()
        print(f"✓ Data saved to {output_file}")
        print(f"  Total records: {len(df)}")
        print(f"  Years covered: {df['year'].min()} - {df['year'].max()}")
        print(f"  Indicators: {df['indicator_code'].nunique()}")
        
        # Create a pivot table for easier analysis
        pivot_df = df.pivot(index='year', columns='indicator_name', values='value')
        pivot_output = 'data/processed/population_occupation_earnings_pivot.csv'
        pivot_df.to_csv(pivot_output)
        print(f"✓ Pivot table saved to {pivot_output}")
        
        # Display summary statistics
        print()
        print("=" * 80)
        print("Data Summary")
        print("=" * 80)
        print(pivot_df.describe())
        
    else:
        print("No data was fetched. Please check your internet connection and try again.")

if __name__ == "__main__":
    main()

# Made with Bob
