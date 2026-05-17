"""
Bangladesh Fuel Resources Database
Comprehensive information about fuel sources, reserves, and operating companies
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path

def create_fuel_resources_database():
    """
    Create comprehensive database of Bangladesh's fuel resources
    """
    
    print("="*80)
    print("BANGLADESH FUEL RESOURCES DATABASE")
    print("="*80)
    
    # Natural Gas Fields
    natural_gas_fields = [
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Titas Gas Field',
            'Location': 'Brahmanbaria District',
            'Status': 'Active',
            'Operator': 'Petrobangla (Bangladesh Oil, Gas and Mineral Corporation)',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1968,
            'Production_Start': 1968,
            'Estimated_Reserves': 'Depleting - Major field',
            'Current_Production': 'Declining',
            'Notes': 'Largest gas field in Bangladesh, supplies to Dhaka and industrial areas'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Habiganj Gas Field',
            'Location': 'Habiganj District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1963,
            'Production_Start': 1963,
            'Estimated_Reserves': 'Moderate',
            'Current_Production': 'Active',
            'Notes': 'One of the oldest gas fields'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Bakhrabad Gas Field',
            'Location': 'Comilla District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1964,
            'Production_Start': 1964,
            'Estimated_Reserves': 'Moderate',
            'Current_Production': 'Active',
            'Notes': 'Supplies gas to Dhaka and Chittagong'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Rashidpur Gas Field',
            'Location': 'Narsingdi District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1960,
            'Production_Start': 1960,
            'Estimated_Reserves': 'Low - Depleting',
            'Current_Production': 'Declining',
            'Notes': 'One of the first gas fields discovered'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Kailashtila Gas Field',
            'Location': 'Sylhet District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1959,
            'Production_Start': 1960,
            'Estimated_Reserves': 'Moderate',
            'Current_Production': 'Active',
            'Notes': 'Supplies to Sylhet region'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Jalalabad Gas Field',
            'Location': 'Sylhet District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1989,
            'Production_Start': 1994,
            'Estimated_Reserves': 'Moderate',
            'Current_Production': 'Active',
            'Notes': 'Important field in Sylhet basin'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Bibiyana Gas Field',
            'Location': 'Habiganj District',
            'Status': 'Active',
            'Operator': 'Chevron Bangladesh',
            'Operator_Type': 'Foreign Private',
            'Country_of_Operator': 'United States',
            'Discovered_Year': 1998,
            'Production_Start': 2007,
            'Estimated_Reserves': '2.4 TCF (Trillion Cubic Feet)',
            'Current_Production': 'High - Largest producing field',
            'Notes': 'Largest gas field, produces ~50% of Bangladesh total gas production'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Jalalabad Gas Field (Chevron operated)',
            'Location': 'Sylhet District',
            'Status': 'Active',
            'Operator': 'Chevron Bangladesh',
            'Operator_Type': 'Foreign Private',
            'Country_of_Operator': 'United States',
            'Discovered_Year': 1989,
            'Production_Start': 1994,
            'Estimated_Reserves': 'Moderate',
            'Current_Production': 'Active',
            'Notes': 'Operated by Chevron under PSC'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Moulvibazar Gas Field',
            'Location': 'Moulvibazar District',
            'Status': 'Active',
            'Operator': 'Chevron Bangladesh',
            'Operator_Type': 'Foreign Private',
            'Country_of_Operator': 'United States',
            'Discovered_Year': 1997,
            'Production_Start': 2007,
            'Estimated_Reserves': 'Moderate',
            'Current_Production': 'Active',
            'Notes': 'Part of Chevron operations'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Sangu Gas Field',
            'Location': 'Bay of Bengal (Offshore)',
            'Status': 'Depleted',
            'Operator': 'Santos (formerly), now Petrobangla',
            'Operator_Type': 'Foreign Private (now State-Owned)',
            'Country_of_Operator': 'Australia (formerly)',
            'Discovered_Year': 1996,
            'Production_Start': 1998,
            'Estimated_Reserves': 'Depleted',
            'Current_Production': 'Ceased',
            'Notes': 'First offshore gas field, now depleted'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Bhola Gas Field',
            'Location': 'Bhola District (Offshore)',
            'Status': 'Under Development',
            'Operator': 'Gazprom (Russia)',
            'Operator_Type': 'Foreign State-Owned',
            'Country_of_Operator': 'Russia',
            'Discovered_Year': 2012,
            'Production_Start': 'Planned',
            'Estimated_Reserves': 'Significant',
            'Current_Production': 'Not yet producing',
            'Notes': 'Offshore field under development'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Shahbazpur Gas Field',
            'Location': 'Bhola District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1995,
            'Production_Start': 1998,
            'Estimated_Reserves': 'Moderate',
            'Current_Production': 'Active',
            'Notes': 'Supplies to southern region'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Semutang Gas Field',
            'Location': 'Sylhet District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1960,
            'Production_Start': 1960,
            'Estimated_Reserves': 'Low',
            'Current_Production': 'Declining',
            'Notes': 'Old field with declining production'
        },
        {
            'Resource_Type': 'Natural Gas',
            'Field_Name': 'Fenchuganj Gas Field',
            'Location': 'Sylhet District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1960,
            'Production_Start': 1960,
            'Estimated_Reserves': 'Low',
            'Current_Production': 'Declining',
            'Notes': 'Old field with declining production'
        }
    ]
    
    # Coal Fields
    coal_fields = [
        {
            'Resource_Type': 'Coal',
            'Field_Name': 'Barapukuria Coal Mine',
            'Location': 'Dinajpur District',
            'Status': 'Active',
            'Operator': 'Barapukuria Coal Mining Company Limited (BCMCL)',
            'Operator_Type': 'State-Owned (Chinese assistance)',
            'Country_of_Operator': 'Bangladesh (with China)',
            'Discovered_Year': 1985,
            'Production_Start': 2005,
            'Estimated_Reserves': '390 million tons',
            'Current_Production': 'Active - Underground mining',
            'Notes': 'Only operational coal mine in Bangladesh, Chinese assistance in development'
        },
        {
            'Resource_Type': 'Coal',
            'Field_Name': 'Phulbari Coal Field',
            'Location': 'Dinajpur District',
            'Status': 'Undeveloped - Controversial',
            'Operator': 'GCM Resources (UK) - License suspended',
            'Operator_Type': 'Foreign Private',
            'Country_of_Operator': 'United Kingdom',
            'Discovered_Year': 1997,
            'Production_Start': 'Not started',
            'Estimated_Reserves': '572 million tons',
            'Current_Production': 'None',
            'Notes': 'Largest coal reserve, open-pit mining proposed but suspended due to environmental and displacement concerns'
        },
        {
            'Resource_Type': 'Coal',
            'Field_Name': 'Khalashpir Coal Field',
            'Location': 'Rangpur District',
            'Status': 'Undeveloped',
            'Operator': 'Not assigned',
            'Operator_Type': 'N/A',
            'Country_of_Operator': 'N/A',
            'Discovered_Year': 1995,
            'Production_Start': 'Not started',
            'Estimated_Reserves': '1.3 billion tons',
            'Current_Production': 'None',
            'Notes': 'Largest coal reserve in Bangladesh, undeveloped'
        },
        {
            'Resource_Type': 'Coal',
            'Field_Name': 'Dighipara Coal Field',
            'Location': 'Dinajpur District',
            'Status': 'Undeveloped',
            'Operator': 'Not assigned',
            'Operator_Type': 'N/A',
            'Country_of_Operator': 'N/A',
            'Discovered_Year': 1995,
            'Production_Start': 'Not started',
            'Estimated_Reserves': '750 million tons',
            'Current_Production': 'None',
            'Notes': 'Undeveloped reserve'
        },
        {
            'Resource_Type': 'Coal',
            'Field_Name': 'Baramasia Coal Field',
            'Location': 'Nawabganj District',
            'Status': 'Undeveloped',
            'Operator': 'Not assigned',
            'Operator_Type': 'N/A',
            'Country_of_Operator': 'N/A',
            'Discovered_Year': 1995,
            'Production_Start': 'Not started',
            'Estimated_Reserves': '300 million tons',
            'Current_Production': 'None',
            'Notes': 'Undeveloped reserve'
        }
    ]
    
    # Oil Fields
    oil_fields = [
        {
            'Resource_Type': 'Crude Oil',
            'Field_Name': 'Haripur Oil Field',
            'Location': 'Sylhet District',
            'Status': 'Active',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 1986,
            'Production_Start': 1987,
            'Estimated_Reserves': 'Small - Declining',
            'Current_Production': 'Very low - ~200 barrels/day',
            'Notes': 'Only producing oil field, minimal production'
        },
        {
            'Resource_Type': 'Crude Oil',
            'Field_Name': 'Salda Oil Field',
            'Location': 'Sylhet District',
            'Status': 'Inactive',
            'Operator': 'Petrobangla',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': '1980s',
            'Production_Start': 'Limited',
            'Estimated_Reserves': 'Minimal',
            'Current_Production': 'Ceased',
            'Notes': 'Small field, production ceased'
        }
    ]
    
    # LNG Terminals (Import Infrastructure)
    lng_terminals = [
        {
            'Resource_Type': 'LNG Import',
            'Field_Name': 'Summit LNG Terminal',
            'Location': 'Maheshkhali, Cox\'s Bazar',
            'Status': 'Active',
            'Operator': 'Summit Group (Bangladesh)',
            'Operator_Type': 'Private Domestic',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 'N/A',
            'Production_Start': 2019,
            'Estimated_Reserves': 'N/A - Import facility',
            'Current_Production': '500 MMCFD capacity',
            'Notes': 'First LNG terminal, imports from Qatar and other sources'
        },
        {
            'Resource_Type': 'LNG Import',
            'Field_Name': 'Excelerate Energy LNG Terminal',
            'Location': 'Moheshkhali, Cox\'s Bazar',
            'Status': 'Active',
            'Operator': 'Excelerate Energy (USA) & Petrobangla',
            'Operator_Type': 'Foreign Private & State Partnership',
            'Country_of_Operator': 'United States & Bangladesh',
            'Discovered_Year': 'N/A',
            'Production_Start': 2018,
            'Estimated_Reserves': 'N/A - Import facility',
            'Current_Production': '500 MMCFD capacity',
            'Notes': 'Floating Storage Regasification Unit (FSRU)'
        },
        {
            'Resource_Type': 'LNG Import',
            'Field_Name': 'Payra LNG Terminal',
            'Location': 'Payra, Patuakhali',
            'Status': 'Under Construction',
            'Operator': 'Reliance Power (India) & Petrobangla',
            'Operator_Type': 'Foreign Private & State Partnership',
            'Country_of_Operator': 'India & Bangladesh',
            'Discovered_Year': 'N/A',
            'Production_Start': 'Planned',
            'Estimated_Reserves': 'N/A - Import facility',
            'Current_Production': 'Not yet operational',
            'Notes': 'Third LNG terminal under development'
        }
    ]
    
    # Renewable Energy Projects
    renewable_projects = [
        {
            'Resource_Type': 'Solar Power',
            'Field_Name': 'Teknaf Solar Power Plant',
            'Location': 'Teknaf, Cox\'s Bazar',
            'Status': 'Active',
            'Operator': 'Bangladesh Power Development Board (BPDB)',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 'N/A',
            'Production_Start': 2017,
            'Estimated_Reserves': 'N/A - Renewable',
            'Current_Production': '28 MW',
            'Notes': 'Largest solar power plant in Bangladesh'
        },
        {
            'Resource_Type': 'Solar Power',
            'Field_Name': 'Mymensingh Solar Park',
            'Location': 'Mymensingh',
            'Status': 'Active',
            'Operator': 'BPDB',
            'Operator_Type': 'State-Owned',
            'Country_of_Operator': 'Bangladesh',
            'Discovered_Year': 'N/A',
            'Production_Start': 2016,
            'Estimated_Reserves': 'N/A - Renewable',
            'Current_Production': '8 MW',
            'Notes': 'Solar power facility'
        },
        {
            'Resource_Type': 'Wind Power',
            'Field_Name': 'Feni Wind Power Project',
            'Location': 'Feni District',
            'Status': 'Planned',
            'Operator': 'Various private developers',
            'Operator_Type': 'Private',
            'Country_of_Operator': 'Bangladesh/Foreign',
            'Discovered_Year': 'N/A',
            'Production_Start': 'Planned',
            'Estimated_Reserves': 'N/A - Renewable',
            'Current_Production': 'Not yet operational',
            'Notes': 'Wind power potential being explored'
        }
    ]
    
    # Combine all data
    all_resources = (natural_gas_fields + coal_fields + oil_fields + 
                     lng_terminals + renewable_projects)
    
    df = pd.DataFrame(all_resources)
    
    return df

def analyze_ownership(df):
    """Analyze ownership structure of fuel resources"""
    print("\n" + "="*80)
    print("OWNERSHIP ANALYSIS")
    print("="*80)
    
    # Count by operator type
    ownership_counts = df['Operator_Type'].value_counts()
    
    print("\nResources by Ownership Type:")
    for operator_type, count in ownership_counts.items():
        print(f"  {operator_type}: {count} resources")
    
    # Foreign vs Domestic
    print("\n" + "-"*80)
    print("Foreign vs Domestic Control:")
    
    foreign_resources = df[df['Country_of_Operator'] != 'Bangladesh']
    domestic_resources = df[df['Country_of_Operator'] == 'Bangladesh']
    
    print(f"  Domestic Control: {len(domestic_resources)} resources")
    print(f"  Foreign Control: {len(foreign_resources)} resources")
    
    # List foreign operators
    print("\n" + "-"*80)
    print("Foreign Operators in Bangladesh:")
    
    foreign_ops = df[df['Country_of_Operator'] != 'Bangladesh'][
        ['Field_Name', 'Resource_Type', 'Operator', 'Country_of_Operator', 'Status']
    ].drop_duplicates()
    
    for _, row in foreign_ops.iterrows():
        print(f"\n  • {row['Field_Name']} ({row['Resource_Type']})")
        print(f"    Operator: {row['Operator']}")
        print(f"    Country: {row['Country_of_Operator']}")
        print(f"    Status: {row['Status']}")
    
    return ownership_counts

def generate_fuel_report(df):
    """Generate comprehensive fuel resources report"""
    print("\n" + "="*80)
    print("GENERATING REPORT")
    print("="*80)
    
    report = []
    report.append("# Bangladesh Fuel Resources Comprehensive Report")
    report.append("\n## Executive Summary")
    report.append("\nThis report provides a comprehensive overview of Bangladesh's fuel resources,")
    report.append("including natural gas, coal, oil, and renewable energy sources, along with")
    report.append("information about operating companies and ownership structures.")
    
    # Natural Gas
    report.append("\n## 1. Natural Gas Resources")
    report.append("\nBangladesh's primary energy source. The country has multiple gas fields:")
    
    gas_fields = df[df['Resource_Type'] == 'Natural Gas']
    
    report.append(f"\n**Total Gas Fields**: {len(gas_fields)}")
    report.append(f"**Active Fields**: {len(gas_fields[gas_fields['Status'] == 'Active'])}")
    
    report.append("\n### Major Gas Fields:")
    report.append("\n| Field Name | Location | Operator | Ownership | Status |")
    report.append("|------------|----------|----------|-----------|--------|")
    
    for _, row in gas_fields.iterrows():
        ownership = "🇧🇩 Domestic" if row['Country_of_Operator'] == 'Bangladesh' else f"🌍 Foreign ({row['Country_of_Operator']})"
        report.append(f"| {row['Field_Name']} | {row['Location']} | {row['Operator']} | {ownership} | {row['Status']} |")
    
    # Highlight foreign control
    report.append("\n### ⚠️ Foreign Control of Gas Resources:")
    
    foreign_gas = gas_fields[gas_fields['Country_of_Operator'] != 'Bangladesh']
    report.append(f"\n**Chevron (USA)** controls {len(foreign_gas[foreign_gas['Operator'].str.contains('Chevron', na=False)])} major gas fields:")
    
    chevron_fields = foreign_gas[foreign_gas['Operator'].str.contains('Chevron', na=False)]
    for _, row in chevron_fields.iterrows():
        report.append(f"- **{row['Field_Name']}**: {row['Notes']}")
    
    # Coal
    report.append("\n## 2. Coal Resources")
    
    coal_fields = df[df['Resource_Type'] == 'Coal']
    
    report.append(f"\n**Total Coal Fields**: {len(coal_fields)}")
    report.append(f"**Operational**: {len(coal_fields[coal_fields['Status'] == 'Active'])}")
    report.append(f"**Undeveloped**: {len(coal_fields[coal_fields['Status'].str.contains('Undeveloped', na=False)])}")
    
    report.append("\n### Coal Fields:")
    report.append("\n| Field Name | Location | Reserves | Operator | Status |")
    report.append("|------------|----------|----------|----------|--------|")
    
    for _, row in coal_fields.iterrows():
        report.append(f"| {row['Field_Name']} | {row['Location']} | {row['Estimated_Reserves']} | {row['Operator']} | {row['Status']} |")
    
    report.append("\n### ⚠️ Coal Resource Issues:")
    report.append("\n- **Only 1 operational mine** (Barapukuria) out of 5 discovered fields")
    report.append("- **3+ billion tons of coal reserves remain undeveloped**")
    report.append("- Largest field (Phulbari) controlled by UK company but suspended due to controversy")
    report.append("- Bangladesh imports coal despite having significant domestic reserves")
    
    # Oil
    report.append("\n## 3. Crude Oil Resources")
    
    oil_fields = df[df['Resource_Type'] == 'Crude Oil']
    
    report.append(f"\n**Total Oil Fields**: {len(oil_fields)}")
    report.append("\n### Oil Fields:")
    report.append("\n| Field Name | Location | Production | Status |")
    report.append("|------------|----------|------------|--------|")
    
    for _, row in oil_fields.iterrows():
        report.append(f"| {row['Field_Name']} | {row['Location']} | {row['Current_Production']} | {row['Status']} |")
    
    report.append("\n### ⚠️ Oil Resource Reality:")
    report.append("\n- **Minimal domestic oil production** (~200 barrels/day)")
    report.append("- **99%+ of oil needs are imported**")
    report.append("- No significant oil reserves discovered")
    
    # LNG
    report.append("\n## 4. LNG Import Infrastructure")
    
    lng_terminals = df[df['Resource_Type'] == 'LNG Import']
    
    report.append("\n### LNG Terminals:")
    report.append("\n| Terminal | Location | Operator | Ownership | Capacity |")
    report.append("|----------|----------|----------|-----------|----------|")
    
    for _, row in lng_terminals.iterrows():
        ownership = "🇧🇩 Domestic" if row['Country_of_Operator'] == 'Bangladesh' else f"🌍 Foreign ({row['Country_of_Operator']})"
        report.append(f"| {row['Field_Name']} | {row['Location']} | {row['Operator']} | {ownership} | {row['Current_Production']} |")
    
    report.append("\n### ⚠️ LNG Import Dependency:")
    report.append("\n- Bangladesh now imports LNG to meet gas demand")
    report.append("- 2 operational terminals, 1 under construction")
    report.append("- Foreign companies involved in terminal operations")
    
    # Renewable
    report.append("\n## 5. Renewable Energy")
    
    renewable = df[df['Resource_Type'].isin(['Solar Power', 'Wind Power'])]
    
    report.append(f"\n**Total Renewable Projects**: {len(renewable)}")
    report.append("\n### Renewable Energy Projects:")
    report.append("\n| Project | Type | Capacity | Status |")
    report.append("|---------|------|----------|--------|")
    
    for _, row in renewable.iterrows():
        report.append(f"| {row['Field_Name']} | {row['Resource_Type']} | {row['Current_Production']} | {row['Status']} |")
    
    report.append("\n### ⚠️ Renewable Energy Status:")
    report.append("\n- **Very limited renewable energy development**")
    report.append("- Solar and wind potential largely untapped")
    report.append("- Renewable energy <3% of total energy mix")
    
    # Ownership Summary
    report.append("\n## 6. Ownership and Control Summary")
    
    domestic = df[df['Country_of_Operator'] == 'Bangladesh']
    foreign = df[df['Country_of_Operator'] != 'Bangladesh']
    
    report.append(f"\n### Overall Control:")
    report.append(f"- **Domestic Control**: {len(domestic)} resources ({len(domestic)/len(df)*100:.1f}%)")
    report.append(f"- **Foreign Control**: {len(foreign)} resources ({len(foreign)/len(df)*100:.1f}%)")
    
    report.append("\n### Foreign Companies Operating in Bangladesh:")
    
    foreign_companies = foreign.groupby(['Operator', 'Country_of_Operator']).size().reset_index(name='Count')
    
    for _, row in foreign_companies.iterrows():
        report.append(f"\n- **{row['Operator']}** ({row['Country_of_Operator']}): {row['Count']} resource(s)")
    
    # Critical Issues
    report.append("\n## 7. Critical Issues and Findings")
    
    report.append("\n### 🔴 Major Problems:")
    
    report.append("\n1. **Foreign Control of Key Gas Production**")
    report.append("   - Chevron (USA) operates Bibiyana field, producing ~50% of Bangladesh's gas")
    report.append("   - Largest producing field controlled by foreign company")
    
    report.append("\n2. **Underdeveloped Domestic Resources**")
    report.append("   - 3+ billion tons of coal reserves undeveloped")
    report.append("   - Only 1 coal mine operational despite 5 discovered fields")
    report.append("   - Minimal oil production despite exploration")
    
    report.append("\n3. **Import Dependency**")
    report.append("   - Now importing LNG despite having gas reserves")
    report.append("   - 99%+ oil imported")
    report.append("   - Coal imported despite domestic reserves")
    
    report.append("\n4. **Depleting Gas Reserves**")
    report.append("   - Major fields like Titas are depleting")
    report.append("   - Production declining in older fields")
    report.append("   - New discoveries limited")
    
    report.append("\n5. **Limited Renewable Development**")
    report.append("   - Renewable energy <3% of energy mix")
    report.append("   - Solar and wind potential largely untapped")
    report.append("   - Heavy reliance on fossil fuels")
    
    # Save report
    output_dir = Path('analysis/fuel_resources')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir / 'bangladesh_fuel_resources_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"✓ Report saved to: {report_file}")
    
    # Save database
    df.to_csv(output_dir / 'fuel_resources_database.csv', index=False)
    print(f"✓ Database saved to: {output_dir / 'fuel_resources_database.csv'}")

if __name__ == "__main__":
    # Create database
    fuel_df = create_fuel_resources_database()
    
    print(f"\n✓ Created database with {len(fuel_df)} fuel resources")
    
    # Analyze ownership
    ownership_analysis = analyze_ownership(fuel_df)
    
    # Generate report
    generate_fuel_report(fuel_df)
    
    print("\n" + "="*80)
    print("FUEL RESOURCES DATABASE COMPLETED!")
    print("="*80)
    print("\nOutput files:")
    print("  - analysis/fuel_resources/bangladesh_fuel_resources_report.md")
    print("  - analysis/fuel_resources/fuel_resources_database.csv")

# Made with Bob
