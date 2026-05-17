"""
Manufactures Import Analysis - Local Production Potential
Analyzes what manufactured goods Bangladesh imports and local production capability
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path

def create_manufactures_database():
    """
    Create database of manufactured goods imports with local production potential
    """
    
    manufactures = [
        # Chemicals & Pharmaceuticals
        {
            'Category': 'Chemicals & Pharmaceuticals',
            'Item': 'Pharmaceutical Products',
            'Annual_Import_Million_USD': 1500,
            'Primary_Importers': 'India, China, Europe',
            'Current_Local_Production': 'Good - 98% of domestic demand',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - Strong pharmaceutical industry',
            'Technical_Complexity': 'Medium-High',
            'Investment_Needed_Million_USD': 200,
            'Potential_Local_Production_Percentage': 80,
            'Import_Reduction_Million_USD': 1200,
            'Key_Companies': 'Square, Beximco, Incepta, Renata',
            'Challenges': 'API imports, advanced formulations',
            'Recommendations': 'API manufacturing, R&D investment, export focus'
        },
        {
            'Category': 'Chemicals & Pharmaceuticals',
            'Item': 'Industrial Chemicals',
            'Annual_Import_Million_USD': 2000,
            'Primary_Importers': 'China, India, Middle East',
            'Current_Local_Production': 'Limited',
            'Local_Production_Potential': 'Medium',
            'Existing_Industry': 'Limited',
            'Technical_Complexity': 'High',
            'Investment_Needed_Million_USD': 800,
            'Potential_Local_Production_Percentage': 40,
            'Import_Reduction_Million_USD': 800,
            'Key_Companies': 'Few local producers',
            'Challenges': 'Technology, environmental concerns',
            'Recommendations': 'Petrochemical complex, environmental standards'
        },
        {
            'Category': 'Chemicals & Pharmaceuticals',
            'Item': 'Fertilizers',
            'Annual_Import_Million_USD': 800,
            'Primary_Importers': 'China, Middle East, India',
            'Current_Local_Production': 'Yes - Urea production',
            'Local_Production_Potential': 'High',
            'Existing_Industry': 'Yes - BCIC factories',
            'Technical_Complexity': 'Medium-High',
            'Investment_Needed_Million_USD': 300,
            'Potential_Local_Production_Percentage': 70,
            'Import_Reduction_Million_USD': 560,
            'Key_Companies': 'BCIC, Jamuna Fertilizer',
            'Challenges': 'Gas supply, technology',
            'Recommendations': 'Modernize plants, diversify products'
        },
        {
            'Category': 'Chemicals & Pharmaceuticals',
            'Item': 'Plastics & Polymers',
            'Annual_Import_Million_USD': 1800,
            'Primary_Importers': 'China, Thailand, Saudi Arabia',
            'Current_Local_Production': 'Limited - Recycling only',
            'Local_Production_Potential': 'High',
            'Existing_Industry': 'Recycling, some production',
            'Technical_Complexity': 'Medium-High',
            'Investment_Needed_Million_USD': 600,
            'Potential_Local_Production_Percentage': 50,
            'Import_Reduction_Million_USD': 900,
            'Key_Companies': 'RFL, Partex, others',
            'Challenges': 'Petrochemical feedstock',
            'Recommendations': 'Petrochemical industry, recycling expansion'
        },
        
        # Metals & Metal Products
        {
            'Category': 'Metals & Metal Products',
            'Item': 'Iron & Steel',
            'Annual_Import_Million_USD': 3500,
            'Primary_Importers': 'China, India, Japan, South Korea',
            'Current_Local_Production': 'Yes - Re-rolling mills',
            'Local_Production_Potential': 'High',
            'Existing_Industry': 'Yes - Strong steel industry',
            'Technical_Complexity': 'Medium-High',
            'Investment_Needed_Million_USD': 1000,
            'Potential_Local_Production_Percentage': 60,
            'Import_Reduction_Million_USD': 2100,
            'Key_Companies': 'BSRM, GPH Ispat, Abul Khair',
            'Challenges': 'Scrap dependency, primary steel',
            'Recommendations': 'Integrated steel mill, iron ore processing'
        },
        {
            'Category': 'Metals & Metal Products',
            'Item': 'Aluminum Products',
            'Annual_Import_Million_USD': 500,
            'Primary_Importers': 'China, India, Middle East',
            'Current_Local_Production': 'Limited',
            'Local_Production_Potential': 'Medium',
            'Existing_Industry': 'Fabrication only',
            'Technical_Complexity': 'High',
            'Investment_Needed_Million_USD': 400,
            'Potential_Local_Production_Percentage': 40,
            'Import_Reduction_Million_USD': 200,
            'Key_Companies': 'Few fabricators',
            'Challenges': 'Energy intensive, bauxite imports',
            'Recommendations': 'Aluminum smelter, value addition'
        },
        {
            'Category': 'Metals & Metal Products',
            'Item': 'Metal Products & Hardware',
            'Annual_Import_Million_USD': 800,
            'Primary_Importers': 'China, India, Taiwan',
            'Current_Local_Production': 'Good',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - Many manufacturers',
            'Technical_Complexity': 'Low-Medium',
            'Investment_Needed_Million_USD': 150,
            'Potential_Local_Production_Percentage': 80,
            'Import_Reduction_Million_USD': 640,
            'Key_Companies': 'Numerous SMEs',
            'Challenges': 'Quality, standardization',
            'Recommendations': 'Quality improvement, standards'
        },
        
        # Electronics & Electrical
        {
            'Category': 'Electronics & Electrical',
            'Item': 'Consumer Electronics',
            'Annual_Import_Million_USD': 2500,
            'Primary_Importers': 'China, Japan, South Korea, Thailand',
            'Current_Local_Production': 'Assembly only',
            'Local_Production_Potential': 'Medium',
            'Existing_Industry': 'Yes - Walton, others assemble',
            'Technical_Complexity': 'High',
            'Investment_Needed_Million_USD': 800,
            'Potential_Local_Production_Percentage': 50,
            'Import_Reduction_Million_USD': 1250,
            'Key_Companies': 'Walton, Singer, Vision',
            'Challenges': 'Component manufacturing, technology',
            'Recommendations': 'Component manufacturing, R&D'
        },
        {
            'Category': 'Electronics & Electrical',
            'Item': 'Mobile Phones & Accessories',
            'Annual_Import_Million_USD': 1500,
            'Primary_Importers': 'China, Vietnam, India',
            'Current_Local_Production': 'Assembly starting',
            'Local_Production_Potential': 'High',
            'Existing_Industry': 'Assembly plants emerging',
            'Technical_Complexity': 'High',
            'Investment_Needed_Million_USD': 500,
            'Potential_Local_Production_Percentage': 60,
            'Import_Reduction_Million_USD': 900,
            'Key_Companies': 'Walton, Symphony, others',
            'Challenges': 'Component imports, technology',
            'Recommendations': 'Component ecosystem, attract brands'
        },
        {
            'Category': 'Electronics & Electrical',
            'Item': 'Electrical Appliances',
            'Annual_Import_Million_USD': 1000,
            'Primary_Importers': 'China, India, Thailand',
            'Current_Local_Production': 'Yes - Growing',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - Walton leading',
            'Technical_Complexity': 'Medium',
            'Investment_Needed_Million_USD': 300,
            'Potential_Local_Production_Percentage': 75,
            'Import_Reduction_Million_USD': 750,
            'Key_Companies': 'Walton, Minister, Jamuna',
            'Challenges': 'Component imports',
            'Recommendations': 'Component manufacturing, export focus'
        },
        
        # Textiles & Garments (Inputs)
        {
            'Category': 'Textile Inputs',
            'Item': 'Fabric & Yarn',
            'Annual_Import_Million_USD': 8000,
            'Primary_Importers': 'China, India, Pakistan, Turkey',
            'Current_Local_Production': 'Yes - But insufficient',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - Large textile sector',
            'Technical_Complexity': 'Medium',
            'Investment_Needed_Million_USD': 2000,
            'Potential_Local_Production_Percentage': 70,
            'Import_Reduction_Million_USD': 5600,
            'Key_Companies': 'Numerous textile mills',
            'Challenges': 'Backward linkage, cotton imports',
            'Recommendations': 'Spinning, weaving capacity expansion'
        },
        {
            'Category': 'Textile Inputs',
            'Item': 'Dyes & Chemicals',
            'Annual_Import_Million_USD': 1200,
            'Primary_Importers': 'China, India, Germany',
            'Current_Local_Production': 'Limited',
            'Local_Production_Potential': 'Medium',
            'Existing_Industry': 'Few producers',
            'Technical_Complexity': 'High',
            'Investment_Needed_Million_USD': 400,
            'Potential_Local_Production_Percentage': 40,
            'Import_Reduction_Million_USD': 480,
            'Key_Companies': 'Limited local production',
            'Challenges': 'Technology, environmental',
            'Recommendations': 'Chemical industry development'
        },
        {
            'Category': 'Textile Inputs',
            'Item': 'Accessories (Buttons, Zippers, etc.)',
            'Annual_Import_Million_USD': 800,
            'Primary_Importers': 'China, India, Taiwan',
            'Current_Local_Production': 'Yes - Growing',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - Many manufacturers',
            'Technical_Complexity': 'Low-Medium',
            'Investment_Needed_Million_USD': 150,
            'Potential_Local_Production_Percentage': 85,
            'Import_Reduction_Million_USD': 680,
            'Key_Companies': 'Numerous SMEs',
            'Challenges': 'Quality, variety',
            'Recommendations': 'Quality improvement, diversification'
        },
        
        # Paper & Packaging
        {
            'Category': 'Paper & Packaging',
            'Item': 'Paper & Paperboard',
            'Annual_Import_Million_USD': 600,
            'Primary_Importers': 'India, Indonesia, China',
            'Current_Local_Production': 'Yes',
            'Local_Production_Potential': 'High',
            'Existing_Industry': 'Yes - Several mills',
            'Technical_Complexity': 'Medium',
            'Investment_Needed_Million_USD': 200,
            'Potential_Local_Production_Percentage': 70,
            'Import_Reduction_Million_USD': 420,
            'Key_Companies': 'Bashundhara, Meghna, others',
            'Challenges': 'Raw material, technology',
            'Recommendations': 'Capacity expansion, recycling'
        },
        {
            'Category': 'Paper & Packaging',
            'Item': 'Packaging Materials',
            'Annual_Import_Million_USD': 400,
            'Primary_Importers': 'China, India, Thailand',
            'Current_Local_Production': 'Yes - Growing',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes',
            'Technical_Complexity': 'Low-Medium',
            'Investment_Needed_Million_USD': 100,
            'Potential_Local_Production_Percentage': 80,
            'Import_Reduction_Million_USD': 320,
            'Key_Companies': 'Many manufacturers',
            'Challenges': 'Quality, variety',
            'Recommendations': 'Modern equipment, standards'
        },
        
        # Construction Materials
        {
            'Category': 'Construction Materials',
            'Item': 'Cement',
            'Annual_Import_Million_USD': 300,
            'Primary_Importers': 'India, Pakistan, Vietnam',
            'Current_Local_Production': 'Yes - Excellent',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - Strong industry',
            'Technical_Complexity': 'Medium',
            'Investment_Needed_Million_USD': 50,
            'Potential_Local_Production_Percentage': 95,
            'Import_Reduction_Million_USD': 285,
            'Key_Companies': 'Heidelberg, Holcim, Shah, others',
            'Challenges': 'Clinker imports',
            'Recommendations': 'Clinker production, export focus'
        },
        {
            'Category': 'Construction Materials',
            'Item': 'Ceramic Tiles & Sanitary Ware',
            'Annual_Import_Million_USD': 400,
            'Primary_Importers': 'China, India, Spain, Italy',
            'Current_Local_Production': 'Yes - Excellent',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - World-class',
            'Technical_Complexity': 'Medium',
            'Investment_Needed_Million_USD': 100,
            'Potential_Local_Production_Percentage': 90,
            'Import_Reduction_Million_USD': 360,
            'Key_Companies': 'RAK Ceramics, Shinepukur, others',
            'Challenges': 'Premium segment',
            'Recommendations': 'Premium products, export expansion'
        },
        {
            'Category': 'Construction Materials',
            'Item': 'Glass & Glass Products',
            'Annual_Import_Million_USD': 300,
            'Primary_Importers': 'China, India, Thailand',
            'Current_Local_Production': 'Yes',
            'Local_Production_Potential': 'High',
            'Existing_Industry': 'Yes',
            'Technical_Complexity': 'Medium',
            'Investment_Needed_Million_USD': 150,
            'Potential_Local_Production_Percentage': 70,
            'Import_Reduction_Million_USD': 210,
            'Key_Companies': 'PHP Glass, others',
            'Challenges': 'Specialty glass',
            'Recommendations': 'Capacity expansion, specialty glass'
        },
        
        # Consumer Goods
        {
            'Category': 'Consumer Goods',
            'Item': 'Footwear',
            'Annual_Import_Million_USD': 500,
            'Primary_Importers': 'China, Vietnam, India',
            'Current_Local_Production': 'Yes - Good',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - Large industry',
            'Technical_Complexity': 'Low-Medium',
            'Investment_Needed_Million_USD': 100,
            'Potential_Local_Production_Percentage': 85,
            'Import_Reduction_Million_USD': 425,
            'Key_Companies': 'Bata, Apex, Bay, others',
            'Challenges': 'Premium segment, branding',
            'Recommendations': 'Quality improvement, export focus'
        },
        {
            'Category': 'Consumer Goods',
            'Item': 'Furniture',
            'Annual_Import_Million_USD': 300,
            'Primary_Importers': 'China, India, Malaysia',
            'Current_Local_Production': 'Yes - Excellent',
            'Local_Production_Potential': 'Very High',
            'Existing_Industry': 'Yes - Strong craftsmanship',
            'Technical_Complexity': 'Low-Medium',
            'Investment_Needed_Million_USD': 80,
            'Potential_Local_Production_Percentage': 90,
            'Import_Reduction_Million_USD': 270,
            'Key_Companies': 'Hatil, Otobi, Partex, others',
            'Challenges': 'Premium segment',
            'Recommendations': 'Design, branding, export'
        },
        {
            'Category': 'Consumer Goods',
            'Item': 'Toys & Sports Goods',
            'Annual_Import_Million_USD': 400,
            'Primary_Importers': 'China, India',
            'Current_Local_Production': 'Limited',
            'Local_Production_Potential': 'High',
            'Existing_Industry': 'Small scale',
            'Technical_Complexity': 'Low-Medium',
            'Investment_Needed_Million_USD': 120,
            'Potential_Local_Production_Percentage': 60,
            'Import_Reduction_Million_USD': 240,
            'Key_Companies': 'Few local producers',
            'Challenges': 'Safety standards, variety',
            'Recommendations': 'Manufacturing clusters, standards'
        },
        
        # Others
        {
            'Category': 'Others',
            'Item': 'Rubber Products (Tires, etc.)',
            'Annual_Import_Million_USD': 600,
            'Primary_Importers': 'China, India, Thailand',
            'Current_Local_Production': 'Yes',
            'Local_Production_Potential': 'High',
            'Existing_Industry': 'Yes',
            'Technical_Complexity': 'Medium',
            'Investment_Needed_Million_USD': 200,
            'Potential_Local_Production_Percentage': 70,
            'Import_Reduction_Million_USD': 420,
            'Key_Companies': 'Bata, Apex, others',
            'Challenges': 'Rubber imports, technology',
            'Recommendations': 'Capacity expansion, technology'
        }
    ]
    
    return pd.DataFrame(manufactures)

def analyze_local_production_potential(df):
    """
    Analyze local production potential
    """
    
    print("="*80)
    print("MANUFACTURES IMPORT - LOCAL PRODUCTION ANALYSIS")
    print("="*80)
    
    total_imports = df['Annual_Import_Million_USD'].sum()
    print(f"\nTotal Manufactures Imports Analyzed: ${total_imports:,.0f} million")
    print(f"Total: ${total_imports/1000:.2f} billion")
    print(f"Note: This is a subset of total manufactures imports ($40.56B)")
    
    # By category
    print("\n" + "-"*80)
    print("BY CATEGORY:")
    print("-"*80)
    
    category_summary = df.groupby('Category').agg({
        'Annual_Import_Million_USD': 'sum',
        'Import_Reduction_Million_USD': 'sum'
    }).sort_values('Annual_Import_Million_USD', ascending=False)
    
    for category, row in category_summary.iterrows():
        imports = row['Annual_Import_Million_USD']
        reduction = row['Import_Reduction_Million_USD']
        pct = (reduction / imports) * 100 if imports > 0 else 0
        print(f"{category:<30} ${imports:>8,.0f}M | Potential: ${reduction:>8,.0f}M ({pct:.0f}%)")
    
    # Total potential
    total_reduction = df['Import_Reduction_Million_USD'].sum()
    reduction_pct = (total_reduction / total_imports) * 100
    total_investment = df['Investment_Needed_Million_USD'].sum()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nCurrent Imports: ${total_imports:,.0f}M")
    print(f"Reduction Potential: ${total_reduction:,.0f}M ({reduction_pct:.1f}%)")
    print(f"Investment Needed: ${total_investment:,.0f}M")
    print(f"ROI: {total_investment/total_reduction:.1f} years")
    
    # High potential
    high_pot = df[df['Potential_Local_Production_Percentage'] >= 75]
    print(f"\nHigh Potential Items (≥75%): {len(high_pot)}")
    print(f"Value: ${high_pot['Import_Reduction_Million_USD'].sum():,.0f}M")
    
    return total_reduction, reduction_pct

def generate_report(df):
    """
    Generate report
    """
    
    output_dir = Path('analysis/manufactures_local_production')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_dir / 'manufactures_production_database.csv', index=False)
    
    high_pot = df[df['Potential_Local_Production_Percentage'] >= 75]
    high_pot.to_csv(output_dir / 'high_potential_manufactures.csv', index=False)
    
    print("\n✓ Reports saved")

if __name__ == "__main__":
    df = create_manufactures_database()
    total_red, red_pct = analyze_local_production_potential(df)
    generate_report(df)
    print("\n" + "="*80)
    print("ANALYSIS COMPLETED!")
    print("="*80)

# Made with Bob
