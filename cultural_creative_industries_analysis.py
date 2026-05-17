"""
Cultural & Creative Industries Export Potential Analysis
Analyzes Bangladesh's cultural products and creative workforce for export revenue
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
from pathlib import Path

def analyze_available_workforce():
    """Analyze workforce available for cultural/creative industries"""
    
    print("="*80)
    print("CULTURAL & CREATIVE INDUSTRIES - WORKFORCE ANALYSIS")
    print("="*80)
    
    # From previous analysis
    total_pop = 173.56e6
    working_age = 113.71e6
    labor_force = 73.62e6
    employed = 70.94e6
    unemployed = 2.68e6
    not_in_lf = 40.09e6
    
    # Foreign employment potential (moderate scenario)
    will_migrate = 3.05e6
    
    # Available for domestic industries
    available_unemployed = unemployed - (will_migrate * 0.60)  # 60% of migrants from unemployed
    available_not_in_lf = not_in_lf - (will_migrate * 0.40)  # 40% of migrants from not in LF
    
    # Youth population (18-35) - prime for creative industries
    youth_working_age = working_age * 0.45  # 45% are 18-35
    youth_in_creative = youth_working_age * 0.15  # 15% interested in creative work
    
    # Women - significant untapped potential
    women_working_age = working_age * 0.50
    women_in_lf = labor_force * 0.36  # Current female labor participation 36%
    women_not_in_lf = women_working_age - women_in_lf
    women_potential_creative = women_not_in_lf * 0.20  # 20% interested in home-based creative work
    
    print(f"\nTOTAL WORKING AGE POPULATION: {working_age/1e6:.2f}M")
    print(f"\nAVAILABLE WORKFORCE (After Migration):")
    print(f"  Unemployed Available: {available_unemployed/1e6:.2f}M")
    print(f"  Not in Labor Force Available: {available_not_in_lf/1e6:.2f}M")
    print(f"  Youth Interested in Creative: {youth_in_creative/1e6:.2f}M")
    print(f"  Women Potential (Home-based): {women_potential_creative/1e6:.2f}M")
    
    total_potential = youth_in_creative + women_potential_creative
    
    print(f"\n{'='*80}")
    print(f"TOTAL POTENTIAL FOR CREATIVE INDUSTRIES: {total_potential/1e6:.2f}M")
    print(f"{'='*80}")
    
    return {
        'youth_creative': youth_in_creative,
        'women_creative': women_potential_creative,
        'total_potential': total_potential
    }

def create_cultural_products_database():
    """Create database of cultural and creative products with export potential"""
    
    products = [
        # Textiles & Fashion
        {
            'Category': 'Textiles & Fashion',
            'Product': 'Jamdani Sarees',
            'Description': 'UNESCO heritage handwoven muslin sarees',
            'Current_Production_Million_USD': 50,
            'Current_Export_Million_USD': 15,
            'Global_Market_Size_Billion_USD': 2.5,
            'Bangladesh_Market_Share_Percent': 0.6,
            'Export_Potential_Million_USD': 500,
            'Workers_Needed': 50000,
            'Skill_Level': 'High',
            'Production_Location': 'Home-based, clusters',
            'Target_Markets': 'India, USA, UK, Middle East, diaspora',
            'Investment_Needed_Million_USD': 30,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'UNESCO heritage, handcrafted, unique designs'
        },
        {
            'Category': 'Textiles & Fashion',
            'Product': 'Nakshi Kantha (Embroidered Quilts)',
            'Description': 'Traditional embroidered quilts and textiles',
            'Current_Production_Million_USD': 30,
            'Current_Export_Million_USD': 8,
            'Global_Market_Size_Billion_USD': 5.0,
            'Bangladesh_Market_Share_Percent': 0.16,
            'Export_Potential_Million_USD': 300,
            'Workers_Needed': 100000,
            'Skill_Level': 'Medium',
            'Production_Location': 'Home-based, rural women',
            'Target_Markets': 'USA, Europe, Japan, Australia',
            'Investment_Needed_Million_USD': 20,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Handmade, sustainable, storytelling through stitches'
        },
        {
            'Category': 'Textiles & Fashion',
            'Product': 'Contemporary Fashion Design',
            'Description': 'Modern fashion with traditional elements',
            'Current_Production_Million_USD': 100,
            'Current_Export_Million_USD': 20,
            'Global_Market_Size_Billion_USD': 50.0,
            'Bangladesh_Market_Share_Percent': 0.04,
            'Export_Potential_Million_USD': 1000,
            'Workers_Needed': 50000,
            'Skill_Level': 'High',
            'Production_Location': 'Urban studios, factories',
            'Target_Markets': 'Global fashion markets',
            'Investment_Needed_Million_USD': 100,
            'Time_to_Scale': '3-5 years',
            'Unique_Selling_Point': 'Fusion of traditional and modern, ethical fashion'
        },
        
        # Handicrafts
        {
            'Category': 'Handicrafts',
            'Product': 'Jute Products',
            'Description': 'Bags, home decor, fashion accessories from jute',
            'Current_Production_Million_USD': 80,
            'Current_Export_Million_USD': 40,
            'Global_Market_Size_Billion_USD': 3.0,
            'Bangladesh_Market_Share_Percent': 1.33,
            'Export_Potential_Million_USD': 500,
            'Workers_Needed': 200000,
            'Skill_Level': 'Low-Medium',
            'Production_Location': 'Rural clusters, cooperatives',
            'Target_Markets': 'Europe, USA, Japan (eco-conscious)',
            'Investment_Needed_Million_USD': 50,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Eco-friendly, biodegradable, golden fiber'
        },
        {
            'Category': 'Handicrafts',
            'Product': 'Bamboo & Cane Crafts',
            'Description': 'Furniture, baskets, home decor from bamboo',
            'Current_Production_Million_USD': 40,
            'Current_Export_Million_USD': 10,
            'Global_Market_Size_Billion_USD': 8.0,
            'Bangladesh_Market_Share_Percent': 0.125,
            'Export_Potential_Million_USD': 400,
            'Workers_Needed': 150000,
            'Skill_Level': 'Medium',
            'Production_Location': 'Rural areas, tribal communities',
            'Target_Markets': 'Europe, USA, Japan, Australia',
            'Investment_Needed_Million_USD': 40,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Sustainable, natural, artisanal'
        },
        {
            'Category': 'Handicrafts',
            'Product': 'Pottery & Ceramics',
            'Description': 'Traditional and contemporary pottery',
            'Current_Production_Million_USD': 20,
            'Current_Export_Million_USD': 5,
            'Global_Market_Size_Billion_USD': 10.0,
            'Bangladesh_Market_Share_Percent': 0.05,
            'Export_Potential_Million_USD': 200,
            'Workers_Needed': 50000,
            'Skill_Level': 'Medium-High',
            'Production_Location': 'Pottery villages, studios',
            'Target_Markets': 'Global home decor markets',
            'Investment_Needed_Million_USD': 25,
            'Time_to_Scale': '3-4 years',
            'Unique_Selling_Point': 'Handcrafted, unique designs, cultural heritage'
        },
        {
            'Category': 'Handicrafts',
            'Product': 'Leather Goods',
            'Description': 'Bags, shoes, accessories from leather',
            'Current_Production_Million_USD': 60,
            'Current_Export_Million_USD': 25,
            'Global_Market_Size_Billion_USD': 15.0,
            'Bangladesh_Market_Share_Percent': 0.17,
            'Export_Potential_Million_USD': 400,
            'Workers_Needed': 80000,
            'Skill_Level': 'Medium-High',
            'Production_Location': 'Dhaka, Chittagong clusters',
            'Target_Markets': 'Europe, USA, Middle East',
            'Investment_Needed_Million_USD': 50,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Quality craftsmanship, competitive pricing'
        },
        
        # Performing Arts & Entertainment
        {
            'Category': 'Performing Arts',
            'Product': 'Music & Film Production',
            'Description': 'Bengali music, films, web series',
            'Current_Production_Million_USD': 150,
            'Current_Export_Million_USD': 20,
            'Global_Market_Size_Billion_USD': 100.0,
            'Bangladesh_Market_Share_Percent': 0.02,
            'Export_Potential_Million_USD': 500,
            'Workers_Needed': 100000,
            'Skill_Level': 'High',
            'Production_Location': 'Dhaka studios, digital platforms',
            'Target_Markets': 'Bengali diaspora, South Asia, OTT platforms',
            'Investment_Needed_Million_USD': 200,
            'Time_to_Scale': '3-5 years',
            'Unique_Selling_Point': '300M Bengali speakers globally, rich storytelling'
        },
        {
            'Category': 'Performing Arts',
            'Product': 'Traditional Dance & Theater',
            'Description': 'Cultural performances, festivals',
            'Current_Production_Million_USD': 10,
            'Current_Export_Million_USD': 2,
            'Global_Market_Size_Billion_USD': 5.0,
            'Bangladesh_Market_Share_Percent': 0.04,
            'Export_Potential_Million_USD': 50,
            'Workers_Needed': 20000,
            'Skill_Level': 'High',
            'Production_Location': 'Cultural centers, touring',
            'Target_Markets': 'International festivals, cultural exchanges',
            'Investment_Needed_Million_USD': 15,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Rich cultural heritage, unique art forms'
        },
        
        # Digital & Creative Services
        {
            'Category': 'Digital Creative',
            'Product': 'Graphic Design & Animation',
            'Description': 'Digital design, 2D/3D animation services',
            'Current_Production_Million_USD': 100,
            'Current_Export_Million_USD': 80,
            'Global_Market_Size_Billion_USD': 45.0,
            'Bangladesh_Market_Share_Percent': 0.18,
            'Export_Potential_Million_USD': 1000,
            'Workers_Needed': 200000,
            'Skill_Level': 'Medium-High',
            'Production_Location': 'Home-based, studios, remote',
            'Target_Markets': 'Global (USA, Europe, Asia)',
            'Investment_Needed_Million_USD': 80,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Cost-effective, skilled workforce, English proficiency'
        },
        {
            'Category': 'Digital Creative',
            'Product': 'Content Writing & Translation',
            'Description': 'Content creation, Bengali-English translation',
            'Current_Production_Million_USD': 50,
            'Current_Export_Million_USD': 40,
            'Global_Market_Size_Billion_USD': 20.0,
            'Bangladesh_Market_Share_Percent': 0.20,
            'Export_Potential_Million_USD': 300,
            'Workers_Needed': 150000,
            'Skill_Level': 'Medium',
            'Production_Location': 'Home-based, remote',
            'Target_Markets': 'Global content markets',
            'Investment_Needed_Million_USD': 30,
            'Time_to_Scale': '1-2 years',
            'Unique_Selling_Point': 'Bilingual, cultural understanding, cost-effective'
        },
        {
            'Category': 'Digital Creative',
            'Product': 'Game Development',
            'Description': 'Mobile games, casual games',
            'Current_Production_Million_USD': 20,
            'Current_Export_Million_USD': 15,
            'Global_Market_Size_Billion_USD': 200.0,
            'Bangladesh_Market_Share_Percent': 0.0075,
            'Export_Potential_Million_USD': 500,
            'Workers_Needed': 50000,
            'Skill_Level': 'High',
            'Production_Location': 'Studios, remote teams',
            'Target_Markets': 'Global mobile gaming market',
            'Investment_Needed_Million_USD': 100,
            'Time_to_Scale': '3-5 years',
            'Unique_Selling_Point': 'Young talent, cost-effective, growing ecosystem'
        },
        
        # Food & Culinary
        {
            'Category': 'Food & Culinary',
            'Product': 'Packaged Bengali Food',
            'Description': 'Ready-to-eat Bengali cuisine, snacks',
            'Current_Production_Million_USD': 80,
            'Current_Export_Million_USD': 30,
            'Global_Market_Size_Billion_USD': 30.0,
            'Bangladesh_Market_Share_Percent': 0.10,
            'Export_Potential_Million_USD': 500,
            'Workers_Needed': 100000,
            'Skill_Level': 'Low-Medium',
            'Production_Location': 'Food processing units',
            'Target_Markets': 'Bengali diaspora, South Asian markets',
            'Investment_Needed_Million_USD': 80,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Authentic taste, diaspora demand, halal'
        },
        {
            'Category': 'Food & Culinary',
            'Product': 'Spices & Condiments',
            'Description': 'Traditional spice blends, sauces',
            'Current_Production_Million_USD': 40,
            'Current_Export_Million_USD': 15,
            'Global_Market_Size_Billion_USD': 20.0,
            'Bangladesh_Market_Share_Percent': 0.075,
            'Export_Potential_Million_USD': 200,
            'Workers_Needed': 50000,
            'Skill_Level': 'Low-Medium',
            'Production_Location': 'Processing units, cooperatives',
            'Target_Markets': 'Global ethnic food markets',
            'Investment_Needed_Million_USD': 40,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Authentic recipes, quality, organic options'
        },
        
        # Literature & Publishing
        {
            'Category': 'Literature',
            'Product': 'Bengali Literature & Translation',
            'Description': 'Books, e-books, audiobooks',
            'Current_Production_Million_USD': 30,
            'Current_Export_Million_USD': 5,
            'Global_Market_Size_Billion_USD': 10.0,
            'Bangladesh_Market_Share_Percent': 0.05,
            'Export_Potential_Million_USD': 100,
            'Workers_Needed': 30000,
            'Skill_Level': 'High',
            'Production_Location': 'Publishing houses, digital',
            'Target_Markets': 'Bengali diaspora, South Asia, global',
            'Investment_Needed_Million_USD': 20,
            'Time_to_Scale': '2-3 years',
            'Unique_Selling_Point': 'Rich literary tradition, Nobel laureate heritage'
        },
        
        # Tourism & Cultural Services
        {
            'Category': 'Tourism',
            'Product': 'Cultural Tourism Services',
            'Description': 'Heritage tours, cultural experiences',
            'Current_Production_Million_USD': 50,
            'Current_Export_Million_USD': 40,
            'Global_Market_Size_Billion_USD': 200.0,
            'Bangladesh_Market_Share_Percent': 0.02,
            'Export_Potential_Million_USD': 500,
            'Workers_Needed': 100000,
            'Skill_Level': 'Medium',
            'Production_Location': 'Heritage sites, cultural centers',
            'Target_Markets': 'Global tourists, cultural enthusiasts',
            'Investment_Needed_Million_USD': 150,
            'Time_to_Scale': '3-5 years',
            'Unique_Selling_Point': 'UNESCO sites, Sundarbans, rich culture'
        }
    ]
    
    return pd.DataFrame(products)

def analyze_export_potential(df):
    """Analyze export potential"""
    
    print(f"\n{'='*80}")
    print("CULTURAL & CREATIVE PRODUCTS - EXPORT POTENTIAL")
    print(f"{'='*80}")
    
    total_current_export = df['Current_Export_Million_USD'].sum()
    total_potential_export = df['Export_Potential_Million_USD'].sum()
    total_workers = df['Workers_Needed'].sum()
    total_investment = df['Investment_Needed_Million_USD'].sum()
    
    print(f"\nCurrent Export: ${total_current_export}M")
    print(f"Potential Export: ${total_potential_export}M")
    print(f"Increase: ${total_potential_export - total_current_export}M ({((total_potential_export/total_current_export)-1)*100:.0f}%)")
    print(f"\nWorkers Needed: {total_workers/1e6:.2f}M")
    print(f"Investment Required: ${total_investment}M")
    print(f"ROI: {(total_potential_export - total_current_export)/total_investment:.1f}x annually")
    
    # By category
    print(f"\n{'-'*80}")
    print("BY CATEGORY:")
    print(f"{'-'*80}")
    
    category_summary = df.groupby('Category').agg({
        'Current_Export_Million_USD': 'sum',
        'Export_Potential_Million_USD': 'sum',
        'Workers_Needed': 'sum',
        'Investment_Needed_Million_USD': 'sum'
    }).sort_values('Export_Potential_Million_USD', ascending=False)
    
    for category, row in category_summary.iterrows():
        current = row['Current_Export_Million_USD']
        potential = row['Export_Potential_Million_USD']
        workers = row['Workers_Needed']
        investment = row['Investment_Needed_Million_USD']
        increase = potential - current
        
        print(f"\n{category}:")
        print(f"  Current: ${current:.0f}M | Potential: ${potential:.0f}M | Increase: ${increase:.0f}M")
        print(f"  Workers: {workers/1000:.0f}K | Investment: ${investment:.0f}M")
    
    return total_potential_export, total_workers

def generate_report(df, workforce_data):
    """Generate comprehensive report"""
    
    output_dir = Path('analysis/cultural_creative_industries')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save full database
    df.to_csv(output_dir / 'cultural_products_database.csv', index=False)
    
    # High potential products (>$300M)
    high_potential = df[df['Export_Potential_Million_USD'] >= 300]
    high_potential.to_csv(output_dir / 'high_potential_cultural_products.csv', index=False)
    
    # Women-friendly products (home-based, low-medium skill)
    women_friendly = df[df['Production_Location'].str.contains('Home-based|Rural', case=False, na=False)]
    women_friendly.to_csv(output_dir / 'women_friendly_products.csv', index=False)
    
    print(f"\n✓ Reports saved to {output_dir}")

if __name__ == "__main__":
    workforce_data = analyze_available_workforce()
    df = create_cultural_products_database()
    total_export, total_workers = analyze_export_potential(df)
    generate_report(df, workforce_data)
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETED!")
    print(f"{'='*80}")
    print(f"\nKEY FINDINGS:")
    print(f"- Available Workforce: {workforce_data['total_potential']/1e6:.2f}M")
    print(f"- Workers Needed: {total_workers/1e6:.2f}M")
    print(f"- Export Potential: ${total_export}M")
    print(f"- Workforce Utilization: {(total_workers/workforce_data['total_potential'])*100:.1f}%")

# Made with Bob
