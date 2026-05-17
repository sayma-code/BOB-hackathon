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
BASE_URL = "https://api.worldbank.org/v2/country/BGD/indicator"

# Detailed agricultural and income indicators
INDICATORS = {
    # Agricultural productivity and value added
    'NV.AGR.TOTL.CD': 'Agriculture, forestry, and fishing, value added (current US$)',
    'NV.AGR.TOTL.ZS': 'Agriculture, forestry, and fishing, value added (% of GDP)',
    'NV.AGR.TOTL.KD.ZG': 'Agriculture, forestry, and fishing, value added (annual % growth)',
    'AG.LND.AGRI.ZS': 'Agricultural land (% of land area)',
    'AG.LND.AGRI.K2': 'Agricultural land (sq. km)',
    'AG.PRD.CROP.XD': 'Crop production index (2014-2016 = 100)',
    'AG.PRD.FOOD.XD': 'Food production index (2014-2016 = 100)',
    'AG.PRD.LVSK.XD': 'Livestock production index (2014-2016 = 100)',
    
    # Agricultural employment and wages
    'SL.AGR.EMPL.MA.ZS': 'Employment in agriculture, male (% of male employment)',
    'SL.AGR.EMPL.FE.ZS': 'Employment in agriculture, female (% of female employment)',
    
    # Rural development and poverty
    'SI.POV.RUHC': 'Poverty headcount ratio at national poverty lines, rural (% of rural population)',
    'SI.POV.URHC': 'Poverty headcount ratio at national poverty lines, urban (% of urban population)',
    'SP.RUR.TOTL.ZS': 'Rural population (% of total population)',
    
    # Income distribution
    'SI.DST.FRST.10': 'Income share held by lowest 10%',
    'SI.DST.FRST.20': 'Income share held by lowest 20%',
    'SI.DST.02ND.20': 'Income share held by second 20%',
    'SI.DST.03RD.20': 'Income share held by third 20%',
    'SI.DST.04TH.20': 'Income share held by fourth 20%',
    'SI.DST.05TH.20': 'Income share held by highest 20%',
    'SI.DST.10TH.10': 'Income share held by highest 10%',
    
    # Household consumption and expenditure
    'NE.CON.PRVT.PC.KD': 'Household final consumption expenditure per capita (constant 2015 US$)',
    'NE.CON.PRVT.CD': 'Household final consumption expenditure (current US$)',
    
    # Additional economic indicators
    'NY.ADJ.NNTY.CD': 'Adjusted net national income (current US$)',
    'NY.GNP.PCAP.CD': 'GNI per capita, Atlas method (current US$)',
    'NY.GNP.PCAP.PP.CD': 'GNI per capita, PPP (current international $)',
    
    # Food security
    'SN.ITK.DEFC.ZS': 'Prevalence of undernourishment (% of population)',
    
    # Land productivity
    'AG.YLD.CREL.KG': 'Cereal yield (kg per hectare)',
    
    # Fertilizer and machinery
    'AG.CON.FERT.ZS': 'Fertilizer consumption (kilograms per hectare of arable land)',
    'AG.LND.TRAC.ZS': 'Agricultural machinery, tractors per 100 sq. km of arable land)',
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
    print("Fetching Detailed Agricultural Sector Data for Bangladesh")
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
        output_file = 'data/raw/agricultural_detailed_data.csv'
        df.to_csv(output_file, index=False)
        print()
        print(f"✓ Data saved to {output_file}")
        print(f"  Total records: {len(df)}")
        print(f"  Years covered: {df['year'].min()} - {df['year'].max()}")
        print(f"  Indicators: {df['indicator_code'].nunique()}")
        
        # Create a pivot table for easier analysis
        pivot_df = df.pivot(index='year', columns='indicator_name', values='value')
        pivot_output = 'data/processed/agricultural_detailed_pivot.csv'
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
