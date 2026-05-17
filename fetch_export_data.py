"""
Fetch Bangladesh Export Data from World Bank API
Collects export data by product categories from 2000 onwards
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import wbgapi as wb
import pandas as pd
import numpy as np
from datetime import datetime

def fetch_export_data():
    """
    Fetch Bangladesh export data from World Bank API
    Focus on merchandise exports by product category
    """
    
    print("Fetching Bangladesh export data from World Bank API...")
    print("=" * 80)
    
    # Country code for Bangladesh
    country = 'BGD'
    
    # Time range from 2000 to latest available
    time_range = range(2000, datetime.now().year + 1)
    
    # Export-related indicators from World Bank
    export_indicators = {
        # Total exports
        'TX.VAL.MRCH.CD.WT': 'Total Merchandise Exports (current US$)',
        'TX.VAL.MRCH.WL.CD': 'Total Merchandise Exports (current US$) - Alternative',
        'NE.EXP.GNFS.CD': 'Exports of goods and services (current US$)',
        'NE.EXP.GNFS.KD': 'Exports of goods and services (constant 2015 US$)',
        
        # Export by product categories (percentages)
        'TX.VAL.FOOD.ZS.UN': 'Food exports (% of merchandise exports)',
        'TX.VAL.FUEL.ZS.UN': 'Fuel exports (% of merchandise exports)',
        'TX.VAL.MANF.ZS.UN': 'Manufactures exports (% of merchandise exports)',
        'TX.VAL.AGRI.ZS.UN': 'Agricultural raw materials exports (% of merchandise exports)',
        'TX.VAL.ORES.ZS.UN': 'Ores and metals exports (% of merchandise exports)',
        
        # Export values by category (current US$)
        'TX.VAL.FOOD.CD.WT': 'Food exports (current US$)',
        'TX.VAL.FUEL.CD.WT': 'Fuel exports (current US$)',
        'TX.VAL.MANF.CD.WT': 'Manufactures exports (current US$)',
        'TX.VAL.AGRI.CD.WT': 'Agricultural raw materials exports (current US$)',
        'TX.VAL.ORES.CD.WT': 'Ores and metals exports (current US$)',
        
        # Export destinations
        'TX.VAL.MRCH.AL.ZS': 'Merchandise exports to economies in the Arab World (% of total)',
        'TX.VAL.MRCH.HI.ZS': 'Merchandise exports to high income economies (% of total)',
        'TX.VAL.MRCH.R1.ZS': 'Merchandise exports to developing economies in East Asia & Pacific (% of total)',
        'TX.VAL.MRCH.R2.ZS': 'Merchandise exports to developing economies in Europe & Central Asia (% of total)',
        'TX.VAL.MRCH.R3.ZS': 'Merchandise exports to developing economies in Latin America & the Caribbean (% of total)',
        'TX.VAL.MRCH.R4.ZS': 'Merchandise exports to developing economies in Middle East & North Africa (% of total)',
        'TX.VAL.MRCH.R5.ZS': 'Merchandise exports to developing economies in South Asia (% of total)',
        'TX.VAL.MRCH.R6.ZS': 'Merchandise exports to developing economies in Sub-Saharan Africa (% of total)',
        
        # Export structure
        'TX.VAL.MMTL.ZS.UN': 'Machinery and transport equipment exports (% of merchandise exports)',
        'TX.VAL.OTHR.ZS.UN': 'Other merchandise exports (% of merchandise exports)',
        'TX.VAL.TECH.CD': 'High-technology exports (current US$)',
        'TX.VAL.TECH.MF.ZS': 'High-technology exports (% of manufactured exports)',
        
        # Textiles (important for Bangladesh)
        'TX.VAL.TEXT.CD.WT': 'Textile exports (current US$)',
        'TX.VAL.TRAN.ZS.WT': 'Transport services (% of service exports)',
    }
    
    all_data = []
    
    for indicator_code, indicator_name in export_indicators.items():
        try:
            print(f"\nFetching: {indicator_name}")
            print(f"Indicator code: {indicator_code}")
            
            # Fetch data
            data = wb.data.DataFrame(
                indicator_code,
                country,
                time=time_range,
                skipBlanks=True,
                columns='series'
            )
            
            if not data.empty:
                # Reset index to get year as a column
                data = data.reset_index()
                data.columns = ['Year', 'Value']
                data['Indicator'] = indicator_name
                data['Indicator_Code'] = indicator_code
                data['Country'] = 'Bangladesh'
                
                all_data.append(data)
                print(f"✓ Successfully fetched {len(data)} records")
            else:
                print(f"✗ No data available")
                
        except Exception as e:
            print(f"✗ Error fetching {indicator_code}: {str(e)}")
            continue
    
    if all_data:
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Sort by year and indicator
        combined_df = combined_df.sort_values(['Year', 'Indicator'])
        
        # Save raw data
        output_file = 'data/raw/bangladesh_export_data.csv'
        combined_df.to_csv(output_file, index=False)
        print(f"\n{'=' * 80}")
        print(f"✓ Data saved to: {output_file}")
        print(f"Total records: {len(combined_df)}")
        print(f"Years covered: {combined_df['Year'].min()} - {combined_df['Year'].max()}")
        print(f"Indicators collected: {combined_df['Indicator'].nunique()}")
        
        return combined_df
    else:
        print("\n✗ No data was successfully fetched")
        return None

def create_pivot_table(df):
    """
    Create a pivot table with years as rows and indicators as columns
    """
    if df is None or df.empty:
        return None
    
    print("\nCreating pivot table...")
    
    # Create pivot table
    pivot_df = df.pivot_table(
        index='Year',
        columns='Indicator',
        values='Value',
        aggfunc='first'
    )
    
    # Sort by year
    pivot_df = pivot_df.sort_index()
    
    # Save pivot table
    output_file = 'data/processed/bangladesh_export_pivot.csv'
    pivot_df.to_csv(output_file)
    print(f"✓ Pivot table saved to: {output_file}")
    
    return pivot_df

def calculate_export_categories(df):
    """
    Calculate absolute values for export categories based on percentages and total exports
    """
    if df is None or df.empty:
        return None
    
    print("\nCalculating export category values...")
    
    # Create a pivot for easier calculation
    pivot = df.pivot_table(
        index='Year',
        columns='Indicator_Code',
        values='Value',
        aggfunc='first'
    )
    
    # Get total merchandise exports
    total_exports_col = None
    for col in ['TX.VAL.MRCH.CD.WT', 'TX.VAL.MRCH.WL.CD', 'NE.EXP.GNFS.CD']:
        if col in pivot.columns:
            total_exports_col = col
            break
    
    if total_exports_col is None:
        print("✗ Could not find total exports column")
        return None
    
    # Calculate absolute values from percentages
    category_data = []
    
    percentage_indicators = {
        'TX.VAL.FOOD.ZS.UN': 'Food',
        'TX.VAL.FUEL.ZS.UN': 'Fuel',
        'TX.VAL.MANF.ZS.UN': 'Manufactures',
        'TX.VAL.AGRI.ZS.UN': 'Agricultural Raw Materials',
        'TX.VAL.ORES.ZS.UN': 'Ores and Metals',
        'TX.VAL.MMTL.ZS.UN': 'Machinery and Transport Equipment',
        'TX.VAL.OTHR.ZS.UN': 'Other Merchandise',
    }
    
    for year in pivot.index:
        total_exports = pivot.loc[year, total_exports_col]
        
        if pd.notna(total_exports):
            for indicator_code, category_name in percentage_indicators.items():
                if indicator_code in pivot.columns:
                    percentage = pivot.loc[year, indicator_code]
                    if pd.notna(percentage):
                        value_usd = (percentage / 100) * total_exports
                        category_data.append({
                            'Year': year,
                            'Category': category_name,
                            'Value_USD': value_usd,
                            'Percentage': percentage,
                            'Total_Exports_USD': total_exports
                        })
    
    if category_data:
        category_df = pd.DataFrame(category_data)
        output_file = 'data/processed/bangladesh_export_categories.csv'
        category_df.to_csv(output_file, index=False)
        print(f"✓ Export categories saved to: {output_file}")
        return category_df
    
    return None

if __name__ == "__main__":
    # Fetch export data
    export_df = fetch_export_data()
    
    if export_df is not None:
        # Create pivot table
        pivot_df = create_pivot_table(export_df)
        
        # Calculate export categories
        categories_df = calculate_export_categories(export_df)
        
        print("\n" + "=" * 80)
        print("Export data collection completed successfully!")
        print("=" * 80)
    else:
        print("\nFailed to fetch export data")

# Made with Bob
