"""
Analyze Bangladesh Import Data
Visualize import trends by product categories from 2000 onwards
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data():
    """Load the import data"""
    print("Loading import data...")
    
    # Load raw data
    raw_df = pd.read_csv('data/raw/bangladesh_import_data.csv')
    
    # Load pivot data
    pivot_df = pd.read_csv('data/processed/bangladesh_import_pivot.csv')
    
    # Load category data
    categories_df = pd.read_csv('data/processed/bangladesh_import_categories.csv')
    
    print(f"✓ Loaded {len(raw_df)} raw records")
    print(f"✓ Loaded pivot table with {len(pivot_df)} years")
    print(f"✓ Loaded {len(categories_df)} category records")
    
    return raw_df, pivot_df, categories_df

def analyze_total_imports(pivot_df):
    """Analyze total import trends"""
    print("\n" + "="*80)
    print("TOTAL IMPORT ANALYSIS")
    print("="*80)
    
    # Clean year column
    pivot_df['Year'] = pivot_df['Year'].str.replace('YR', '').astype(int)
    
    # Get total imports column
    total_col = 'Total Merchandise Imports (current US$)'
    if total_col in pivot_df.columns:
        total_imports = pivot_df[['Year', total_col]].dropna()
        
        print(f"\nTotal Merchandise Imports (2000-2024):")
        print(f"  First year (2000): ${total_imports[total_col].iloc[0]:,.0f}")
        print(f"  Latest year: ${total_imports[total_col].iloc[-1]:,.0f}")
        print(f"  Growth: {((total_imports[total_col].iloc[-1] / total_imports[total_col].iloc[0]) - 1) * 100:.1f}%")
        print(f"  Average annual imports: ${total_imports[total_col].mean():,.0f}")
        
        return total_imports
    
    return None

def analyze_import_categories(categories_df):
    """Analyze import by product categories"""
    print("\n" + "="*80)
    print("IMPORT BY PRODUCT CATEGORY")
    print("="*80)
    
    # Get latest year data
    latest_year = categories_df['Year'].max()
    latest_data = categories_df[categories_df['Year'] == latest_year].copy()
    
    print(f"\nImport Breakdown for {latest_year}:")
    print(f"{'Category':<40} {'Value (USD)':<20} {'Percentage':<10}")
    print("-" * 70)
    
    latest_data = latest_data.sort_values('Value_USD', ascending=False)
    for _, row in latest_data.iterrows():
        print(f"{row['Category']:<40} ${row['Value_USD']:>18,.0f} {row['Percentage']:>9.1f}%")
    
    print(f"\nTotal: ${latest_data['Total_Imports_USD'].iloc[0]:,.0f}")
    
    return latest_data

def create_visualizations(pivot_df, categories_df):
    """Create comprehensive visualizations"""
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    
    # Clean year column if needed
    if pivot_df['Year'].dtype == 'object':
        pivot_df['Year'] = pivot_df['Year'].str.replace('YR', '').astype(int)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Total Imports Trend
    ax1 = plt.subplot(2, 3, 1)
    total_col = 'Total Merchandise Imports (current US$)'
    if total_col in pivot_df.columns:
        data = pivot_df[['Year', total_col]].dropna()
        ax1.plot(data['Year'], data[total_col] / 1e9, marker='o', linewidth=2, markersize=6)
        ax1.set_title('Total Merchandise Imports (2000-2024)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Year', fontsize=12)
        ax1.set_ylabel('Imports (Billion USD)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
    
    # 2. Import Categories Over Time (Stacked Area)
    ax2 = plt.subplot(2, 3, 2)
    category_pivot = categories_df.pivot_table(
        index='Year',
        columns='Category',
        values='Value_USD',
        aggfunc='sum'
    )
    category_pivot = category_pivot.div(1e9)  # Convert to billions
    
    ax2.stackplot(category_pivot.index, 
                  *[category_pivot[col] for col in category_pivot.columns],
                  labels=category_pivot.columns,
                  alpha=0.8)
    ax2.set_title('Import Categories Over Time (Stacked)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Imports (Billion USD)', fontsize=12)
    ax2.legend(loc='upper left', fontsize=8)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Latest Year Category Breakdown (Pie Chart)
    ax3 = plt.subplot(2, 3, 3)
    latest_year = categories_df['Year'].max()
    latest_data = categories_df[categories_df['Year'] == latest_year]
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(latest_data)))
    wedges, texts, autotexts = ax3.pie(
        latest_data['Value_USD'],
        labels=latest_data['Category'],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors
    )
    ax3.set_title(f'Import Categories Breakdown ({latest_year})', fontsize=14, fontweight='bold')
    for text in texts:
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(8)
    
    # 4. Category Trends (Line Chart)
    ax4 = plt.subplot(2, 3, 4)
    for category in category_pivot.columns:
        ax4.plot(category_pivot.index, category_pivot[category], 
                marker='o', label=category, linewidth=2, markersize=4)
    ax4.set_title('Import Category Trends', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Year', fontsize=12)
    ax4.set_ylabel('Imports (Billion USD)', fontsize=12)
    ax4.legend(loc='upper left', fontsize=8)
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='x', rotation=45)
    
    # 5. Import Growth Rate
    ax5 = plt.subplot(2, 3, 5)
    if total_col in pivot_df.columns:
        data = pivot_df[['Year', total_col]].dropna()
        data['Growth_Rate'] = data[total_col].pct_change() * 100
        
        colors_growth = ['green' if x > 0 else 'red' for x in data['Growth_Rate']]
        ax5.bar(data['Year'], data['Growth_Rate'], color=colors_growth, alpha=0.7)
        ax5.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax5.set_title('Year-over-Year Import Growth Rate', fontsize=14, fontweight='bold')
        ax5.set_xlabel('Year', fontsize=12)
        ax5.set_ylabel('Growth Rate (%)', fontsize=12)
        ax5.grid(True, alpha=0.3, axis='y')
        ax5.tick_params(axis='x', rotation=45)
    
    # 6. Category Percentage Trends
    ax6 = plt.subplot(2, 3, 6)
    percentage_pivot = categories_df.pivot_table(
        index='Year',
        columns='Category',
        values='Percentage',
        aggfunc='mean'
    )
    
    for category in percentage_pivot.columns:
        ax6.plot(percentage_pivot.index, percentage_pivot[category], 
                marker='o', label=category, linewidth=2, markersize=4)
    ax6.set_title('Import Category Percentages Over Time', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Year', fontsize=12)
    ax6.set_ylabel('Percentage of Total Imports (%)', fontsize=12)
    ax6.legend(loc='best', fontsize=8)
    ax6.grid(True, alpha=0.3)
    ax6.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save figure
    output_dir = Path('analysis/imports')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'import_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved to: {output_file}")
    
    plt.close()

def generate_report(pivot_df, categories_df):
    """Generate comprehensive markdown report"""
    print("\n" + "="*80)
    print("GENERATING REPORT")
    print("="*80)
    
    # Clean year column if needed
    if pivot_df['Year'].dtype == 'object':
        pivot_df['Year'] = pivot_df['Year'].str.replace('YR', '').astype(int)
    
    report = []
    report.append("# Bangladesh Import Analysis Report (2000-2024)")
    report.append("\n## Executive Summary")
    report.append("\nThis report analyzes Bangladesh's import patterns from 2000 to 2024, ")
    report.append("categorizing products and tracking spending trends over time.")
    
    # Total imports analysis
    report.append("\n## 1. Total Import Trends")
    total_col = 'Total Merchandise Imports (current US$)'
    if total_col in pivot_df.columns:
        data = pivot_df[['Year', total_col]].dropna()
        
        first_value = data[total_col].iloc[0]
        last_value = data[total_col].iloc[-1]
        growth = ((last_value / first_value) - 1) * 100
        
        report.append(f"\n- **First Year (2000)**: ${first_value:,.0f}")
        report.append(f"- **Latest Year ({data['Year'].iloc[-1]})**: ${last_value:,.0f}")
        report.append(f"- **Total Growth**: {growth:.1f}%")
        report.append(f"- **Average Annual Imports**: ${data[total_col].mean():,.0f}")
        
        # Year-by-year breakdown
        report.append("\n### Year-by-Year Import Values")
        report.append("\n| Year | Total Imports (USD) | Growth Rate (%) |")
        report.append("|------|---------------------|-----------------|")
        
        for i, row in data.iterrows():
            year = row['Year']
            value = row[total_col]
            if i > 0:
                prev_value = data[total_col].iloc[i-1]
                growth_rate = ((value / prev_value) - 1) * 100
                report.append(f"| {year} | ${value:,.0f} | {growth_rate:+.1f}% |")
            else:
                report.append(f"| {year} | ${value:,.0f} | - |")
    
    # Category analysis
    report.append("\n## 2. Import by Product Category")
    
    latest_year = categories_df['Year'].max()
    latest_data = categories_df[categories_df['Year'] == latest_year].copy()
    latest_data = latest_data.sort_values('Value_USD', ascending=False)
    
    report.append(f"\n### Latest Year Breakdown ({latest_year})")
    report.append("\n| Category | Value (USD) | Percentage |")
    report.append("|----------|-------------|------------|")
    
    for _, row in latest_data.iterrows():
        report.append(f"| {row['Category']} | ${row['Value_USD']:,.0f} | {row['Percentage']:.1f}% |")
    
    report.append(f"\n**Total Imports**: ${latest_data['Total_Imports_USD'].iloc[0]:,.0f}")
    
    # Category trends
    report.append("\n### Category Trends Over Time")
    
    for category in categories_df['Category'].unique():
        cat_data = categories_df[categories_df['Category'] == category].sort_values('Year')
        
        if len(cat_data) > 0:
            first_val = cat_data['Value_USD'].iloc[0]
            last_val = cat_data['Value_USD'].iloc[-1]
            cat_growth = ((last_val / first_val) - 1) * 100
            
            report.append(f"\n#### {category}")
            report.append(f"- First Year Value: ${first_val:,.0f}")
            report.append(f"- Latest Year Value: ${last_val:,.0f}")
            report.append(f"- Growth: {cat_growth:+.1f}%")
    
    # Key insights
    report.append("\n## 3. Key Insights")
    
    # Find fastest growing category
    category_growth = {}
    for category in categories_df['Category'].unique():
        cat_data = categories_df[categories_df['Category'] == category].sort_values('Year')
        if len(cat_data) > 1:
            first_val = cat_data['Value_USD'].iloc[0]
            last_val = cat_data['Value_USD'].iloc[-1]
            growth = ((last_val / first_val) - 1) * 100
            category_growth[category] = growth
    
    if category_growth:
        fastest = max(category_growth, key=category_growth.get)
        slowest = min(category_growth, key=category_growth.get)
        
        report.append(f"\n- **Fastest Growing Category**: {fastest} ({category_growth[fastest]:+.1f}%)")
        report.append(f"- **Slowest Growing Category**: {slowest} ({category_growth[slowest]:+.1f}%)")
    
    # Largest category
    report.append(f"\n- **Largest Import Category ({latest_year})**: {latest_data.iloc[0]['Category']} ")
    report.append(f"(${latest_data.iloc[0]['Value_USD']:,.0f}, {latest_data.iloc[0]['Percentage']:.1f}%)")
    
    report.append("\n## 4. Visualizations")
    report.append("\n![Import Analysis](figures/import_analysis.png)")
    
    report.append("\n## 5. Data Sources")
    report.append("\n- World Bank Open Data API")
    report.append("- Indicators: Merchandise imports by product category")
    report.append("- Time Period: 2000-2024")
    
    # Save report
    output_dir = Path('analysis/imports')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create figures subdirectory
    figures_dir = output_dir / 'figures'
    figures_dir.mkdir(exist_ok=True)
    
    report_file = output_dir / 'bangladesh_import_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"✓ Report saved to: {report_file}")
    
    # Also save detailed category data
    categories_df.to_csv(output_dir / 'import_categories_detailed.csv', index=False)
    print(f"✓ Detailed category data saved to: {output_dir / 'import_categories_detailed.csv'}")

if __name__ == "__main__":
    print("="*80)
    print("BANGLADESH IMPORT DATA ANALYSIS")
    print("="*80)
    
    # Load data
    raw_df, pivot_df, categories_df = load_data()
    
    # Analyze total imports
    total_imports = analyze_total_imports(pivot_df)
    
    # Analyze categories
    latest_data = analyze_import_categories(categories_df)
    
    # Create visualizations
    create_visualizations(pivot_df, categories_df)
    
    # Generate report
    generate_report(pivot_df, categories_df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nOutput files:")
    print("  - analysis/imports/bangladesh_import_report.md")
    print("  - analysis/imports/figures/import_analysis.png")
    print("  - analysis/imports/import_categories_detailed.csv")

# Made with Bob
