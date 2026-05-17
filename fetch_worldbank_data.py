"""
Bangladesh External Debt Data Collection - World Bank API
This script fetches external debt and economic indicators from the World Bank API
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time
import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class WorldBankDataFetcher:
    """Fetch data from World Bank API for Bangladesh"""
    
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"
        self.country_code = "BGD"  # Bangladesh
        self.start_year = 2000
        self.end_year = 2024
        
        # External Debt Indicators
        self.debt_indicators = {
            'DT.DOD.DECT.CD': 'External debt stocks, total (current US$)',
            'DT.DOD.MLAT.CD': 'Multilateral debt (IMF, World Bank, ADB)',
            'DT.DOD.BLAT.CD': 'Bilateral debt (government-to-government)',
            'DT.DOD.PRVT.CD': 'Private creditors debt',
            'DT.AMT.DLXF.CD': 'Principal repayments on external debt',
            'DT.INT.DLXF.CD': 'Interest payments on external debt',
            'DT.TDS.DECT.CD': 'Total debt service on external debt',
            'DT.DOD.DPPG.CD': 'Public and publicly guaranteed debt',
        }
        
        # Economic Indicators
        self.economic_indicators = {
            'NY.GDP.MKTP.CD': 'GDP (current US$)',
            'NY.GDP.MKTP.KD.ZG': 'GDP growth (annual %)',
            'NE.EXP.GNFS.CD': 'Exports of goods and services (current US$)',
            'NE.IMP.GNFS.CD': 'Imports of goods and services (current US$)',
            'FI.RES.TOTL.CD': 'Total reserves (includes gold, current US$)',
            'PA.NUS.FCRF': 'Official exchange rate (LCU per US$, period average)',
            'GC.REV.XGRT.GD.ZS': 'Revenue, excluding grants (% of GDP)',
            'GC.XPN.TOTL.GD.ZS': 'Expense (% of GDP)',
            'BN.CAB.XOKA.CD': 'Current account balance (BoP, current US$)',
        }
        
        # Create data directory if it doesn't exist
        os.makedirs('data/raw', exist_ok=True)
        os.makedirs('data/processed', exist_ok=True)
    
    def fetch_indicator_data(self, indicator_code, indicator_name):
        """
        Fetch data for a specific indicator
        
        Args:
            indicator_code: World Bank indicator code
            indicator_name: Human-readable name for the indicator
            
        Returns:
            DataFrame with year and value columns
        """
        url = f"{self.base_url}/country/{self.country_code}/indicator/{indicator_code}"
        params = {
            'date': f'{self.start_year}:{self.end_year}',
            'format': 'json',
            'per_page': 500
        }
        
        try:
            print(f"Fetching: {indicator_name}...")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # World Bank API returns [metadata, data]
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
                
                df = pd.DataFrame(records)
                print(f"  [OK] Retrieved {len(df)} data points")
                return df
            else:
                print(f"  [WARN] No data available for {indicator_name}")
                return pd.DataFrame()
                
        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] Error fetching {indicator_name}: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"  [ERROR] Unexpected error for {indicator_name}: {e}")
            return pd.DataFrame()
    
    def fetch_all_debt_indicators(self):
        """Fetch all external debt indicators"""
        print("\n" + "="*60)
        print("FETCHING EXTERNAL DEBT INDICATORS")
        print("="*60)
        
        all_data = []
        for code, name in self.debt_indicators.items():
            df = self.fetch_indicator_data(code, name)
            if not df.empty:
                all_data.append(df)
            time.sleep(0.5)  # Rate limiting
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df = combined_df.sort_values(['year', 'indicator_code'])
            
            # Save raw data
            filename = 'data/raw/worldbank_debt_data.csv'
            combined_df.to_csv(filename, index=False)
            print(f"\n[OK] Saved debt data to {filename}")
            
            return combined_df
        else:
            print("\n[ERROR] No debt data retrieved")
            return pd.DataFrame()
    
    def fetch_all_economic_indicators(self):
        """Fetch all economic indicators"""
        print("\n" + "="*60)
        print("FETCHING ECONOMIC INDICATORS")
        print("="*60)
        
        all_data = []
        for code, name in self.economic_indicators.items():
            df = self.fetch_indicator_data(code, name)
            if not df.empty:
                all_data.append(df)
            time.sleep(0.5)  # Rate limiting
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df = combined_df.sort_values(['year', 'indicator_code'])
            
            # Save raw data
            filename = 'data/raw/worldbank_economic_data.csv'
            combined_df.to_csv(filename, index=False)
            print(f"\n[OK] Saved economic data to {filename}")
            
            return combined_df
        else:
            print("\n[ERROR] No economic data retrieved")
            return pd.DataFrame()
    
    def create_wide_format_dataset(self, debt_df, economic_df):
        """
        Create a wide-format dataset with years as rows and indicators as columns
        
        Args:
            debt_df: DataFrame with debt indicators
            economic_df: DataFrame with economic indicators
            
        Returns:
            Wide-format DataFrame
        """
        print("\n" + "="*60)
        print("CREATING CONSOLIDATED DATASET")
        print("="*60)
        
        # Combine both datasets
        all_data = pd.concat([debt_df, economic_df], ignore_index=True)
        
        if all_data.empty:
            print("[ERROR] No data to consolidate")
            return pd.DataFrame()
        
        # Pivot to wide format
        wide_df = all_data.pivot(
            index='year',
            columns='indicator_name',
            values='value'
        ).reset_index()
        
        # Sort by year
        wide_df = wide_df.sort_values('year')
        
        # Calculate derived metrics
        if 'External debt stocks, total (current US$)' in wide_df.columns and 'GDP (current US$)' in wide_df.columns:
            wide_df['Debt-to-GDP Ratio (%)'] = (
                wide_df['External debt stocks, total (current US$)'] / 
                wide_df['GDP (current US$)'] * 100
            )
        
        if 'Total debt service on external debt' in wide_df.columns and 'Exports of goods and services (current US$)' in wide_df.columns:
            wide_df['Debt Service Ratio (%)'] = (
                wide_df['Total debt service on external debt'] / 
                wide_df['Exports of goods and services (current US$)'] * 100
            )
        
        if 'Imports of goods and services (current US$)' in wide_df.columns and 'Exports of goods and services (current US$)' in wide_df.columns:
            wide_df['Trade Balance (current US$)'] = (
                wide_df['Exports of goods and services (current US$)'] - 
                wide_df['Imports of goods and services (current US$)']
            )
        
        # Save consolidated dataset
        filename = 'data/processed/bangladesh_debt_consolidated.csv'
        wide_df.to_csv(filename, index=False)
        print(f"[OK] Saved consolidated dataset to {filename}")
        print(f"  - Years covered: {wide_df['year'].min()} to {wide_df['year'].max()}")
        print(f"  - Total indicators: {len(wide_df.columns) - 1}")
        
        return wide_df
    
    def generate_summary_statistics(self, df):
        """Generate summary statistics for the dataset"""
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        if df.empty:
            print("No data available for summary")
            return
        
        # Key metrics
        key_metrics = [
            'External debt stocks, total (current US$)',
            'GDP (current US$)',
            'Debt-to-GDP Ratio (%)',
            'Total debt service on external debt',
            'Debt Service Ratio (%)'
        ]
        
        summary_data = []
        for metric in key_metrics:
            if metric in df.columns:
                values = df[metric].dropna()
                if not values.empty:
                    summary_data.append({
                        'Indicator': metric,
                        'Latest Year': df.loc[values.index[-1], 'year'],
                        'Latest Value': f"{values.iloc[-1]:,.2f}",
                        'Min': f"{values.min():,.2f}",
                        'Max': f"{values.max():,.2f}",
                        'Mean': f"{values.mean():,.2f}",
                        'Growth (%)': f"{((values.iloc[-1] / values.iloc[0] - 1) * 100):,.2f}" if len(values) > 1 else "N/A"
                    })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            print(summary_df.to_string(index=False))
            
            # Save summary
            summary_df.to_csv('data/processed/summary_statistics.csv', index=False)
            print(f"\n[OK] Saved summary statistics to data/processed/summary_statistics.csv")
        
    def run_full_collection(self):
        """Run the complete data collection process"""
        print("\n" + "="*60)
        print("BANGLADESH EXTERNAL DEBT DATA COLLECTION")
        print(f"Time Period: {self.start_year} - {self.end_year}")
        print("="*60)
        
        start_time = time.time()
        
        # Fetch debt indicators
        debt_df = self.fetch_all_debt_indicators()
        
        # Fetch economic indicators
        economic_df = self.fetch_all_economic_indicators()
        
        # Create consolidated dataset
        consolidated_df = self.create_wide_format_dataset(debt_df, economic_df)
        
        # Generate summary statistics
        self.generate_summary_statistics(consolidated_df)
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*60)
        print(f"DATA COLLECTION COMPLETED in {elapsed_time:.2f} seconds")
        print("="*60)
        print("\nFiles created:")
        print("  1. data/raw/worldbank_debt_data.csv")
        print("  2. data/raw/worldbank_economic_data.csv")
        print("  3. data/processed/bangladesh_debt_consolidated.csv")
        print("  4. data/processed/summary_statistics.csv")
        print("\nNext steps:")
        print("  - Review the consolidated dataset")
        print("  - Run exploratory data analysis")
        print("  - Create visualizations")
        print("="*60)

def main():
    """Main execution function"""
    fetcher = WorldBankDataFetcher()
    fetcher.run_full_collection()

if __name__ == "__main__":
    main()

# Made with Bob
