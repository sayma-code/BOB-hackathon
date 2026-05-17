"""
Foreign Employment Potential Analysis
Analyzes unemployment and potential for sending workers abroad for remittance revenue
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
from pathlib import Path

def load_population_data():
    """Load population and employment data"""
    df = pd.read_csv('data/raw/population_occupation_earnings_data.csv')
    
    # Pivot to get years as columns
    pivot = df.pivot(index='year', columns='indicator_code', values='value')
    pivot = pivot.reset_index()
    
    return pivot

def analyze_unemployment_and_labor_force(df):
    """Analyze unemployment trends and labor force"""
    
    print("="*80)
    print("UNEMPLOYMENT & FOREIGN EMPLOYMENT POTENTIAL ANALYSIS")
    print("="*80)
    
    # Get latest data (2024)
    latest = df[df['year'] == 2024].iloc[0]
    
    total_pop = latest['SP.POP.TOTL']
    labor_force = latest['SL.TLF.TOTL.IN']
    unemployment_rate = latest['SL.UEM.TOTL.ZS']
    employment_ratio = latest['SL.EMP.TOTL.SP.ZS']
    working_age_pct = latest['SP.POP.1564.TO.ZS']
    
    # Calculate key metrics
    working_age_pop = total_pop * (working_age_pct / 100)
    employed = labor_force * (1 - unemployment_rate / 100)
    unemployed = labor_force * (unemployment_rate / 100)
    not_in_labor_force = working_age_pop - labor_force
    
    print(f"\n{'='*80}")
    print("2024 LABOR MARKET SITUATION")
    print(f"{'='*80}")
    print(f"\nTotal Population: {total_pop/1e6:.2f} million")
    print(f"Working Age Population (15-64): {working_age_pop/1e6:.2f} million ({working_age_pct:.1f}%)")
    print(f"\nLabor Force: {labor_force/1e6:.2f} million")
    print(f"Employed: {employed/1e6:.2f} million")
    print(f"Unemployed: {unemployed/1e6:.2f} million ({unemployment_rate:.2f}%)")
    print(f"Not in Labor Force: {not_in_labor_force/1e6:.2f} million")
    
    # Historical trend
    print(f"\n{'-'*80}")
    print("UNEMPLOYMENT TREND (2000-2024)")
    print(f"{'-'*80}")
    
    years_to_show = [2000, 2005, 2010, 2015, 2020, 2024]
    for year in years_to_show:
        year_data = df[df['year'] == year].iloc[0]
        unemp_rate = year_data['SL.UEM.TOTL.ZS']
        lf = year_data['SL.TLF.TOTL.IN']
        unemp_count = lf * (unemp_rate / 100)
        print(f"{year}: {unemp_rate:.2f}% ({unemp_count/1e6:.2f}M unemployed)")
    
    return {
        'total_pop': total_pop,
        'working_age_pop': working_age_pop,
        'labor_force': labor_force,
        'employed': employed,
        'unemployed': unemployed,
        'not_in_labor_force': not_in_labor_force,
        'unemployment_rate': unemployment_rate
    }

def analyze_foreign_employment_potential(metrics):
    """Analyze potential for foreign employment"""
    
    print(f"\n{'='*80}")
    print("FOREIGN EMPLOYMENT POTENTIAL")
    print(f"{'='*80}")
    
    unemployed = metrics['unemployed']
    not_in_lf = metrics['not_in_labor_force']
    
    # Current remittance data (approximate from World Bank)
    current_migrants_abroad = 7.5e6  # ~7.5 million Bangladeshis abroad
    current_remittance = 21.5e9  # $21.5 billion in 2023
    avg_remittance_per_worker = current_remittance / current_migrants_abroad
    
    print(f"\nCURRENT SITUATION:")
    print(f"Bangladeshis Working Abroad: {current_migrants_abroad/1e6:.2f} million")
    print(f"Annual Remittance: ${current_remittance/1e9:.2f} billion")
    print(f"Average Remittance per Worker: ${avg_remittance_per_worker:,.0f}/year")
    
    # Potential pools for foreign employment
    print(f"\n{'-'*80}")
    print("POTENTIAL WORKER POOLS:")
    print(f"{'-'*80}")
    
    # Pool 1: Currently unemployed
    pool1_size = unemployed
    pool1_eligible = pool1_size * 0.60  # 60% eligible (age, health, skills)
    print(f"\n1. Currently Unemployed:")
    print(f"   Total: {pool1_size/1e6:.2f} million")
    print(f"   Eligible for Foreign Work: {pool1_eligible/1e6:.2f} million (60%)")
    
    # Pool 2: Underemployed in agriculture
    agri_employment_pct = 44.74  # 2024 data
    total_employed = metrics['employed']
    agri_workers = total_employed * (agri_employment_pct / 100)
    underemployed_agri = agri_workers * 0.30  # 30% underemployed
    pool2_eligible = underemployed_agri * 0.50  # 50% willing to go abroad
    print(f"\n2. Underemployed in Agriculture:")
    print(f"   Agricultural Workers: {agri_workers/1e6:.2f} million")
    print(f"   Underemployed (30%): {underemployed_agri/1e6:.2f} million")
    print(f"   Eligible & Willing: {pool2_eligible/1e6:.2f} million (50%)")
    
    # Pool 3: Youth not in labor force
    youth_not_in_lf = not_in_lf * 0.40  # 40% are youth
    pool3_eligible = youth_not_in_lf * 0.25  # 25% interested in foreign work
    print(f"\n3. Youth Not in Labor Force:")
    print(f"   Total Not in Labor Force: {not_in_lf/1e6:.2f} million")
    print(f"   Youth (40%): {youth_not_in_lf/1e6:.2f} million")
    print(f"   Interested in Foreign Work: {pool3_eligible/1e6:.2f} million (25%)")
    
    # Total potential
    total_potential = pool1_eligible + pool2_eligible + pool3_eligible
    
    print(f"\n{'='*80}")
    print(f"TOTAL POTENTIAL: {total_potential/1e6:.2f} million workers")
    print(f"{'='*80}")
    
    return {
        'current_migrants': current_migrants_abroad,
        'current_remittance': current_remittance,
        'avg_remittance': avg_remittance_per_worker,
        'pool1': pool1_eligible,
        'pool2': pool2_eligible,
        'pool3': pool3_eligible,
        'total_potential': total_potential
    }

def analyze_destination_countries():
    """Analyze destination countries and opportunities"""
    
    print(f"\n{'='*80}")
    print("DESTINATION COUNTRIES & OPPORTUNITIES")
    print(f"{'='*80}")
    
    destinations = [
        {
            'Region': 'Middle East',
            'Countries': 'Saudi Arabia, UAE, Qatar, Kuwait, Oman, Bahrain',
            'Current_Workers_Million': 4.5,
            'Potential_Additional_Million': 2.0,
            'Avg_Salary_USD': 400,
            'Job_Types': 'Construction, domestic work, services, retail',
            'Skill_Level': 'Low to Medium',
            'Language': 'Arabic (basic), English',
            'Demand': 'Very High'
        },
        {
            'Region': 'Southeast Asia',
            'Countries': 'Malaysia, Singapore, Brunei',
            'Current_Workers_Million': 1.2,
            'Potential_Additional_Million': 0.8,
            'Avg_Salary_USD': 500,
            'Job_Types': 'Manufacturing, construction, services',
            'Skill_Level': 'Low to Medium',
            'Language': 'English, Malay',
            'Demand': 'High'
        },
        {
            'Region': 'Europe',
            'Countries': 'UK, Italy, Greece, Spain, Germany',
            'Current_Workers_Million': 0.8,
            'Potential_Additional_Million': 1.5,
            'Avg_Salary_USD': 1500,
            'Job_Types': 'Healthcare, IT, hospitality, agriculture',
            'Skill_Level': 'Medium to High',
            'Language': 'English, local languages',
            'Demand': 'High (aging population)'
        },
        {
            'Region': 'North America',
            'Countries': 'USA, Canada',
            'Current_Workers_Million': 0.5,
            'Potential_Additional_Million': 1.0,
            'Avg_Salary_USD': 2500,
            'Job_Types': 'IT, healthcare, engineering, services',
            'Skill_Level': 'High',
            'Language': 'English',
            'Demand': 'High (skilled workers)'
        },
        {
            'Region': 'East Asia',
            'Countries': 'Japan, South Korea',
            'Current_Workers_Million': 0.3,
            'Potential_Additional_Million': 0.5,
            'Avg_Salary_USD': 1800,
            'Job_Types': 'Manufacturing, caregiving, agriculture',
            'Skill_Level': 'Medium',
            'Language': 'Japanese, Korean',
            'Demand': 'Very High (aging population)'
        },
        {
            'Region': 'Australia & NZ',
            'Countries': 'Australia, New Zealand',
            'Current_Workers_Million': 0.2,
            'Potential_Additional_Million': 0.3,
            'Avg_Salary_USD': 2000,
            'Job_Types': 'Agriculture, healthcare, IT, trades',
            'Skill_Level': 'Medium to High',
            'Language': 'English',
            'Demand': 'High'
        }
    ]
    
    df_dest = pd.DataFrame(destinations)
    
    print(f"\n{'-'*80}")
    for _, row in df_dest.iterrows():
        print(f"\n{row['Region'].upper()}")
        print(f"Countries: {row['Countries']}")
        print(f"Current Workers: {row['Current_Workers_Million']:.1f}M")
        print(f"Additional Potential: {row['Potential_Additional_Million']:.1f}M")
        print(f"Average Salary: ${row['Avg_Salary_USD']}/month")
        print(f"Job Types: {row['Job_Types']}")
        print(f"Skill Level: {row['Skill_Level']}")
        print(f"Demand: {row['Demand']}")
    
    total_current = df_dest['Current_Workers_Million'].sum()
    total_potential = df_dest['Potential_Additional_Million'].sum()
    
    print(f"\n{'='*80}")
    print(f"TOTAL CURRENT: {total_current:.1f} million workers")
    print(f"TOTAL ADDITIONAL POTENTIAL: {total_potential:.1f} million workers")
    print(f"{'='*80}")
    
    return df_dest

def calculate_revenue_potential(foreign_emp_data, destinations_df):
    """Calculate potential remittance revenue"""
    
    print(f"\n{'='*80}")
    print("REMITTANCE REVENUE POTENTIAL")
    print(f"{'='*80}")
    
    current_remittance = foreign_emp_data['current_remittance']
    avg_remittance = foreign_emp_data['avg_remittance']
    
    print(f"\nCurrent Annual Remittance: ${current_remittance/1e9:.2f} billion")
    print(f"Average per Worker: ${avg_remittance:,.0f}/year")
    
    # Calculate potential by destination
    print(f"\n{'-'*80}")
    print("POTENTIAL BY DESTINATION:")
    print(f"{'-'*80}")
    
    total_additional_revenue = 0
    
    for _, row in destinations_df.iterrows():
        additional_workers = row['Potential_Additional_Million'] * 1e6
        monthly_salary = row['Avg_Salary_USD']
        annual_salary = monthly_salary * 12
        # Assume 60% of salary is remitted
        annual_remittance_per_worker = annual_salary * 0.60
        total_additional = additional_workers * annual_remittance_per_worker
        
        print(f"\n{row['Region']}:")
        print(f"  Additional Workers: {row['Potential_Additional_Million']:.1f}M")
        print(f"  Avg Monthly Salary: ${monthly_salary}")
        print(f"  Remittance/Worker/Year: ${annual_remittance_per_worker:,.0f}")
        print(f"  Total Additional Revenue: ${total_additional/1e9:.2f}B")
        
        total_additional_revenue += total_additional
    
    # Scenarios
    print(f"\n{'='*80}")
    print("REVENUE SCENARIOS")
    print(f"{'='*80}")
    
    # Conservative: 30% of potential
    conservative_workers = destinations_df['Potential_Additional_Million'].sum() * 0.30
    conservative_revenue = conservative_workers * 1e6 * avg_remittance
    
    # Moderate: 50% of potential
    moderate_workers = destinations_df['Potential_Additional_Million'].sum() * 0.50
    moderate_revenue = moderate_workers * 1e6 * avg_remittance
    
    # Aggressive: 70% of potential
    aggressive_workers = destinations_df['Potential_Additional_Million'].sum() * 0.70
    aggressive_revenue = aggressive_workers * 1e6 * avg_remittance
    
    print(f"\n1. CONSERVATIVE (30% of potential over 10 years):")
    print(f"   Additional Workers: {conservative_workers:.2f}M")
    print(f"   Additional Revenue: ${conservative_revenue/1e9:.2f}B/year")
    print(f"   Total Remittance: ${(current_remittance + conservative_revenue)/1e9:.2f}B/year")
    print(f"   Increase: {(conservative_revenue/current_remittance)*100:.1f}%")
    
    print(f"\n2. MODERATE (50% of potential over 10 years):")
    print(f"   Additional Workers: {moderate_workers:.2f}M")
    print(f"   Additional Revenue: ${moderate_revenue/1e9:.2f}B/year")
    print(f"   Total Remittance: ${(current_remittance + moderate_revenue)/1e9:.2f}B/year")
    print(f"   Increase: {(moderate_revenue/current_remittance)*100:.1f}%")
    
    print(f"\n3. AGGRESSIVE (70% of potential over 10 years):")
    print(f"   Additional Workers: {aggressive_workers:.2f}M")
    print(f"   Additional Revenue: ${aggressive_revenue/1e9:.2f}B/year")
    print(f"   Total Remittance: ${(current_remittance + aggressive_revenue)/1e9:.2f}B/year")
    print(f"   Increase: {(aggressive_revenue/current_remittance)*100:.1f}%")
    
    return {
        'conservative': conservative_revenue,
        'moderate': moderate_revenue,
        'aggressive': aggressive_revenue
    }

def generate_report(labor_metrics, foreign_emp_data, destinations_df, revenue_scenarios):
    """Generate comprehensive report"""
    
    output_dir = Path('analysis/foreign_employment')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save destinations data
    destinations_df.to_csv(output_dir / 'destination_countries.csv', index=False)
    
    # Save summary
    summary = {
        'Metric': [
            'Total Population (2024)',
            'Working Age Population',
            'Labor Force',
            'Employed',
            'Unemployed',
            'Unemployment Rate',
            'Current Workers Abroad',
            'Current Remittance',
            'Potential Additional Workers',
            'Conservative Additional Revenue',
            'Moderate Additional Revenue',
            'Aggressive Additional Revenue'
        ],
        'Value': [
            f"{labor_metrics['total_pop']/1e6:.2f}M",
            f"{labor_metrics['working_age_pop']/1e6:.2f}M",
            f"{labor_metrics['labor_force']/1e6:.2f}M",
            f"{labor_metrics['employed']/1e6:.2f}M",
            f"{labor_metrics['unemployed']/1e6:.2f}M",
            f"{labor_metrics['unemployment_rate']:.2f}%",
            f"{foreign_emp_data['current_migrants']/1e6:.2f}M",
            f"${foreign_emp_data['current_remittance']/1e9:.2f}B",
            f"{foreign_emp_data['total_potential']/1e6:.2f}M",
            f"${revenue_scenarios['conservative']/1e9:.2f}B/year",
            f"${revenue_scenarios['moderate']/1e9:.2f}B/year",
            f"${revenue_scenarios['aggressive']/1e9:.2f}B/year"
        ]
    }
    
    pd.DataFrame(summary).to_csv(output_dir / 'foreign_employment_summary.csv', index=False)
    
    print(f"\n✓ Reports saved to {output_dir}")

if __name__ == "__main__":
    df = load_population_data()
    labor_metrics = analyze_unemployment_and_labor_force(df)
    foreign_emp_data = analyze_foreign_employment_potential(labor_metrics)
    destinations_df = analyze_destination_countries()
    revenue_scenarios = calculate_revenue_potential(foreign_emp_data, destinations_df)
    generate_report(labor_metrics, foreign_emp_data, destinations_df, revenue_scenarios)
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETED!")
    print(f"{'='*80}")

# Made with Bob
