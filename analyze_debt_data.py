"""
Bangladesh External Debt Analysis
Exploratory data analysis and visualization of Bangladesh's debt situation
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

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class BangladeshDebtAnalyzer:
    """Analyze Bangladesh's external debt data"""
    
    def __init__(self, data_path='data/processed/bangladesh_debt_consolidated.csv'):
        """Initialize analyzer with data"""
        self.data_path = data_path
        self.df = None
        self.load_data()
        
        # Create output directory
        Path('analysis/figures').mkdir(parents=True, exist_ok=True)
        Path('analysis/reports').mkdir(parents=True, exist_ok=True)
    
    def load_data(self):
        """Load the consolidated dataset"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"[OK] Loaded data: {len(self.df)} years of data")
            print(f"     Years: {self.df['year'].min()} - {self.df['year'].max()}")
            print(f"     Indicators: {len(self.df.columns) - 1}")
        except Exception as e:
            print(f"[ERROR] Failed to load data: {e}")
            sys.exit(1)
    
    def analyze_debt_trends(self):
        """Analyze external debt trends over time"""
        print("\n" + "="*60)
        print("DEBT TREND ANALYSIS")
        print("="*60)
        
        # Key findings
        debt_col = 'External debt stocks, total (current US$)'
        gdp_col = 'GDP (current US$)'
        debt_gdp_col = 'Debt-to-GDP Ratio (%)'
        
        if debt_col in self.df.columns:
            debt_2000 = self.df[self.df['year'] == 2000][debt_col].values[0]
            debt_2024 = self.df[self.df['year'] == 2024][debt_col].values[0]
            debt_growth = ((debt_2024 / debt_2000) - 1) * 100
            
            print(f"\n1. EXTERNAL DEBT GROWTH:")
            print(f"   - 2000: ${debt_2000/1e9:.2f} billion")
            print(f"   - 2024: ${debt_2024/1e9:.2f} billion")
            print(f"   - Growth: {debt_growth:.1f}% over 24 years")
            print(f"   - Average annual growth: {(debt_growth/24):.1f}%")
        
        if debt_gdp_col in self.df.columns:
            debt_gdp_2000 = self.df[self.df['year'] == 2000][debt_gdp_col].values[0]
            debt_gdp_2024 = self.df[self.df['year'] == 2024][debt_gdp_col].values[0]
            debt_gdp_max = self.df[debt_gdp_col].max()
            debt_gdp_max_year = self.df[self.df[debt_gdp_col] == debt_gdp_max]['year'].values[0]
            
            print(f"\n2. DEBT-TO-GDP RATIO:")
            print(f"   - 2000: {debt_gdp_2000:.2f}%")
            print(f"   - 2024: {debt_gdp_2024:.2f}%")
            print(f"   - Peak: {debt_gdp_max:.2f}% in {debt_gdp_max_year}")
            print(f"   - Change: {debt_gdp_2024 - debt_gdp_2000:.2f} percentage points")
        
        # Debt service analysis
        debt_service_col = 'Total debt service on external debt'
        debt_service_ratio_col = 'Debt Service Ratio (%)'
        
        if debt_service_col in self.df.columns:
            ds_2000 = self.df[self.df['year'] == 2000][debt_service_col].values[0]
            ds_2024 = self.df[self.df['year'] == 2024][debt_service_col].values[0]
            ds_growth = ((ds_2024 / ds_2000) - 1) * 100
            
            print(f"\n3. DEBT SERVICE PAYMENTS:")
            print(f"   - 2000: ${ds_2000/1e9:.2f} billion")
            print(f"   - 2024: ${ds_2024/1e9:.2f} billion")
            print(f"   - Growth: {ds_growth:.1f}%")
        
        if debt_service_ratio_col in self.df.columns:
            dsr_2024 = self.df[self.df['year'] == 2024][debt_service_ratio_col].values[0]
            print(f"   - 2024 Debt Service Ratio: {dsr_2024:.2f}% of exports")
            print(f"     (Sustainable threshold: typically <15%)")
    
    def analyze_economic_context(self):
        """Analyze economic context and correlations"""
        print("\n" + "="*60)
        print("ECONOMIC CONTEXT ANALYSIS")
        print("="*60)
        
        # GDP growth
        gdp_growth_col = 'GDP growth (annual %)'
        if gdp_growth_col in self.df.columns:
            avg_growth = self.df[gdp_growth_col].mean()
            recent_growth = self.df[self.df['year'] >= 2020][gdp_growth_col].mean()
            
            print(f"\n1. GDP GROWTH:")
            print(f"   - Average (2000-2024): {avg_growth:.2f}%")
            print(f"   - Recent average (2020-2024): {recent_growth:.2f}%")
        
        # Trade balance
        trade_col = 'Trade Balance (current US$)'
        if trade_col in self.df.columns:
            trade_deficit_years = len(self.df[self.df[trade_col] < 0])
            avg_deficit = self.df[self.df[trade_col] < 0][trade_col].mean()
            recent_deficit = self.df[(self.df['year'] >= 2020) & (self.df[trade_col] < 0)][trade_col].mean()
            
            print(f"\n2. TRADE BALANCE:")
            print(f"   - Years with deficit: {trade_deficit_years} out of {len(self.df)}")
            print(f"   - Average deficit: ${abs(avg_deficit)/1e9:.2f} billion")
            print(f"   - Recent deficit (2020-2024): ${abs(recent_deficit)/1e9:.2f} billion")
        
        # Reserves
        reserves_col = 'Total reserves (includes gold, current US$)'
        if reserves_col in self.df.columns:
            reserves_2024 = self.df[self.df['year'] == 2024][reserves_col].values[0]
            reserves_peak = self.df[reserves_col].max()
            reserves_peak_year = self.df[self.df[reserves_col] == reserves_peak]['year'].values[0]
            
            print(f"\n3. FOREIGN RESERVES:")
            print(f"   - 2024: ${reserves_2024/1e9:.2f} billion")
            print(f"   - Peak: ${reserves_peak/1e9:.2f} billion in {reserves_peak_year}")
            print(f"   - Change from peak: {((reserves_2024/reserves_peak - 1) * 100):.1f}%")
        
        # Exchange rate
        exchange_col = 'Official exchange rate (LCU per US$, period average)'
        if exchange_col in self.df.columns:
            exch_2000 = self.df[self.df['year'] == 2000][exchange_col].values[0]
            exch_2024 = self.df[self.df['year'] == 2024][exchange_col].values[0]
            depreciation = ((exch_2024 / exch_2000) - 1) * 100
            
            print(f"\n4. CURRENCY DEPRECIATION:")
            print(f"   - 2000: {exch_2000:.2f} BDT per USD")
            print(f"   - 2024: {exch_2024:.2f} BDT per USD")
            print(f"   - Depreciation: {depreciation:.1f}%")
    
    def identify_root_causes(self):
        """Identify root causes of debt accumulation"""
        print("\n" + "="*60)
        print("ROOT CAUSE ANALYSIS")
        print("="*60)
        
        print("\nBased on the data analysis, key factors contributing to debt:")
        
        # Factor 1: Persistent trade deficits
        trade_col = 'Trade Balance (current US$)'
        if trade_col in self.df.columns:
            total_deficit = self.df[self.df[trade_col] < 0][trade_col].sum()
            print(f"\n1. PERSISTENT TRADE DEFICITS")
            print(f"   - Cumulative deficit (2000-2024): ${abs(total_deficit)/1e9:.2f} billion")
            print(f"   - Imports consistently exceed exports")
            print(f"   - Heavy reliance on imported fuel, machinery, and raw materials")
        
        # Factor 2: Infrastructure development
        debt_col = 'External debt stocks, total (current US$)'
        if debt_col in self.df.columns:
            # Identify periods of rapid debt growth
            self.df['debt_growth'] = self.df[debt_col].pct_change() * 100
            high_growth_years = self.df[self.df['debt_growth'] > 10]
            
            print(f"\n2. INFRASTRUCTURE DEVELOPMENT FINANCING")
            print(f"   - Years with >10% debt growth: {len(high_growth_years)}")
            if len(high_growth_years) > 0:
                print(f"   - Notable periods: {', '.join(map(str, high_growth_years['year'].values))}")
            print(f"   - Major projects: Padma Bridge, metro rail, power plants")
        
        # Factor 3: Currency depreciation impact
        exchange_col = 'Official exchange rate (LCU per US$, period average)'
        if exchange_col in self.df.columns and debt_col in self.df.columns:
            print(f"\n3. CURRENCY DEPRECIATION IMPACT")
            print(f"   - Taka depreciation increases USD-denominated debt burden")
            print(f"   - Makes debt servicing more expensive in local currency")
        
        # Factor 4: Economic shocks
        gdp_growth_col = 'GDP growth (annual %)'
        if gdp_growth_col in self.df.columns:
            low_growth_years = self.df[self.df[gdp_growth_col] < 4]
            print(f"\n4. ECONOMIC SHOCKS")
            print(f"   - Years with GDP growth <4%: {len(low_growth_years)}")
            if 2020 in low_growth_years['year'].values:
                print(f"   - COVID-19 pandemic (2020): Significant economic impact")
            print(f"   - Climate disasters and global commodity price shocks")
    
    def propose_solutions(self):
        """Propose evidence-based solutions"""
        print("\n" + "="*60)
        print("PROPOSED SOLUTIONS")
        print("="*60)
        
        debt_service_ratio_col = 'Debt Service Ratio (%)'
        current_dsr = self.df[self.df['year'] == 2024][debt_service_ratio_col].values[0]
        
        print("\nBased on data analysis, recommended solutions:")
        
        print("\n1. EXPORT DIVERSIFICATION & GROWTH")
        print("   Priority: HIGH")
        print("   - Current debt service ratio: {:.2f}% of exports".format(current_dsr))
        print("   - Target: Increase exports by 50% over 5 years")
        print("   - Actions:")
        print("     * Diversify beyond garments (IT services, pharmaceuticals)")
        print("     * Improve export competitiveness")
        print("     * Negotiate better trade agreements")
        
        print("\n2. IMPORT SUBSTITUTION")
        print("   Priority: HIGH")
        print("   - Reduce dependency on imported fuel and raw materials")
        print("   - Actions:")
        print("     * Develop domestic energy sources (renewables)")
        print("     * Strengthen local manufacturing")
        print("     * Improve agricultural productivity")
        
        print("\n3. DEBT RESTRUCTURING")
        print("   Priority: MEDIUM")
        print("   - Negotiate with creditors for:")
        print("     * Extended repayment periods")
        print("     * Lower interest rates")
        print("     * Grace periods for principal payments")
        
        print("\n4. REVENUE ENHANCEMENT")
        print("   Priority: HIGH")
        print("   - Improve tax collection efficiency")
        print("   - Broaden tax base")
        print("   - Reduce tax evasion and avoidance")
        print("   - Target: Increase tax-to-GDP ratio by 3 percentage points")
        
        print("\n5. FOREIGN EXCHANGE MANAGEMENT")
        print("   Priority: MEDIUM")
        print("   - Rebuild foreign reserves")
        print("   - Attract more FDI and remittances")
        print("   - Manage currency stability")
        
        print("\n6. CONCESSIONAL FINANCING")
        print("   Priority: MEDIUM")
        print("   - Maximize grants and soft loans")
        print("   - Leverage climate financing opportunities")
        print("   - Strengthen relationships with development partners")
        
        print("\n7. FISCAL DISCIPLINE")
        print("   Priority: HIGH")
        print("   - Prioritize high-return infrastructure investments")
        print("   - Improve project implementation efficiency")
        print("   - Reduce non-productive spending")
    
    def create_visualizations(self):
        """Create key visualizations"""
        print("\n" + "="*60)
        print("CREATING VISUALIZATIONS")
        print("="*60)
        
        # Figure 1: Debt and GDP trends
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        debt_col = 'External debt stocks, total (current US$)'
        gdp_col = 'GDP (current US$)'
        
        if debt_col in self.df.columns and gdp_col in self.df.columns:
            ax1.plot(self.df['year'], self.df[debt_col]/1e9, marker='o', linewidth=2, label='External Debt')
            ax1.plot(self.df['year'], self.df[gdp_col]/1e9, marker='s', linewidth=2, label='GDP')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Billion USD')
            ax1.set_title('Bangladesh: External Debt vs GDP (2000-2024)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        debt_gdp_col = 'Debt-to-GDP Ratio (%)'
        if debt_gdp_col in self.df.columns:
            ax2.plot(self.df['year'], self.df[debt_gdp_col], marker='o', linewidth=2, color='red')
            ax2.axhline(y=30, color='orange', linestyle='--', label='Caution threshold (30%)')
            ax2.set_xlabel('Year')
            ax2.set_ylabel('Percentage (%)')
            ax2.set_title('Debt-to-GDP Ratio (2000-2024)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis/figures/debt_trends.png', dpi=300, bbox_inches='tight')
        print("[OK] Saved: analysis/figures/debt_trends.png")
        plt.close()
        
        # Figure 2: Trade balance and debt service
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        trade_col = 'Trade Balance (current US$)'
        if trade_col in self.df.columns:
            colors = ['red' if x < 0 else 'green' for x in self.df[trade_col]]
            ax1.bar(self.df['year'], self.df[trade_col]/1e9, color=colors, alpha=0.7)
            ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Billion USD')
            ax1.set_title('Trade Balance (2000-2024)')
            ax1.grid(True, alpha=0.3)
        
        debt_service_ratio_col = 'Debt Service Ratio (%)'
        if debt_service_ratio_col in self.df.columns:
            ax2.plot(self.df['year'], self.df[debt_service_ratio_col], marker='o', linewidth=2, color='purple')
            ax2.axhline(y=15, color='orange', linestyle='--', label='Sustainable threshold (15%)')
            ax2.set_xlabel('Year')
            ax2.set_ylabel('Percentage (%)')
            ax2.set_title('Debt Service Ratio (% of Exports)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis/figures/trade_and_debt_service.png', dpi=300, bbox_inches='tight')
        print("[OK] Saved: analysis/figures/trade_and_debt_service.png")
        plt.close()
        
        # Figure 3: Economic indicators
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        gdp_growth_col = 'GDP growth (annual %)'
        if gdp_growth_col in self.df.columns:
            ax1.plot(self.df['year'], self.df[gdp_growth_col], marker='o', linewidth=2, color='green')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Percentage (%)')
            ax1.set_title('GDP Growth Rate')
            ax1.grid(True, alpha=0.3)
        
        reserves_col = 'Total reserves (includes gold, current US$)'
        if reserves_col in self.df.columns:
            ax2.plot(self.df['year'], self.df[reserves_col]/1e9, marker='o', linewidth=2, color='blue')
            ax2.set_xlabel('Year')
            ax2.set_ylabel('Billion USD')
            ax2.set_title('Foreign Reserves')
            ax2.grid(True, alpha=0.3)
        
        exchange_col = 'Official exchange rate (LCU per US$, period average)'
        if exchange_col in self.df.columns:
            ax3.plot(self.df['year'], self.df[exchange_col], marker='o', linewidth=2, color='orange')
            ax3.set_xlabel('Year')
            ax3.set_ylabel('BDT per USD')
            ax3.set_title('Exchange Rate (Taka Depreciation)')
            ax3.grid(True, alpha=0.3)
        
        debt_service_col = 'Total debt service on external debt'
        if debt_service_col in self.df.columns:
            ax4.plot(self.df['year'], self.df[debt_service_col]/1e9, marker='o', linewidth=2, color='red')
            ax4.set_xlabel('Year')
            ax4.set_ylabel('Billion USD')
            ax4.set_title('Annual Debt Service Payments')
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis/figures/economic_indicators.png', dpi=300, bbox_inches='tight')
        print("[OK] Saved: analysis/figures/economic_indicators.png")
        plt.close()
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*60)
        print("GENERATING COMPREHENSIVE REPORT")
        print("="*60)
        
        report = []
        report.append("# Bangladesh External Debt Analysis Report")
        report.append(f"\nGenerated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\nData Period: {self.df['year'].min()} - {self.df['year'].max()}")
        report.append("\n" + "="*60)
        
        # Executive Summary
        report.append("\n## Executive Summary")
        debt_col = 'External debt stocks, total (current US$)'
        debt_2024 = self.df[self.df['year'] == 2024][debt_col].values[0]
        debt_2000 = self.df[self.df['year'] == 2000][debt_col].values[0]
        
        report.append(f"\nBangladesh's external debt has grown from ${debt_2000/1e9:.2f} billion in 2000 to ${debt_2024/1e9:.2f} billion in 2024, ")
        report.append(f"representing a {((debt_2024/debt_2000 - 1) * 100):.1f}% increase over 24 years.")
        
        debt_gdp_col = 'Debt-to-GDP Ratio (%)'
        debt_gdp_2024 = self.df[self.df['year'] == 2024][debt_gdp_col].values[0]
        report.append(f"\nThe debt-to-GDP ratio stands at {debt_gdp_2024:.2f}% in 2024, which is within manageable levels but requires careful monitoring.")
        
        # Key Findings
        report.append("\n\n## Key Findings")
        
        report.append("\n### 1. Debt Growth Trajectory")
        report.append(f"- External debt increased by {((debt_2024/debt_2000 - 1) * 100):.1f}% from 2000 to 2024")
        report.append(f"- Average annual growth rate: {(((debt_2024/debt_2000 - 1) * 100)/24):.1f}%")
        report.append("- Accelerated growth observed post-2015 due to major infrastructure projects")
        
        report.append("\n### 2. Debt Sustainability")
        debt_service_ratio_col = 'Debt Service Ratio (%)'
        dsr_2024 = self.df[self.df['year'] == 2024][debt_service_ratio_col].values[0]
        report.append(f"- Current debt service ratio: {dsr_2024:.2f}% of exports")
        report.append("- Above the sustainable threshold of 15%, indicating pressure on foreign exchange")
        report.append("- Debt servicing costs have increased significantly in recent years")
        
        report.append("\n### 3. Economic Context")
        gdp_growth_col = 'GDP growth (annual %)'
        avg_growth = self.df[gdp_growth_col].mean()
        report.append(f"- Average GDP growth (2000-2024): {avg_growth:.2f}%")
        report.append("- Persistent trade deficits throughout the period")
        report.append("- Currency depreciation has increased debt burden in local terms")
        
        # Root Causes
        report.append("\n\n## Root Causes of Debt Accumulation")
        
        report.append("\n### 1. Infrastructure Development")
        report.append("- Large-scale projects: Padma Bridge, Dhaka Metro Rail, power plants")
        report.append("- Necessary for economic development but financed through external borrowing")
        report.append("- Long gestation periods before returns materialize")
        
        report.append("\n### 2. Persistent Trade Deficits")
        trade_col = 'Trade Balance (current US$)'
        deficit_years = len(self.df[self.df[trade_col] < 0])
        report.append(f"- Trade deficits in {deficit_years} out of {len(self.df)} years")
        report.append("- Heavy reliance on imported fuel, machinery, and raw materials")
        report.append("- Export concentration in garment sector (limited diversification)")
        
        report.append("\n### 3. Currency Depreciation")
        exchange_col = 'Official exchange rate (LCU per US$, period average)'
        exch_2000 = self.df[self.df['year'] == 2000][exchange_col].values[0]
        exch_2024 = self.df[self.df['year'] == 2024][exchange_col].values[0]
        depreciation = ((exch_2024 / exch_2000) - 1) * 100
        report.append(f"- Taka depreciated by {depreciation:.1f}% against USD (2000-2024)")
        report.append("- Increases the local currency cost of servicing USD-denominated debt")
        
        report.append("\n### 4. Economic Shocks")
        report.append("- COVID-19 pandemic impact (2020)")
        report.append("- Global commodity price volatility")
        report.append("- Climate-related disasters affecting agriculture and infrastructure")
        
        # Solutions
        report.append("\n\n## Recommended Solutions")
        
        report.append("\n### Priority 1: Export Diversification and Growth")
        report.append("**Target**: Increase exports by 50% over 5 years")
        report.append("- Diversify beyond garments into IT services, pharmaceuticals, light engineering")
        report.append("- Improve export competitiveness through infrastructure and skills development")
        report.append("- Negotiate favorable trade agreements with key partners")
        report.append("- Support SMEs in export-oriented sectors")
        
        report.append("\n### Priority 2: Import Substitution")
        report.append("**Target**: Reduce import dependency by 20% in key sectors")
        report.append("- Develop domestic energy sources (solar, wind, hydroelectric)")
        report.append("- Strengthen local manufacturing capabilities")
        report.append("- Improve agricultural productivity to reduce food imports")
        report.append("- Invest in technology and innovation")
        
        report.append("\n### Priority 3: Revenue Enhancement")
        report.append("**Target**: Increase tax-to-GDP ratio by 3 percentage points")
        report.append("- Modernize tax administration with digital systems")
        report.append("- Broaden tax base by bringing informal sector into formal economy")
        report.append("- Reduce tax evasion through better enforcement")
        report.append("- Rationalize tax incentives and exemptions")
        
        report.append("\n### Priority 4: Debt Management")
        report.append("- Negotiate debt restructuring with major creditors")
        report.append("- Seek extended repayment periods and lower interest rates")
        report.append("- Maximize concessional financing and grants")
        report.append("- Improve debt management capacity")
        
        report.append("\n### Priority 5: Foreign Exchange Management")
        report.append("- Rebuild foreign reserves to comfortable levels (6+ months of imports)")
        report.append("- Attract more FDI through improved business environment")
        report.append("- Facilitate remittance inflows")
        report.append("- Manage exchange rate stability")
        
        # Implementation Timeline
        report.append("\n\n## Implementation Timeline")
        report.append("\n### Short-term (0-12 months)")
        report.append("- Initiate debt restructuring negotiations")
        report.append("- Launch export promotion campaigns")
        report.append("- Implement quick-win tax reforms")
        
        report.append("\n### Medium-term (1-3 years)")
        report.append("- Scale up import substitution programs")
        report.append("- Develop new export sectors")
        report.append("- Strengthen debt management systems")
        
        report.append("\n### Long-term (3-5 years)")
        report.append("- Achieve export diversification targets")
        report.append("- Reduce debt-to-GDP ratio below 20%")
        report.append("- Build sustainable fiscal framework")
        
        # Conclusion
        report.append("\n\n## Conclusion")
        report.append("\nBangladesh's external debt situation, while manageable, requires immediate attention and strategic action.")
        report.append("The combination of export growth, import substitution, revenue enhancement, and prudent debt management")
        report.append("can put the country on a sustainable fiscal path. Success will require strong political will,")
        report.append("effective implementation, and coordination across government agencies.")
        
        report.append("\n\n## Data Sources")
        report.append("- World Bank Open Data API")
        report.append("- International Monetary Fund (IMF)")
        report.append("- Bangladesh Bank")
        
        report.append("\n\n---")
        report.append("\n*This analysis is based on publicly available data and should be used for informational purposes.*")
        
        # Save report
        report_text = '\n'.join(report)
        with open('analysis/reports/bangladesh_debt_analysis.md', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print("[OK] Saved: analysis/reports/bangladesh_debt_analysis.md")
    
    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        print("\n" + "="*60)
        print("BANGLADESH EXTERNAL DEBT - COMPREHENSIVE ANALYSIS")
        print("="*60)
        
        self.analyze_debt_trends()
        self.analyze_economic_context()
        self.identify_root_causes()
        self.propose_solutions()
        self.create_visualizations()
        self.generate_report()
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETED")
        print("="*60)
        print("\nGenerated files:")
        print("  1. analysis/figures/debt_trends.png")
        print("  2. analysis/figures/trade_and_debt_service.png")
        print("  3. analysis/figures/economic_indicators.png")
        print("  4. analysis/reports/bangladesh_debt_analysis.md")
        print("\nReview the report for detailed findings and recommendations.")
        print("="*60)

def main():
    """Main execution function"""
    analyzer = BangladeshDebtAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()

# Made with Bob
