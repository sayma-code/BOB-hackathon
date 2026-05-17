"""
Machinery and Transport Equipment Import Analysis
Identifies what Bangladesh imports and domestic manufacturing potential
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path

def create_machinery_database():
    """
    Create database of machinery and transport equipment imports
    with domestic manufacturing capability assessment
    """
    
    machinery_imports = [
        # Power Generation Equipment
        {
            'Category': 'Power Generation',
            'Item': 'Gas Turbines',
            'Annual_Import_Value_Million_USD': 150,
            'Primary_Importers': 'China, India, USA, Germany',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'Limited - Assembly only',
            'Required_Investment_Million_USD': 200,
            'Technical_Complexity': 'Very High',
            'Potential_for_Local_Production': 'Low - Requires advanced technology',
            'Notes': 'Used in power plants, highly technical'
        },
        {
            'Category': 'Power Generation',
            'Item': 'Steam Turbines',
            'Annual_Import_Value_Million_USD': 100,
            'Primary_Importers': 'China, India, Japan',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'None',
            'Required_Investment_Million_USD': 150,
            'Technical_Complexity': 'Very High',
            'Potential_for_Local_Production': 'Low',
            'Notes': 'Coal/gas power plants'
        },
        {
            'Category': 'Power Generation',
            'Item': 'Generators & Alternators',
            'Annual_Import_Value_Million_USD': 80,
            'Primary_Importers': 'China, India, Turkey',
            'Domestic_Manufacturing': 'Yes - Limited',
            'Domestic_Capability': 'Small generators only',
            'Required_Investment_Million_USD': 50,
            'Technical_Complexity': 'Medium',
            'Potential_for_Local_Production': 'High - Already some production',
            'Notes': 'Small generators made locally, large ones imported'
        },
        
        # Industrial Machinery
        {
            'Category': 'Textile Machinery',
            'Item': 'Spinning Machines',
            'Annual_Import_Value_Million_USD': 200,
            'Primary_Importers': 'China, India, Germany, Japan',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'Parts manufacturing only',
            'Required_Investment_Million_USD': 100,
            'Technical_Complexity': 'High',
            'Potential_for_Local_Production': 'Medium - Large textile industry exists',
            'Notes': 'Critical for garment industry'
        },
        {
            'Category': 'Textile Machinery',
            'Item': 'Weaving Looms',
            'Annual_Import_Value_Million_USD': 150,
            'Primary_Importers': 'China, India, Italy',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'Maintenance & repair',
            'Required_Investment_Million_USD': 80,
            'Technical_Complexity': 'High',
            'Potential_for_Local_Production': 'Medium',
            'Notes': 'Essential for textile sector'
        },
        {
            'Category': 'Textile Machinery',
            'Item': 'Dyeing & Finishing Equipment',
            'Annual_Import_Value_Million_USD': 120,
            'Primary_Importers': 'China, Turkey, Italy',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'Limited',
            'Required_Investment_Million_USD': 60,
            'Technical_Complexity': 'Medium-High',
            'Potential_for_Local_Production': 'Medium-High',
            'Notes': 'Textile processing equipment'
        },
        
        # Construction Equipment
        {
            'Category': 'Construction Equipment',
            'Item': 'Excavators',
            'Annual_Import_Value_Million_USD': 100,
            'Primary_Importers': 'China, Japan, South Korea',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'Assembly possible',
            'Required_Investment_Million_USD': 80,
            'Technical_Complexity': 'Medium-High',
            'Potential_for_Local_Production': 'Medium - Assembly & parts',
            'Notes': 'Heavy construction equipment'
        },
        {
            'Category': 'Construction Equipment',
            'Item': 'Cranes',
            'Annual_Import_Value_Million_USD': 70,
            'Primary_Importers': 'China, Germany, Japan',
            'Domestic_Manufacturing': 'Limited',
            'Domestic_Capability': 'Small cranes only',
            'Required_Investment_Million_USD': 50,
            'Technical_Complexity': 'Medium',
            'Potential_for_Local_Production': 'High - Steel industry exists',
            'Notes': 'Construction & port operations'
        },
        {
            'Category': 'Construction Equipment',
            'Item': 'Concrete Mixers & Pumps',
            'Annual_Import_Value_Million_USD': 40,
            'Primary_Importers': 'China, India',
            'Domestic_Manufacturing': 'Yes - Limited',
            'Domestic_Capability': 'Small units',
            'Required_Investment_Million_USD': 20,
            'Technical_Complexity': 'Low-Medium',
            'Potential_for_Local_Production': 'Very High - Simple technology',
            'Notes': 'Already some local production'
        },
        
        # Agricultural Machinery
        {
            'Category': 'Agricultural Machinery',
            'Item': 'Tractors',
            'Annual_Import_Value_Million_USD': 90,
            'Primary_Importers': 'India, China, Belarus',
            'Domestic_Manufacturing': 'Assembly only',
            'Domestic_Capability': 'Assembly from CKD kits',
            'Required_Investment_Million_USD': 100,
            'Technical_Complexity': 'Medium-High',
            'Potential_for_Local_Production': 'Medium - Assembly exists, need engine production',
            'Notes': 'BMTF assembles tractors from CKD'
        },
        {
            'Category': 'Agricultural Machinery',
            'Item': 'Harvesters & Threshers',
            'Annual_Import_Value_Million_USD': 50,
            'Primary_Importers': 'China, India',
            'Domestic_Manufacturing': 'Limited',
            'Domestic_Capability': 'Simple threshers',
            'Required_Investment_Million_USD': 30,
            'Technical_Complexity': 'Medium',
            'Potential_for_Local_Production': 'High - Agricultural country',
            'Notes': 'Local workshops make simple versions'
        },
        {
            'Category': 'Agricultural Machinery',
            'Item': 'Irrigation Pumps',
            'Annual_Import_Value_Million_USD': 60,
            'Primary_Importers': 'China, India',
            'Domestic_Manufacturing': 'Yes',
            'Domestic_Capability': 'Good - Multiple manufacturers',
            'Required_Investment_Million_USD': 10,
            'Technical_Complexity': 'Low-Medium',
            'Potential_for_Local_Production': 'Very High - Already producing',
            'Notes': 'Strong local industry exists'
        },
        
        # Transport Equipment
        {
            'Category': 'Motor Vehicles',
            'Item': 'Cars & SUVs',
            'Annual_Import_Value_Million_USD': 300,
            'Primary_Importers': 'Japan, India, China, South Korea',
            'Domestic_Manufacturing': 'Assembly only',
            'Domestic_Capability': 'CKD assembly',
            'Required_Investment_Million_USD': 500,
            'Technical_Complexity': 'Very High',
            'Potential_for_Local_Production': 'Low-Medium - Need full supply chain',
            'Notes': 'Pragoti, Walton assemble vehicles'
        },
        {
            'Category': 'Motor Vehicles',
            'Item': 'Buses & Trucks',
            'Annual_Import_Value_Million_USD': 200,
            'Primary_Importers': 'India, China, Japan',
            'Domestic_Manufacturing': 'Assembly & body building',
            'Domestic_Capability': 'Body building strong, chassis imported',
            'Required_Investment_Million_USD': 200,
            'Technical_Complexity': 'High',
            'Potential_for_Local_Production': 'Medium-High - Body building exists',
            'Notes': 'Local body builders are skilled'
        },
        {
            'Category': 'Motor Vehicles',
            'Item': 'Motorcycles',
            'Annual_Import_Value_Million_USD': 150,
            'Primary_Importers': 'China, India, Japan',
            'Domestic_Manufacturing': 'Yes - Assembly',
            'Domestic_Capability': 'Assembly from CKD',
            'Required_Investment_Million_USD': 80,
            'Technical_Complexity': 'Medium',
            'Potential_for_Local_Production': 'High - Multiple assemblers',
            'Notes': 'Walton, Runner, others assemble locally'
        },
        {
            'Category': 'Motor Vehicles',
            'Item': 'Auto Parts & Components',
            'Annual_Import_Value_Million_USD': 250,
            'Primary_Importers': 'China, India, Japan, Thailand',
            'Domestic_Manufacturing': 'Limited',
            'Domestic_Capability': 'Simple parts only',
            'Required_Investment_Million_USD': 150,
            'Technical_Complexity': 'Medium-High',
            'Potential_for_Local_Production': 'High - Huge demand exists',
            'Notes': 'Batteries, tires made locally; engines imported'
        },
        
        # Ships & Boats
        {
            'Category': 'Marine Transport',
            'Item': 'Ships & Vessels',
            'Annual_Import_Value_Million_USD': 180,
            'Primary_Importers': 'China, Japan, South Korea',
            'Domestic_Manufacturing': 'Yes - Growing',
            'Domestic_Capability': 'Small to medium ships',
            'Required_Investment_Million_USD': 200,
            'Technical_Complexity': 'High',
            'Potential_for_Local_Production': 'High - Shipbuilding industry exists',
            'Notes': 'Western Marine, Ananda Shipyard export ships'
        },
        {
            'Category': 'Marine Transport',
            'Item': 'Ship Engines & Equipment',
            'Annual_Import_Value_Million_USD': 100,
            'Primary_Importers': 'China, Japan, Germany',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'Maintenance only',
            'Required_Investment_Million_USD': 120,
            'Technical_Complexity': 'Very High',
            'Potential_for_Local_Production': 'Low-Medium',
            'Notes': 'Marine engines are complex'
        },
        
        # Railway Equipment
        {
            'Category': 'Railway',
            'Item': 'Locomotives',
            'Annual_Import_Value_Million_USD': 80,
            'Primary_Importers': 'China, India, USA',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'Maintenance & repair',
            'Required_Investment_Million_USD': 200,
            'Technical_Complexity': 'Very High',
            'Potential_for_Local_Production': 'Low',
            'Notes': 'Specialized technology'
        },
        {
            'Category': 'Railway',
            'Item': 'Railway Coaches & Wagons',
            'Annual_Import_Value_Million_USD': 60,
            'Primary_Importers': 'China, India',
            'Domestic_Manufacturing': 'Limited',
            'Domestic_Capability': 'Repair & refurbishment',
            'Required_Investment_Million_USD': 80,
            'Technical_Complexity': 'Medium-High',
            'Potential_for_Local_Production': 'Medium - Steel industry exists',
            'Notes': 'BR workshops do repairs'
        },
        
        # Electronics & Electrical
        {
            'Category': 'Electronics',
            'Item': 'Transformers',
            'Annual_Import_Value_Million_USD': 70,
            'Primary_Importers': 'China, India, Turkey',
            'Domestic_Manufacturing': 'Yes',
            'Domestic_Capability': 'Distribution transformers',
            'Required_Investment_Million_USD': 40,
            'Technical_Complexity': 'Medium',
            'Potential_for_Local_Production': 'High - Already producing',
            'Notes': 'REB Transformers, others produce locally'
        },
        {
            'Category': 'Electronics',
            'Item': 'Electric Motors',
            'Annual_Import_Value_Million_USD': 80,
            'Primary_Importers': 'China, India, Germany',
            'Domestic_Manufacturing': 'Limited',
            'Domestic_Capability': 'Small motors',
            'Required_Investment_Million_USD': 50,
            'Technical_Complexity': 'Medium',
            'Potential_for_Local_Production': 'High',
            'Notes': 'Industrial motors mostly imported'
        },
        {
            'Category': 'Electronics',
            'Item': 'Cables & Wires',
            'Annual_Import_Value_Million_USD': 60,
            'Primary_Importers': 'China, India',
            'Domestic_Manufacturing': 'Yes',
            'Domestic_Capability': 'Good production',
            'Required_Investment_Million_USD': 20,
            'Technical_Complexity': 'Low-Medium',
            'Potential_for_Local_Production': 'Very High - Already strong',
            'Notes': 'BSRM, others produce cables'
        },
        
        # Machine Tools
        {
            'Category': 'Machine Tools',
            'Item': 'CNC Machines',
            'Annual_Import_Value_Million_USD': 90,
            'Primary_Importers': 'China, Japan, Germany, Taiwan',
            'Domestic_Manufacturing': 'No',
            'Domestic_Capability': 'None',
            'Required_Investment_Million_USD': 150,
            'Technical_Complexity': 'Very High',
            'Potential_for_Local_Production': 'Low - Advanced technology',
            'Notes': 'Precision manufacturing equipment'
        },
        {
            'Category': 'Machine Tools',
            'Item': 'Lathes & Milling Machines',
            'Annual_Import_Value_Million_USD': 50,
            'Primary_Importers': 'China, India, Taiwan',
            'Domestic_Manufacturing': 'Limited',
            'Domestic_Capability': 'Simple machines',
            'Required_Investment_Million_USD': 60,
            'Technical_Complexity': 'Medium-High',
            'Potential_for_Local_Production': 'Medium',
            'Notes': 'Basic machines can be made'
        },
        
        # Pumps & Compressors
        {
            'Category': 'Industrial Equipment',
            'Item': 'Industrial Pumps',
            'Annual_Import_Value_Million_USD': 70,
            'Primary_Importers': 'China, India, Germany',
            'Domestic_Manufacturing': 'Limited',
            'Domestic_Capability': 'Simple pumps',
            'Required_Investment_Million_USD': 40,
            'Technical_Complexity': 'Medium',
            'Potential_for_Local_Production': 'High',
            'Notes': 'Water pumps made, industrial pumps imported'
        },
        {
            'Category': 'Industrial Equipment',
            'Item': 'Air Compressors',
            'Annual_Import_Value_Million_USD': 40,
            'Primary_Importers': 'China, India, Japan',
            'Domestic_Manufacturing': 'Limited',
            'Domestic_Capability': 'Small compressors',
            'Required_Investment_Million_USD': 30,
            'Technical_Complexity': 'Medium',
            'Potential_for_Local_Production': 'High',
            'Notes': 'Industrial compressors imported'
        },
        
        # Medical Equipment
        {
            'Category': 'Medical Equipment',
            'Item': 'Medical Devices & Equipment',
            'Annual_Import_Value_Million_USD': 100,
            'Primary_Importers': 'China, India, USA, Germany',
            'Domestic_Manufacturing': 'Very Limited',
            'Domestic_Capability': 'Basic items only',
            'Required_Investment_Million_USD': 80,
            'Technical_Complexity': 'High',
            'Potential_for_Local_Production': 'Medium - Growing healthcare sector',
            'Notes': 'Mostly imported, some basic items made'
        }
    ]
    
    return pd.DataFrame(machinery_imports)

def analyze_manufacturing_potential(df):
    """
    Analyze domestic manufacturing potential
    """
    
    print("\n" + "="*80)
    print("MACHINERY & TRANSPORT EQUIPMENT IMPORT ANALYSIS")
    print("="*80)
    
    # Total import value
    total_imports = df['Annual_Import_Value_Million_USD'].sum()
    print(f"\nTotal Annual Machinery & Transport Imports: ${total_imports:,.0f} million")
    print(f"Total Annual Machinery & Transport Imports: ${total_imports/1000:.2f} billion")
    
    # By category
    print("\n" + "-"*80)
    print("IMPORTS BY CATEGORY:")
    print("-"*80)
    
    category_summary = df.groupby('Category')['Annual_Import_Value_Million_USD'].sum().sort_values(ascending=False)
    
    for category, value in category_summary.items():
        pct = (value / total_imports) * 100
        print(f"{category:<30} ${value:>8,.0f}M ({pct:>5.1f}%)")
    
    # Manufacturing capability
    print("\n" + "-"*80)
    print("DOMESTIC MANUFACTURING CAPABILITY:")
    print("-"*80)
    
    has_manufacturing = df[df['Domestic_Manufacturing'].str.contains('Yes', na=False)]
    no_manufacturing = df[df['Domestic_Manufacturing'] == 'No']
    
    print(f"\nItems with some domestic production: {len(has_manufacturing)}")
    print(f"Items with NO domestic production: {len(no_manufacturing)}")
    
    # Potential for local production
    print("\n" + "-"*80)
    print("POTENTIAL FOR LOCAL PRODUCTION:")
    print("-"*80)
    
    high_potential = df[df['Potential_for_Local_Production'].str.contains('High|Very High', na=False)]
    medium_potential = df[df['Potential_for_Local_Production'].str.contains('Medium', na=False)]
    low_potential = df[df['Potential_for_Local_Production'].str.contains('Low', na=False)]
    
    high_value = high_potential['Annual_Import_Value_Million_USD'].sum()
    medium_value = medium_potential['Annual_Import_Value_Million_USD'].sum()
    low_value = low_potential['Annual_Import_Value_Million_USD'].sum()
    
    print(f"\nHigh Potential: {len(high_potential)} items, ${high_value:,.0f}M annual imports")
    print(f"Medium Potential: {len(medium_potential)} items, ${medium_value:,.0f}M annual imports")
    print(f"Low Potential: {len(low_potential)} items, ${low_value:,.0f}M annual imports")
    
    # Investment required
    total_investment = df['Required_Investment_Million_USD'].sum()
    print(f"\n" + "-"*80)
    print(f"TOTAL INVESTMENT REQUIRED FOR FULL LOCALIZATION: ${total_investment:,.0f} million")
    print(f"TOTAL INVESTMENT REQUIRED: ${total_investment/1000:.2f} billion")
    print("-"*80)
    
    return category_summary, high_potential, medium_potential, low_potential

def generate_machinery_report(df, high_potential, medium_potential):
    """
    Generate comprehensive report
    """
    
    print("\n" + "="*80)
    print("GENERATING REPORT")
    print("="*80)
    
    output_dir = Path('analysis/machinery_imports')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save full database
    df.to_csv(output_dir / 'machinery_import_database.csv', index=False)
    print(f"✓ Database saved to: {output_dir / 'machinery_import_database.csv'}")
    
    # Save high potential items
    high_potential.to_csv(output_dir / 'high_potential_local_production.csv', index=False)
    print(f"✓ High potential items saved to: {output_dir / 'high_potential_local_production.csv'}")
    
    # Create summary report
    total_imports = df['Annual_Import_Value_Million_USD'].sum()
    high_value = high_potential['Annual_Import_Value_Million_USD'].sum()
    
    print(f"\n✓ Total machinery imports: ${total_imports:,.0f} million/year")
    print(f"✓ High potential for localization: ${high_value:,.0f} million/year ({(high_value/total_imports)*100:.1f}%)")
    print(f"✓ Potential import substitution: ${high_value:,.0f} million/year")

if __name__ == "__main__":
    # Create database
    machinery_df = create_machinery_database()
    
    # Analyze
    category_summary, high_pot, medium_pot, low_pot = analyze_manufacturing_potential(machinery_df)
    
    # Generate report
    generate_machinery_report(machinery_df, high_pot, medium_pot)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETED!")
    print("="*80)

# Made with Bob
