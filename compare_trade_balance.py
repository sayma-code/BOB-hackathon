"""
Compare Bangladesh Import vs Export Data
Analyze trade balance and identify gaps by product categories
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

def load_trade_data():
    """Load both import and export data"""
    print("Loading trade data...")
    
    # Load import data
    import_categories = pd.read_csv('data/processed/bangladesh_import_categories.csv')
    import_pivot = pd.read_csv('data/processed/bangladesh_import_pivot.csv')
    
    # Load export data
    export_categories = pd.read_csv('data/processed/bangladesh_export_categories.csv')
    export_pivot = pd.read_csv('data/processed/bangladesh_export_pivot.csv')
    
    print(f"✓ Loaded {len(import_categories)} import category records")
    print(f"✓ Loaded {len(export_categories)} export category records")
    
    return import_categories, export_categories, import_pivot, export_pivot

def calculate_trade_balance(import_cat, export_cat):
    """Calculate trade balance by category"""
    print("\n" + "="*80)
    print("CALCULATING TRADE BALANCE")
    print("="*80)
    
    # Merge import and export data
    trade_balance = []
    
    # Get all unique years and categories
    years = sorted(set(import_cat['Year'].unique()) & set(export_cat['Year'].unique()))
    categories = sorted(set(import_cat['Category'].unique()) & set(export_cat['Category'].unique()))
    
    for year in years:
        year_import = import_cat[import_cat['Year'] == year]
        year_export = export_cat[export_cat['Year'] == year]
        
        # Get total trade values
        if len(year_import) > 0:
            total_imports = year_import['Total_Imports_USD'].iloc[0]
        else:
            total_imports = 0
            
        if len(year_export) > 0:
            total_exports = year_export['Total_Exports_USD'].iloc[0]
        else:
            total_exports = 0
        
        trade_deficit = total_imports - total_exports
        
        for category in categories:
            cat_import = year_import[year_import['Category'] == category]
            cat_export = year_export[year_export['Category'] == category]
            
            import_value = cat_import['Value_USD'].iloc[0] if len(cat_import) > 0 else 0
            export_value = cat_export['Value_USD'].iloc[0] if len(cat_export) > 0 else 0
            
            balance = export_value - import_value  # Positive = surplus, Negative = deficit
            
            trade_balance.append({
                'Year': year,
                'Category': category,
                'Import_Value': import_value,
                'Export_Value': export_value,
                'Trade_Balance': balance,
                'Trade_Deficit': abs(balance) if balance < 0 else 0,
                'Trade_Surplus': balance if balance > 0 else 0,
                'Total_Imports': total_imports,
                'Total_Exports': total_exports,
                'Overall_Trade_Balance': total_exports - total_imports
            })
    
    balance_df = pd.DataFrame(trade_balance)
    
    # Save trade balance data
    output_file = 'data/processed/bangladesh_trade_balance.csv'
    balance_df.to_csv(output_file, index=False)
    print(f"✓ Trade balance data saved to: {output_file}")
    
    return balance_df

def analyze_trade_gaps(balance_df):
    """Analyze trade gaps by category"""
    print("\n" + "="*80)
    print("TRADE GAP ANALYSIS")
    print("="*80)
    
    # Get latest year
    latest_year = balance_df['Year'].max()
    latest_data = balance_df[balance_df['Year'] == latest_year].copy()
    
    print(f"\nTrade Balance Analysis for {latest_year}:")
    print(f"{'Category':<40} {'Imports (USD)':<20} {'Exports (USD)':<20} {'Balance (USD)':<20} {'Status':<10}")
    print("-" * 110)
    
    latest_data = latest_data.sort_values('Trade_Deficit', ascending=False)
    
    for _, row in latest_data.iterrows():
        status = "DEFICIT" if row['Trade_Balance'] < 0 else "SURPLUS"
        print(f"{row['Category']:<40} ${row['Import_Value']:>18,.0f} ${row['Export_Value']:>18,.0f} ${row['Trade_Balance']:>18,.0f} {status:<10}")
    
    total_imports = latest_data['Total_Imports'].iloc[0]
    total_exports = latest_data['Total_Exports'].iloc[0]
    overall_deficit = total_imports - total_exports
    
    print("\n" + "="*110)
    print(f"{'TOTAL':<40} ${total_imports:>18,.0f} ${total_exports:>18,.0f} ${-overall_deficit:>18,.0f} {'DEFICIT':<10}")
    print("="*110)
    
    # Calculate percentages
    print(f"\nOverall Trade Deficit: ${overall_deficit:,.0f}")
    print(f"Export/Import Ratio: {(total_exports/total_imports)*100:.1f}%")
    print(f"Trade Coverage: Exports cover {(total_exports/total_imports)*100:.1f}% of imports")
    
    return latest_data

def create_comparison_visualizations(balance_df):
    """Create comprehensive trade comparison visualizations"""
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Overall Trade Balance Over Time
    ax1 = plt.subplot(3, 3, 1)
    yearly_balance = balance_df.groupby('Year').agg({
        'Total_Imports': 'first',
        'Total_Exports': 'first',
        'Overall_Trade_Balance': 'first'
    }).reset_index()
    
    ax1.plot(yearly_balance['Year'], yearly_balance['Total_Imports']/1e9, 
             marker='o', label='Imports', linewidth=2, color='red')
    ax1.plot(yearly_balance['Year'], yearly_balance['Total_Exports']/1e9, 
             marker='s', label='Exports', linewidth=2, color='green')
    ax1.fill_between(yearly_balance['Year'], 
                      yearly_balance['Total_Imports']/1e9,
                      yearly_balance['Total_Exports']/1e9,
                      alpha=0.3, color='orange', label='Trade Deficit')
    ax1.set_title('Total Imports vs Exports (2000-2024)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Value (Billion USD)', fontsize=12)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Trade Deficit Over Time
    ax2 = plt.subplot(3, 3, 2)
    trade_deficit = (yearly_balance['Total_Imports'] - yearly_balance['Total_Exports']) / 1e9
    colors_deficit = ['red' if x > 0 else 'green' for x in trade_deficit]
    ax2.bar(yearly_balance['Year'], trade_deficit, color=colors_deficit, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_title('Trade Deficit/Surplus Over Time', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Deficit (Billion USD)', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Export/Import Ratio Over Time
    ax3 = plt.subplot(3, 3, 3)
    export_import_ratio = (yearly_balance['Total_Exports'] / yearly_balance['Total_Imports']) * 100
    ax3.plot(yearly_balance['Year'], export_import_ratio, marker='o', linewidth=2, color='purple')
    ax3.axhline(y=100, color='green', linestyle='--', linewidth=1, label='Break-even (100%)')
    ax3.fill_between(yearly_balance['Year'], export_import_ratio, 100, 
                      where=(export_import_ratio < 100), alpha=0.3, color='red', label='Deficit Zone')
    ax3.set_title('Export/Import Coverage Ratio', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Year', fontsize=12)
    ax3.set_ylabel('Coverage (%)', fontsize=12)
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. Category-wise Trade Balance (Latest Year)
    ax4 = plt.subplot(3, 3, 4)
    latest_year = balance_df['Year'].max()
    latest_data = balance_df[balance_df['Year'] == latest_year].sort_values('Trade_Balance')
    
    colors_cat = ['red' if x < 0 else 'green' for x in latest_data['Trade_Balance']]
    ax4.barh(latest_data['Category'], latest_data['Trade_Balance']/1e9, color=colors_cat, alpha=0.7)
    ax4.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax4.set_title(f'Trade Balance by Category ({latest_year})', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Balance (Billion USD)', fontsize=12)
    ax4.set_ylabel('Category', fontsize=12)
    ax4.grid(True, alpha=0.3, axis='x')
    
    # 5. Import vs Export by Category (Latest Year)
    ax5 = plt.subplot(3, 3, 5)
    x = np.arange(len(latest_data))
    width = 0.35
    
    ax5.bar(x - width/2, latest_data['Import_Value']/1e9, width, label='Imports', color='red', alpha=0.7)
    ax5.bar(x + width/2, latest_data['Export_Value']/1e9, width, label='Exports', color='green', alpha=0.7)
    ax5.set_title(f'Imports vs Exports by Category ({latest_year})', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Category', fontsize=12)
    ax5.set_ylabel('Value (Billion USD)', fontsize=12)
    ax5.set_xticks(x)
    ax5.set_xticklabels(latest_data['Category'], rotation=45, ha='right')
    ax5.legend()
    ax5.grid(True, alpha=0.3, axis='y')
    
    # 6. Trade Deficit by Category Over Time (Stacked)
    ax6 = plt.subplot(3, 3, 6)
    deficit_pivot = balance_df[balance_df['Trade_Balance'] < 0].pivot_table(
        index='Year',
        columns='Category',
        values='Trade_Deficit',
        aggfunc='sum',
        fill_value=0
    )
    deficit_pivot = deficit_pivot.div(1e9)
    
    ax6.stackplot(deficit_pivot.index, 
                  *[deficit_pivot[col] for col in deficit_pivot.columns],
                  labels=deficit_pivot.columns,
                  alpha=0.8)
    ax6.set_title('Trade Deficit by Category Over Time', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Year', fontsize=12)
    ax6.set_ylabel('Deficit (Billion USD)', fontsize=12)
    ax6.legend(loc='upper left', fontsize=8)
    ax6.grid(True, alpha=0.3)
    ax6.tick_params(axis='x', rotation=45)
    
    # 7. Manufactures Trade Balance
    ax7 = plt.subplot(3, 3, 7)
    manuf_data = balance_df[balance_df['Category'] == 'Manufactures']
    ax7.plot(manuf_data['Year'], manuf_data['Import_Value']/1e9, 
             marker='o', label='Imports', linewidth=2, color='red')
    ax7.plot(manuf_data['Year'], manuf_data['Export_Value']/1e9, 
             marker='s', label='Exports', linewidth=2, color='green')
    ax7.set_title('Manufactures: Imports vs Exports', fontsize=14, fontweight='bold')
    ax7.set_xlabel('Year', fontsize=12)
    ax7.set_ylabel('Value (Billion USD)', fontsize=12)
    ax7.legend()
    ax7.grid(True, alpha=0.3)
    ax7.tick_params(axis='x', rotation=45)
    
    # 8. Food Trade Balance
    ax8 = plt.subplot(3, 3, 8)
    food_data = balance_df[balance_df['Category'] == 'Food']
    ax8.plot(food_data['Year'], food_data['Import_Value']/1e9, 
             marker='o', label='Imports', linewidth=2, color='red')
    ax8.plot(food_data['Year'], food_data['Export_Value']/1e9, 
             marker='s', label='Exports', linewidth=2, color='green')
    ax8.set_title('Food: Imports vs Exports', fontsize=14, fontweight='bold')
    ax8.set_xlabel('Year', fontsize=12)
    ax8.set_ylabel('Value (Billion USD)', fontsize=12)
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    ax8.tick_params(axis='x', rotation=45)
    
    # 9. Fuel Trade Balance
    ax9 = plt.subplot(3, 3, 9)
    fuel_data = balance_df[balance_df['Category'] == 'Fuel']
    ax9.plot(fuel_data['Year'], fuel_data['Import_Value']/1e9, 
             marker='o', label='Imports', linewidth=2, color='red')
    ax9.plot(fuel_data['Year'], fuel_data['Export_Value']/1e9, 
             marker='s', label='Exports', linewidth=2, color='green')
    ax9.set_title('Fuel: Imports vs Exports', fontsize=14, fontweight='bold')
    ax9.set_xlabel('Year', fontsize=12)
    ax9.set_ylabel('Value (Billion USD)', fontsize=12)
    ax9.legend()
    ax9.grid(True, alpha=0.3)
    ax9.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save figure
    output_dir = Path('analysis/trade_balance')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'trade_balance_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved to: {output_file}")
    
    plt.close()

def generate_comparison_report(balance_df):
    """Generate comprehensive trade balance report"""
    print("\n" + "="*80)
    print("GENERATING REPORT")
    print("="*80)
    
    report = []
    report.append("# Bangladesh Trade Balance Analysis Report (2000-2024)")
    report.append("\n## Executive Summary")
    report.append("\nThis report analyzes Bangladesh's trade balance by comparing imports and exports,")
    report.append("identifying trade gaps and deficits by product categories over time.")
    
    # Overall trade balance
    report.append("\n## 1. Overall Trade Balance")
    
    latest_year = balance_df['Year'].max()
    latest_total = balance_df[balance_df['Year'] == latest_year].iloc[0]
    first_year = balance_df['Year'].min()
    first_total = balance_df[balance_df['Year'] == first_year].iloc[0]
    
    report.append(f"\n### Latest Year ({latest_year}):")
    report.append(f"- **Total Imports**: ${latest_total['Total_Imports']:,.0f}")
    report.append(f"- **Total Exports**: ${latest_total['Total_Exports']:,.0f}")
    report.append(f"- **Trade Deficit**: ${latest_total['Total_Imports'] - latest_total['Total_Exports']:,.0f}")
    report.append(f"- **Export/Import Ratio**: {(latest_total['Total_Exports']/latest_total['Total_Imports'])*100:.1f}%")
    
    report.append(f"\n### First Year ({first_year}):")
    report.append(f"- **Total Imports**: ${first_total['Total_Imports']:,.0f}")
    report.append(f"- **Total Exports**: ${first_total['Total_Exports']:,.0f}")
    report.append(f"- **Trade Deficit**: ${first_total['Total_Imports'] - first_total['Total_Exports']:,.0f}")
    
    # Trade balance by category
    report.append("\n## 2. Trade Balance by Product Category")
    
    latest_data = balance_df[balance_df['Year'] == latest_year].sort_values('Trade_Deficit', ascending=False)
    
    report.append(f"\n### {latest_year} Category Breakdown")
    report.append("\n| Category | Imports (USD) | Exports (USD) | Balance (USD) | Status |")
    report.append("|----------|---------------|---------------|---------------|--------|")
    
    for _, row in latest_data.iterrows():
        status = "DEFICIT ❌" if row['Trade_Balance'] < 0 else "SURPLUS ✓"
        report.append(f"| {row['Category']} | ${row['Import_Value']:,.0f} | ${row['Export_Value']:,.0f} | ${row['Trade_Balance']:,.0f} | {status} |")
    
    # Biggest deficits
    report.append("\n### Largest Trade Deficits by Category")
    
    top_deficits = latest_data.nlargest(5, 'Trade_Deficit')
    for i, (_, row) in enumerate(top_deficits.iterrows(), 1):
        deficit_pct = (row['Trade_Deficit'] / (latest_total['Total_Imports'] - latest_total['Total_Exports'])) * 100
        report.append(f"\n{i}. **{row['Category']}**")
        report.append(f"   - Deficit: ${row['Trade_Deficit']:,.0f}")
        report.append(f"   - Imports: ${row['Import_Value']:,.0f}")
        report.append(f"   - Exports: ${row['Export_Value']:,.0f}")
        report.append(f"   - Contribution to total deficit: {deficit_pct:.1f}%")
    
    # Historical trends
    report.append("\n## 3. Historical Trade Balance Trends")
    
    yearly_summary = balance_df.groupby('Year').agg({
        'Total_Imports': 'first',
        'Total_Exports': 'first',
        'Overall_Trade_Balance': 'first'
    }).reset_index()
    
    report.append("\n| Year | Imports (USD) | Exports (USD) | Trade Balance (USD) | Coverage (%) |")
    report.append("|------|---------------|---------------|---------------------|--------------|")
    
    for _, row in yearly_summary.iterrows():
        coverage = (row['Total_Exports'] / row['Total_Imports']) * 100
        report.append(f"| {row['Year']} | ${row['Total_Imports']:,.0f} | ${row['Total_Exports']:,.0f} | ${row['Overall_Trade_Balance']:,.0f} | {coverage:.1f}% |")
    
    # Key insights
    report.append("\n## 4. Key Insights")
    
    avg_deficit = yearly_summary['Overall_Trade_Balance'].mean()
    worst_deficit_year = yearly_summary.loc[yearly_summary['Overall_Trade_Balance'].idxmin()]
    best_year = yearly_summary.loc[yearly_summary['Overall_Trade_Balance'].idxmax()]
    
    report.append(f"\n- **Average Annual Trade Deficit**: ${abs(avg_deficit):,.0f}")
    report.append(f"- **Worst Deficit Year**: {worst_deficit_year['Year']} (${abs(worst_deficit_year['Overall_Trade_Balance']):,.0f})")
    report.append(f"- **Best Year**: {best_year['Year']} (${abs(best_year['Overall_Trade_Balance']):,.0f})")
    
    # Category-specific insights
    report.append("\n### Category-Specific Observations:")
    
    for category in balance_df['Category'].unique():
        cat_data = balance_df[balance_df['Category'] == category]
        latest_cat = cat_data[cat_data['Year'] == latest_year].iloc[0]
        
        if latest_cat['Trade_Balance'] < 0:
            report.append(f"\n- **{category}**: Persistent deficit of ${abs(latest_cat['Trade_Balance']):,.0f}")
            report.append(f"  - Bangladesh imports {latest_cat['Import_Value']/latest_cat['Export_Value']:.1f}x more than it exports")
        else:
            report.append(f"\n- **{category}**: Surplus of ${latest_cat['Trade_Balance']:,.0f}")
    
    report.append("\n## 5. Visualizations")
    report.append("\n![Trade Balance Analysis](figures/trade_balance_analysis.png)")
    
    report.append("\n## 6. Data Sources")
    report.append("\n- World Bank Open Data API")
    report.append("- Import and Export data by product category")
    report.append("- Time Period: 2000-2024")
    
    # Save report
    output_dir = Path('analysis/trade_balance')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create figures subdirectory
    figures_dir = output_dir / 'figures'
    figures_dir.mkdir(exist_ok=True)
    
    report_file = output_dir / 'trade_balance_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"✓ Report saved to: {report_file}")

if __name__ == "__main__":
    print("="*80)
    print("BANGLADESH TRADE BALANCE ANALYSIS")
    print("="*80)
    
    # Load data
    import_cat, export_cat, import_pivot, export_pivot = load_trade_data()
    
    # Calculate trade balance
    balance_df = calculate_trade_balance(import_cat, export_cat)
    
    # Analyze trade gaps
    latest_analysis = analyze_trade_gaps(balance_df)
    
    # Create visualizations
    create_comparison_visualizations(balance_df)
    
    # Generate report
    generate_comparison_report(balance_df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nOutput files:")
    print("  - analysis/trade_balance/trade_balance_report.md")
    print("  - analysis/trade_balance/figures/trade_balance_analysis.png")
    print("  - data/processed/bangladesh_trade_balance.csv")

# Made with Bob
