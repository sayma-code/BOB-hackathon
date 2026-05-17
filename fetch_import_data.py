"""
Fetch Bangladesh Import Data from World Bank API
Collects import data by product categories from 2000 onwards
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import wbgapi as wb
import pandas as pd
import numpy as np
from datetime import datetime

def fetch_import_data():
    """
    Fetch Bangladesh import data from World Bank API
    Focus on merchandise imports by product category
    """
    
    print("Fetching Bangladesh import data from World Bank API...")
    print("=" * 80)
    
    # Country code for Bangladesh
    country = 'BGD'
    
    # Time range from 2000 to latest available
    time_range = range(2000, datetime.now().year + 1)
    
    # Import-related indicators from World Bank
    import_indicators = {
        # Total imports
        'TM.VAL.MRCH.CD.WT': 'Total Merchandise Imports (current US$)',
        'TM.VAL.MRCH.WL.CD': 'Total Merchandise Imports (current US$) - Alternative',
        'NE.IMP.GNFS.CD': 'Imports of goods and services (current US$)',
        'NE.IMP.GNFS.KD': 'Imports of goods and services (constant 2015 US$)',
        
        # Import by product categories
        'TM.VAL.FOOD.ZS.UN': 'Food imports (% of merchandise imports)',
        'TM.VAL.FUEL.ZS.UN': 'Fuel imports (% of merchandise imports)',
        'TM.VAL.MANF.ZS.UN': 'Manufactures imports (% of merchandise imports)',
        'TM.VAL.AGRI.ZS.UN': 'Agricultural raw materials imports (% of merchandise imports)',
        'TM.VAL.ORES.ZS.UN': 'Ores and metals imports (% of merchandise imports)',
        
        # Import values by category (current US$)
        'TM.VAL.FOOD.CD.WT': 'Food imports (current US$)',
        'TM.VAL.FUEL.CD.WT': 'Fuel imports (current US$)',
        'TM.VAL.MANF.CD.WT': 'Manufactures imports (current US$)',
        'TM.VAL.AGRI.CD.WT': 'Agricultural raw materials imports (current US$)',
        'TM.VAL.ORES.CD.WT': 'Ores and metals imports (current US$)',
        
        # Additional trade indicators
        'TM.VAL.MRCH.AL.ZS': 'Merchandise imports from economies in the Arab World (% of total)',
        'TM.VAL.MRCH.HI.ZS': 'Merchandise imports from high income economies (% of total)',
        'TM.VAL.MRCH.R1.ZS': 'Merchandise imports from developing economies in East Asia & Pacific (% of total)',
        'TM.VAL.MRCH.R2.ZS': 'Merchandise imports from developing economies in Europe & Central Asia (% of total)',
        'TM.VAL.MRCH.R3.ZS': 'Merchandise imports from developing economies in Latin America & the Caribbean (% of total)',
        'TM.VAL.MRCH.R4.ZS': 'Merchandise imports from developing economies in Middle East & North Africa (% of total)',
        'TM.VAL.MRCH.R5.ZS': 'Merchandise imports from developing economies in South Asia (% of total)',
        'TM.VAL.MRCH.R6.ZS': 'Merchandise imports from developing economies in Sub-Saharan Africa (% of total)',
        
        # Import structure
        'TM.VAL.MMTL.ZS.UN': 'Machinery and transport equipment imports (% of merchandise imports)',
        'TM.VAL.OTHR.ZS.UN': 'Other merchandise imports (% of merchandise imports)',
        
        # Trade balance related
        'NE.RSB.GNFS.CD': 'External balance on goods and services (current US$)',
        'BN.GSR.GNFS.CD': 'Trade in goods and services (current US$)',
    }
    
    all_data = []
    
    for indicator_code, indicator_name in import_indicators.items():
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
        output_file = 'data/raw/bangladesh_import_data.csv'
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
    output_file = 'data/processed/bangladesh_import_pivot.csv'
    pivot_df.to_csv(output_file)
    print(f"✓ Pivot table saved to: {output_file}")
    
    return pivot_df

def calculate_import_categories(df):
    """
    Calculate absolute values for import categories based on percentages and total imports
    """
    if df is None or df.empty:
        return None
    
    print("\nCalculating import category values...")
    
    # Create a pivot for easier calculation
    pivot = df.pivot_table(
        index='Year',
        columns='Indicator_Code',
        values='Value',
        aggfunc='first'
    )
    
    # Get total merchandise imports
    total_imports_col = None
    for col in ['TM.VAL.MRCH.CD.WT', 'TM.VAL.MRCH.WL.CD', 'NE.IMP.GNFS.CD']:
        if col in pivot.columns:
            total_imports_col = col
            break
    
    if total_imports_col is None:
        print("✗ Could not find total imports column")
        return None
    
    # Calculate absolute values from percentages
    category_data = []
    
    percentage_indicators = {
        'TM.VAL.FOOD.ZS.UN': 'Food',
        'TM.VAL.FUEL.ZS.UN': 'Fuel',
        'TM.VAL.MANF.ZS.UN': 'Manufactures',
        'TM.VAL.AGRI.ZS.UN': 'Agricultural Raw Materials',
        'TM.VAL.ORES.ZS.UN': 'Ores and Metals',
        'TM.VAL.MMTL.ZS.UN': 'Machinery and Transport Equipment',
        'TM.VAL.OTHR.ZS.UN': 'Other Merchandise',
    }
    
    for year in pivot.index:
        total_imports = pivot.loc[year, total_imports_col]
        
        if pd.notna(total_imports):
            for indicator_code, category_name in percentage_indicators.items():
                if indicator_code in pivot.columns:
                    percentage = pivot.loc[year, indicator_code]
                    if pd.notna(percentage):
                        value_usd = (percentage / 100) * total_imports
                        category_data.append({
                            'Year': year,
                            'Category': category_name,
                            'Value_USD': value_usd,
                            'Percentage': percentage,
                            'Total_Imports_USD': total_imports
                        })
    
    if category_data:
        category_df = pd.DataFrame(category_data)
        output_file = 'data/processed/bangladesh_import_categories.csv'
        category_df.to_csv(output_file, index=False)
        print(f"✓ Import categories saved to: {output_file}")
        return category_df
    
    return None

if __name__ == "__main__":
    # Fetch import data
    import_df = fetch_import_data()
    
    if import_df is not None:
        # Create pivot table
        pivot_df = create_pivot_table(import_df)
        
        # Calculate import categories
        categories_df = calculate_import_categories(import_df)
        
        print("\n" + "=" * 80)
        print("Import data collection completed successfully!")
        print("=" * 80)
    else:
        print("\nFailed to fetch import data")

# Made with Bob
