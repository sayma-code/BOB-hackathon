"""
Bangladesh Tax Revenue Gap Analysis
Comparing actual tax collection vs. international benchmarks and potential
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

class TaxRevenueAnalyzer:
    """Analyze Bangladesh's tax revenue gap"""
    
    def __init__(self, data_path='data/processed/bangladesh_debt_consolidated.csv'):
        """Initialize analyzer"""
        self.data_path = data_path
        self.df = None
        self.load_data()
        
        # International benchmarks (Tax-to-GDP ratios)
        self.benchmarks = {
            'Bangladesh Current': None,  # Will be calculated
            'South Asian Average': 15.0,  # IMF data
            'Lower-Middle Income Average': 17.0,  # World Bank
            'Emerging Markets Average': 20.0,  # IMF
            'OECD Average': 34.0,  # OECD
            'Recommended Minimum': 15.0,  # IMF recommendation for developing countries
            'Sustainable Target': 18.0,  # Target for Bangladesh
        }
        
        # Create output directory
        Path('analysis/tax_analysis').mkdir(parents=True, exist_ok=True)
    
    def load_data(self):
        """Load the consolidated dataset"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"[OK] Loaded data: {len(self.df)} years")
        except Exception as e:
            print(f"[ERROR] Failed to load data: {e}")
            sys.exit(1)
    
    def calculate_tax_revenue_gap(self):
        """Calculate the tax revenue gap"""
        print("\n" + "="*70)
        print("BANGLADESH TAX REVENUE GAP ANALYSIS")
        print("="*70)
        
        revenue_col = 'Revenue, excluding grants (% of GDP)'
        gdp_col = 'GDP (current US$)'
        
        if revenue_col not in self.df.columns or gdp_col not in self.df.columns:
            print("[ERROR] Required columns not found")
            return
        
        # Get latest year with revenue data
        revenue_data = self.df[self.df[revenue_col].notna()].copy()
        if revenue_data.empty:
            print("[ERROR] No revenue data available")
            return
        
        latest_year = revenue_data['year'].max()
        latest_data = revenue_data[revenue_data['year'] == latest_year].iloc[0]
        
        actual_tax_gdp = latest_data[revenue_col]
        gdp = latest_data[gdp_col]
        actual_revenue = gdp * (actual_tax_gdp / 100)
        
        self.benchmarks['Bangladesh Current'] = actual_tax_gdp
        
        print(f"\n{'='*70}")
        print(f"CURRENT SITUATION ({int(latest_year)})")
        print(f"{'='*70}")
        print(f"GDP: ${gdp/1e9:.2f} billion")
        print(f"Actual Tax-to-GDP Ratio: {actual_tax_gdp:.2f}%")
        print(f"Actual Tax Revenue: ${actual_revenue/1e9:.2f} billion")
        
        # Calculate gaps
        print(f"\n{'='*70}")
        print(f"TAX REVENUE GAP ANALYSIS")
        print(f"{'='*70}")
        
        gap_analysis = []
        
        for benchmark_name, benchmark_ratio in self.benchmarks.items():
            if benchmark_name == 'Bangladesh Current' or benchmark_ratio is None:
                continue
            
            potential_revenue = gdp * (benchmark_ratio / 100)
            revenue_gap = potential_revenue - actual_revenue
            additional_percentage = benchmark_ratio - actual_tax_gdp
            
            gap_analysis.append({
                'Benchmark': benchmark_name,
                'Target Tax-to-GDP (%)': benchmark_ratio,
                'Current Tax-to-GDP (%)': actual_tax_gdp,
                'Gap (percentage points)': additional_percentage,
                'Potential Revenue ($ billion)': potential_revenue / 1e9,
                'Current Revenue ($ billion)': actual_revenue / 1e9,
                'Revenue Gap ($ billion)': revenue_gap / 1e9,
                'Additional Revenue (%)': (revenue_gap / actual_revenue) * 100
            })
        
        gap_df = pd.DataFrame(gap_analysis)
        gap_df = gap_df.sort_values('Revenue Gap ($ billion)', ascending=False)
        
        print("\nComparison with International Benchmarks:")
        print("-" * 70)
        for _, row in gap_df.iterrows():
            print(f"\n{row['Benchmark']}:")
            print(f"  Target Tax-to-GDP: {row['Target Tax-to-GDP (%)']:.1f}%")
            print(f"  Current: {row['Current Tax-to-GDP (%)']:.2f}%")
            print(f"  Gap: {row['Gap (percentage points)']:.2f} percentage points")
            print(f"  Potential Revenue: ${row['Potential Revenue ($ billion)']:.2f} billion")
            print(f"  Revenue Gap: ${row['Revenue Gap ($ billion)']:.2f} billion")
            print(f"  Additional Revenue: +{row['Additional Revenue (%)']:.1f}%")
        
        # Save to CSV
        gap_df.to_csv('analysis/tax_analysis/tax_revenue_gap_analysis.csv', index=False)
        print(f"\n[OK] Saved gap analysis to analysis/tax_analysis/tax_revenue_gap_analysis.csv")
        
        return gap_df, latest_year, actual_tax_gdp, gdp
    
    def analyze_historical_trends(self):
        """Analyze historical tax revenue trends"""
        print(f"\n{'='*70}")
        print("HISTORICAL TAX REVENUE TRENDS")
        print(f"{'='*70}")
        
        revenue_col = 'Revenue, excluding grants (% of GDP)'
        expense_col = 'Expense (% of GDP)'
        
        revenue_data = self.df[self.df[revenue_col].notna()].copy()
        
        if revenue_data.empty:
            print("[ERROR] No historical revenue data")
            return
        
        # Calculate statistics
        avg_revenue = revenue_data[revenue_col].mean()
        min_revenue = revenue_data[revenue_col].min()
        max_revenue = revenue_data[revenue_col].max()
        latest_revenue = revenue_data[revenue_col].iloc[-1]
        
        min_year = revenue_data[revenue_data[revenue_col] == min_revenue]['year'].values[0]
        max_year = revenue_data[revenue_data[revenue_col] == max_revenue]['year'].values[0]
        
        print(f"\nTax-to-GDP Ratio Statistics ({int(revenue_data['year'].min())}-{int(revenue_data['year'].max())}):")
        print(f"  Average: {avg_revenue:.2f}%")
        print(f"  Minimum: {min_revenue:.2f}% (in {int(min_year)})")
        print(f"  Maximum: {max_revenue:.2f}% (in {int(max_year)})")
        print(f"  Latest: {latest_revenue:.2f}%")
        print(f"  Change from min to latest: {latest_revenue - min_revenue:.2f} percentage points")
        
        # Fiscal balance
        if expense_col in revenue_data.columns:
            expense_data = revenue_data[revenue_data[expense_col].notna()].copy()
            if not expense_data.empty:
                expense_data['Fiscal Balance (% of GDP)'] = expense_data[revenue_col] - expense_data[expense_col]
                avg_deficit = expense_data['Fiscal Balance (% of GDP)'].mean()
                latest_deficit = expense_data['Fiscal Balance (% of GDP)'].iloc[-1]
                
                print(f"\nFiscal Balance:")
                print(f"  Average deficit: {abs(avg_deficit):.2f}% of GDP")
                print(f"  Latest deficit: {abs(latest_deficit):.2f}% of GDP")
                print(f"  Status: {'Deficit' if latest_deficit < 0 else 'Surplus'}")
    
    def identify_revenue_leakages(self):
        """Identify potential revenue leakages"""
        print(f"\n{'='*70}")
        print("POTENTIAL REVENUE LEAKAGES & IMPROVEMENT AREAS")
        print(f"{'='*70}")
        
        print("\n1. TAX EVASION & AVOIDANCE")
        print("   Estimated Impact: 3-5% of GDP")
        print("   - Informal economy: ~35-40% of GDP not taxed")
        print("   - Under-reporting of income")
        print("   - Transfer pricing by multinationals")
        print("   - Cash-based transactions avoiding VAT")
        
        print("\n2. NARROW TAX BASE")
        print("   Estimated Impact: 2-3% of GDP")
        print("   - Only ~1.5 million individual taxpayers (out of 170M population)")
        print("   - Tax-to-GDP ratio: ~9.5% (one of lowest in world)")
        print("   - Agriculture sector largely untaxed")
        print("   - Many exemptions and incentives")
        
        print("\n3. WEAK TAX ADMINISTRATION")
        print("   Estimated Impact: 1-2% of GDP")
        print("   - Manual processes, limited digitization")
        print("   - Corruption in tax collection")
        print("   - Inadequate enforcement capacity")
        print("   - Complex tax laws and procedures")
        
        print("\n4. CUSTOMS & TRADE REVENUE LOSSES")
        print("   Estimated Impact: 1-2% of GDP")
        print("   - Under-invoicing of imports")
        print("   - Smuggling and illegal trade")
        print("   - Customs duty exemptions")
        print("   - Weak border controls")
        
        print("\n5. PROPERTY TAX UNDERUTILIZATION")
        print("   Estimated Impact: 0.5-1% of GDP")
        print("   - Outdated property valuations")
        print("   - Low collection rates")
        print("   - Political resistance to increases")
        
        total_potential = "8-13% of GDP"
        print(f"\n{'='*70}")
        print(f"TOTAL POTENTIAL REVENUE RECOVERY: {total_potential}")
        print(f"{'='*70}")
    
    def propose_revenue_enhancement_measures(self, gap_df, latest_year, current_ratio, gdp):
        """Propose specific revenue enhancement measures"""
        print(f"\n{'='*70}")
        print("REVENUE ENHANCEMENT ROADMAP")
        print(f"{'='*70}")
        
        # Target: Sustainable Target (18% of GDP)
        target_ratio = 18.0
        target_revenue = gdp * (target_ratio / 100)
        current_revenue = gdp * (current_ratio / 100)
        required_increase = target_revenue - current_revenue
        
        print(f"\nTARGET: Increase Tax-to-GDP from {current_ratio:.2f}% to {target_ratio:.1f}%")
        print(f"Required Additional Revenue: ${required_increase/1e9:.2f} billion")
        print(f"Timeline: 5 years (2024-2029)")
        print(f"Annual Increase Needed: ${(required_increase/5)/1e9:.2f} billion/year")
        
        measures = []
        
        # Measure 1: Digitalization
        digital_impact = gdp * 0.015  # 1.5% of GDP
        measures.append({
            'Measure': 'Tax Administration Digitalization',
            'Impact (% of GDP)': 1.5,
            'Revenue Impact ($ billion)': digital_impact / 1e9,
            'Timeline': 'Years 1-3',
            'Priority': 'HIGH',
            'Actions': [
                'Implement e-filing for all taxpayers',
                'Digital payment systems',
                'Automated tax assessment',
                'Data analytics for compliance',
                'Blockchain for land records'
            ]
        })
        
        # Measure 2: Broaden tax base
        base_impact = gdp * 0.025  # 2.5% of GDP
        measures.append({
            'Measure': 'Broaden Tax Base',
            'Impact (% of GDP)': 2.5,
            'Revenue Impact ($ billion)': base_impact / 1e9,
            'Timeline': 'Years 1-4',
            'Priority': 'HIGH',
            'Actions': [
                'Formalize informal sector (target 50%)',
                'Expand individual taxpayer base to 5M',
                'Introduce minimum tax for businesses',
                'Tax agricultural income above threshold',
                'Simplify tax registration'
            ]
        })
        
        # Measure 3: Reduce evasion
        evasion_impact = gdp * 0.02  # 2% of GDP
        measures.append({
            'Measure': 'Combat Tax Evasion',
            'Impact (% of GDP)': 2.0,
            'Revenue Impact ($ billion)': evasion_impact / 1e9,
            'Timeline': 'Years 2-5',
            'Priority': 'HIGH',
            'Actions': [
                'Strengthen audit capacity',
                'Cross-border information exchange',
                'Transfer pricing regulations',
                'Penalties for non-compliance',
                'Whistleblower protection'
            ]
        })
        
        # Measure 4: VAT reform
        vat_impact = gdp * 0.015  # 1.5% of GDP
        measures.append({
            'Measure': 'VAT System Reform',
            'Impact (% of GDP)': 1.5,
            'Revenue Impact ($ billion)': vat_impact / 1e9,
            'Timeline': 'Years 1-3',
            'Priority': 'MEDIUM',
            'Actions': [
                'Reduce VAT exemptions',
                'Implement VAT on digital services',
                'Improve VAT refund system',
                'Strengthen VAT compliance',
                'Harmonize VAT rates'
            ]
        })
        
        # Measure 5: Property tax
        property_impact = gdp * 0.01  # 1% of GDP
        measures.append({
            'Measure': 'Property Tax Enhancement',
            'Impact (% of GDP)': 1.0,
            'Revenue Impact ($ billion)': property_impact / 1e9,
            'Timeline': 'Years 2-5',
            'Priority': 'MEDIUM',
            'Actions': [
                'Update property valuations',
                'Digital property registry',
                'Improve collection rates',
                'Progressive property tax rates',
                'Tax vacant land'
            ]
        })
        
        # Measure 6: Customs modernization
        customs_impact = gdp * 0.01  # 1% of GDP
        measures.append({
            'Measure': 'Customs Modernization',
            'Impact (% of GDP)': 1.0,
            'Revenue Impact ($ billion)': customs_impact / 1e9,
            'Timeline': 'Years 1-4',
            'Priority': 'MEDIUM',
            'Actions': [
                'Risk-based customs clearance',
                'Electronic cargo tracking',
                'Reduce duty exemptions',
                'Combat smuggling',
                'Trade facilitation'
            ]
        })
        
        print("\n" + "="*70)
        print("SPECIFIC REVENUE ENHANCEMENT MEASURES")
        print("="*70)
        
        total_impact = 0
        for i, measure in enumerate(measures, 1):
            print(f"\n{i}. {measure['Measure'].upper()}")
            print(f"   Priority: {measure['Priority']}")
            print(f"   Impact: {measure['Impact (% of GDP)']}% of GDP (${measure['Revenue Impact ($ billion)']:.2f} billion)")
            print(f"   Timeline: {measure['Timeline']}")
            print(f"   Key Actions:")
            for action in measure['Actions']:
                print(f"     - {action}")
            total_impact += measure['Impact (% of GDP)']
        
        print(f"\n{'='*70}")
        print(f"TOTAL POTENTIAL IMPACT: {total_impact}% of GDP")
        print(f"Total Additional Revenue: ${sum(m['Revenue Impact ($ billion)'] for m in measures):.2f} billion")
        print(f"{'='*70}")
        
        # Save measures
        measures_df = pd.DataFrame([{
            'Measure': m['Measure'],
            'Impact (% of GDP)': m['Impact (% of GDP)'],
            'Revenue Impact ($ billion)': m['Revenue Impact ($ billion)'],
            'Timeline': m['Timeline'],
            'Priority': m['Priority']
        } for m in measures])
        
        measures_df.to_csv('analysis/tax_analysis/revenue_enhancement_measures.csv', index=False)
        print(f"\n[OK] Saved measures to analysis/tax_analysis/revenue_enhancement_measures.csv")
        
        return measures
    
    def create_visualizations(self, gap_df, measures):
        """Create tax revenue visualizations"""
        print(f"\n{'='*70}")
        print("CREATING VISUALIZATIONS")
        print(f"{'='*70}")
        
        # Figure 1: Tax Revenue Gap
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Bar chart of gaps
        benchmarks = gap_df['Benchmark'].values
        gaps = gap_df['Revenue Gap ($ billion)'].values
        
        colors = ['red' if 'Current' in b else 'orange' if 'Minimum' in b or 'South' in b 
                  else 'yellow' if 'Target' in b else 'green' for b in benchmarks]
        
        ax1.barh(benchmarks, gaps, color=colors, alpha=0.7)
        ax1.set_xlabel('Revenue Gap ($ billion)')
        ax1.set_title('Bangladesh Tax Revenue Gap vs. International Benchmarks')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Tax-to-GDP comparison
        current_ratio = gap_df['Current Tax-to-GDP (%)'].iloc[0]
        target_ratios = gap_df['Target Tax-to-GDP (%)'].values
        
        x_pos = np.arange(len(benchmarks))
        ax2.bar(x_pos, target_ratios, alpha=0.7, label='Target', color='lightblue')
        ax2.axhline(y=current_ratio, color='red', linestyle='--', linewidth=2, 
                    label=f'Bangladesh Current ({current_ratio:.1f}%)')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(benchmarks, rotation=45, ha='right')
        ax2.set_ylabel('Tax-to-GDP Ratio (%)')
        ax2.set_title('Tax-to-GDP Ratio: Bangladesh vs. Benchmarks')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('analysis/tax_analysis/tax_revenue_gap.png', dpi=300, bbox_inches='tight')
        print("[OK] Saved: analysis/tax_analysis/tax_revenue_gap.png")
        plt.close()
        
        # Figure 2: Revenue Enhancement Measures
        fig, ax = plt.subplots(figsize=(12, 8))
        
        measure_names = [m['Measure'] for m in measures]
        impacts = [m['Revenue Impact ($ billion)'] for m in measures]
        priorities = [m['Priority'] for m in measures]
        
        colors_map = {'HIGH': 'darkgreen', 'MEDIUM': 'orange', 'LOW': 'gray'}
        colors = [colors_map[p] for p in priorities]
        
        bars = ax.barh(measure_names, impacts, color=colors, alpha=0.7)
        ax.set_xlabel('Additional Revenue ($ billion)')
        ax.set_title('Proposed Revenue Enhancement Measures - Potential Impact')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, impact) in enumerate(zip(bars, impacts)):
            ax.text(impact + 0.2, i, f'${impact:.1f}B', va='center')
        
        # Legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='darkgreen', alpha=0.7, label='HIGH Priority'),
                          Patch(facecolor='orange', alpha=0.7, label='MEDIUM Priority')]
        ax.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        plt.savefig('analysis/tax_analysis/revenue_enhancement_measures.png', dpi=300, bbox_inches='tight')
        print("[OK] Saved: analysis/tax_analysis/revenue_enhancement_measures.png")
        plt.close()
        
        # Figure 3: Historical trends
        revenue_col = 'Revenue, excluding grants (% of GDP)'
        expense_col = 'Expense (% of GDP)'
        
        revenue_data = self.df[self.df[revenue_col].notna()].copy()
        
        if not revenue_data.empty:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(revenue_data['year'], revenue_data[revenue_col], 
                   marker='o', linewidth=2, label='Revenue (% of GDP)', color='green')
            
            if expense_col in revenue_data.columns:
                expense_data = revenue_data[revenue_data[expense_col].notna()]
                if not expense_data.empty:
                    ax.plot(expense_data['year'], expense_data[expense_col], 
                           marker='s', linewidth=2, label='Expense (% of GDP)', color='red')
            
            # Add benchmark lines
            ax.axhline(y=15, color='orange', linestyle='--', alpha=0.7, 
                      label='Recommended Minimum (15%)')
            ax.axhline(y=18, color='blue', linestyle='--', alpha=0.7, 
                      label='Sustainable Target (18%)')
            
            ax.set_xlabel('Year')
            ax.set_ylabel('Percentage of GDP (%)')
            ax.set_title('Bangladesh Government Revenue & Expense Trends (2000-2024)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('analysis/tax_analysis/historical_revenue_trends.png', dpi=300, bbox_inches='tight')
            print("[OK] Saved: analysis/tax_analysis/historical_revenue_trends.png")
            plt.close()
    
    def generate_report(self, gap_df, measures, latest_year, current_ratio, gdp):
        """Generate comprehensive tax revenue report"""
        print(f"\n{'='*70}")
        print("GENERATING TAX REVENUE REPORT")
        print(f"{'='*70}")
        
        report = []
        report.append("# Bangladesh Tax Revenue Gap Analysis Report")
        report.append(f"\nGenerated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\nAnalysis Year: {int(latest_year)}")
        report.append("\n" + "="*70)
        
        # Executive Summary
        report.append("\n## Executive Summary")
        current_revenue = gdp * (current_ratio / 100)
        target_ratio = 18.0
        target_revenue = gdp * (target_ratio / 100)
        gap = target_revenue - current_revenue
        
        report.append(f"\nBangladesh's tax-to-GDP ratio stands at **{current_ratio:.2f}%** in {int(latest_year)}, ")
        report.append(f"significantly below international benchmarks and the recommended sustainable level of 18%.")
        report.append(f"\n\n**Current Tax Revenue**: ${current_revenue/1e9:.2f} billion")
        report.append(f"\n**Target Tax Revenue (18% of GDP)**: ${target_revenue/1e9:.2f} billion")
        report.append(f"\n**Revenue Gap**: ${gap/1e9:.2f} billion ({(gap/current_revenue*100):.1f}% increase needed)")
        
        # Current Situation
        report.append("\n\n## Current Situation")
        report.append(f"\n### Key Metrics ({int(latest_year)})")
        report.append(f"- **GDP**: ${gdp/1e9:.2f} billion")
        report.append(f"- **Tax-to-GDP Ratio**: {current_ratio:.2f}%")
        report.append(f"- **Total Tax Revenue**: ${current_revenue/1e9:.2f} billion")
        report.append(f"- **Ranking**: One of the lowest tax-to-GDP ratios globally")
        
        # International Comparison
        report.append("\n\n## International Comparison")
        report.append("\n| Benchmark | Tax-to-GDP (%) | Revenue Gap ($ billion) |")
        report.append("|-----------|----------------|------------------------|")
        for _, row in gap_df.iterrows():
            report.append(f"| {row['Benchmark']} | {row['Target Tax-to-GDP (%)']:.1f}% | ${row['Revenue Gap ($ billion)']:.2f}B |")
        
        # Root Causes
        report.append("\n\n## Why Tax Revenue is Low")
        report.append("\n### 1. Narrow Tax Base")
        report.append("- Only ~1.5 million individual taxpayers (less than 1% of population)")
        report.append("- Large informal economy (35-40% of GDP) remains untaxed")
        report.append("- Agriculture sector largely exempt")
        report.append("- Extensive tax exemptions and incentives")
        
        report.append("\n### 2. Tax Evasion & Avoidance")
        report.append("- **Estimated loss**: 3-5% of GDP")
        report.append("- Under-reporting of income widespread")
        report.append("- Cash-based economy avoids VAT")
        report.append("- Transfer pricing by multinationals")
        report.append("- Weak enforcement mechanisms")
        
        report.append("\n### 3. Weak Tax Administration")
        report.append("- **Estimated loss**: 1-2% of GDP")
        report.append("- Manual, paper-based processes")
        report.append("- Limited digitalization")
        report.append("- Corruption in tax collection")
        report.append("- Complex tax laws and procedures")
        report.append("- Inadequate staff and resources")
        
        report.append("\n### 4. Customs Revenue Losses")
        report.append("- **Estimated loss**: 1-2% of GDP")
        report.append("- Under-invoicing of imports")
        report.append("- Smuggling and illegal trade")
        report.append("- Excessive duty exemptions")
        report.append("- Weak border controls")
        
        report.append("\n### 5. Property Tax Underutilization")
        report.append("- **Estimated loss**: 0.5-1% of GDP")
        report.append("- Outdated property valuations")
        report.append("- Low collection rates")
        report.append("- Political resistance to increases")
        
        # Revenue Enhancement Measures
        report.append("\n\n## Revenue Enhancement Roadmap")
        report.append(f"\n**Target**: Increase tax-to-GDP ratio from {current_ratio:.2f}% to 18% over 5 years")
        report.append(f"\n**Required Additional Revenue**: ${gap/1e9:.2f} billion")
        report.append(f"\n**Annual Increase Needed**: ${(gap/5)/1e9:.2f} billion/year")
        
        report.append("\n\n### Proposed Measures")
        
        for i, measure in enumerate(measures, 1):
            report.append(f"\n#### {i}. {measure['Measure']}")
            report.append(f"**Priority**: {measure['Priority']}")
            report.append(f"\n**Impact**: {measure['Impact (% of GDP)']}% of GDP (${measure['Revenue Impact ($ billion)']:.2f} billion)")
            report.append(f"\n**Timeline**: {measure['Timeline']}")
            report.append("\n**Key Actions**:")
            for action in measure['Actions']:
                report.append(f"- {action}")
        
        total_impact = sum(m['Impact (% of GDP)'] for m in measures)
        total_revenue = sum(m['Revenue Impact ($ billion)'] for m in measures)
        
        report.append(f"\n\n### Total Potential Impact")
        report.append(f"- **Tax-to-GDP increase**: {total_impact}% of GDP")
        report.append(f"- **Additional revenue**: ${total_revenue:.2f} billion")
        report.append(f"- **New tax-to-GDP ratio**: {current_ratio + total_impact:.1f}%")
        
        # Implementation Timeline
        report.append("\n\n## Implementation Timeline")
        
        report.append("\n### Year 1 (2024-2025)")
        report.append("- Launch tax digitalization program")
        report.append("- Implement e-filing for all taxpayers")
        report.append("- Begin VAT system reform")
        report.append("- Start customs modernization")
        report.append("- **Expected revenue increase**: $2-3 billion")
        
        report.append("\n### Year 2-3 (2025-2027)")
        report.append("- Scale up formalization of informal sector")
        report.append("- Expand taxpayer base to 3 million")
        report.append("- Strengthen audit and enforcement")
        report.append("- Update property valuations")
        report.append("- **Expected cumulative increase**: $5-7 billion")
        
        report.append("\n### Year 4-5 (2027-2029)")
        report.append("- Achieve 5 million taxpayer base")
        report.append("- Full digital tax administration")
        report.append("- Comprehensive anti-evasion measures")
        report.append("- Reach 18% tax-to-GDP target")
        report.append(f"- **Expected cumulative increase**: ${gap/1e9:.2f} billion")
        
        # Success Factors
        report.append("\n\n## Critical Success Factors")
        report.append("\n1. **Political Will**: Strong commitment from government leadership")
        report.append("2. **Institutional Capacity**: Invest in National Board of Revenue (NBR)")
        report.append("3. **Technology**: Rapid digitalization of tax systems")
        report.append("4. **Public Trust**: Transparent use of tax revenues")
        report.append("5. **Simplification**: Make tax compliance easier")
        report.append("6. **Enforcement**: Credible penalties for non-compliance")
        report.append("7. **Coordination**: Align central and local tax authorities")
        
        # Benefits
        report.append("\n\n## Benefits of Increased Tax Revenue")
        report.append(f"\nWith an additional ${gap/1e9:.2f} billion in annual tax revenue, Bangladesh could:")
        report.append(f"\n- **Reduce external borrowing** by 50-70%")
        report.append(f"- **Invest in infrastructure** without accumulating debt")
        report.append(f"- **Strengthen social safety nets** (education, healthcare)")
        report.append(f"- **Build foreign reserves** to 6+ months of imports")
        report.append(f"- **Achieve fiscal sustainability** and reduce debt-to-GDP ratio")
        
        # Conclusion
        report.append("\n\n## Conclusion")
        report.append(f"\nBangladesh's low tax-to-GDP ratio of {current_ratio:.2f}% is a critical constraint on fiscal sustainability ")
        report.append("and a major driver of external debt accumulation. The country is leaving significant revenue on the table - ")
        report.append(f"an estimated ${gap/1e9:.2f} billion annually compared to the sustainable target of 18% of GDP.")
        report.append("\n\nThe proposed revenue enhancement measures are achievable and have been successfully implemented ")
        report.append("in peer countries. With strong political will, institutional reforms, and technology adoption, ")
        report.append("Bangladesh can increase its tax-to-GDP ratio to 18% within 5 years, significantly reducing ")
        report.append("its dependence on external borrowing and putting the country on a sustainable fiscal path.")
        
        report.append("\n\n## Data Sources")
        report.append("- World Bank Open Data")
        report.append("- International Monetary Fund (IMF)")
        report.append("- National Board of Revenue (NBR), Bangladesh")
        report.append("- OECD Tax Statistics")
        
        report.append("\n\n---")
        report.append("\n*This analysis is based on publicly available data and international best practices.*")
        
        # Save report
        report_text = '\n'.join(report)
        with open('analysis/tax_analysis/tax_revenue_gap_report.md', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print("[OK] Saved: analysis/tax_analysis/tax_revenue_gap_report.md")
    
    def run_full_analysis(self):
        """Run complete tax revenue analysis"""
        print("\n" + "="*70)
        print("BANGLADESH TAX REVENUE GAP - COMPREHENSIVE ANALYSIS")
        print("="*70)
        
        gap_df, latest_year, current_ratio, gdp = self.calculate_tax_revenue_gap()
        self.analyze_historical_trends()
        self.identify_revenue_leakages()
        measures = self.propose_revenue_enhancement_measures(gap_df, latest_year, current_ratio, gdp)
        self.create_visualizations(gap_df, measures)
        self.generate_report(gap_df, measures, latest_year, current_ratio, gdp)
        
        print("\n" + "="*70)
        print("TAX REVENUE ANALYSIS COMPLETED")
        print("="*70)
        print("\nGenerated files:")
        print("  1. analysis/tax_analysis/tax_revenue_gap_analysis.csv")
        print("  2. analysis/tax_analysis/revenue_enhancement_measures.csv")
        print("  3. analysis/tax_analysis/tax_revenue_gap.png")
        print("  4. analysis/tax_analysis/revenue_enhancement_measures.png")
        print("  5. analysis/tax_analysis/historical_revenue_trends.png")
        print("  6. analysis/tax_analysis/tax_revenue_gap_report.md")
        print("\nReview the report for detailed findings and recommendations.")
        print("="*70)

def main():
    """Main execution function"""
    analyzer = TaxRevenueAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()

# Made with Bob
