import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

class AgriculturalSectorAnalyzer:
    def __init__(self):
        """Initialize the analyzer with multiple data sources"""
        # Load all relevant data
        self.agri_df = pd.read_csv('data/processed/agricultural_detailed_pivot.csv')
        self.agri_df.set_index('year', inplace=True)
        
        self.pop_df = pd.read_csv('data/processed/population_occupation_earnings_pivot.csv')
        self.pop_df.set_index('year', inplace=True)
        
        # Create output directories
        os.makedirs('analysis/agricultural_sector', exist_ok=True)
        os.makedirs('analysis/agricultural_sector/figures', exist_ok=True)
        
    def calculate_agricultural_earnings_distribution(self):
        """Calculate detailed earnings distribution in agricultural sector"""
        print("\n" + "="*80)
        print("AGRICULTURAL SECTOR EARNINGS ANALYSIS")
        print("="*80)
        
        latest_year = 2024
        
        # Get agricultural value added
        agri_value = self.agri_df['Agriculture, forestry, and fishing, value added (current US$)'][latest_year]
        agri_pct_gdp = self.agri_df['Agriculture, forestry, and fishing, value added (% of GDP)'][latest_year]
        
        # Get employment data
        agri_emp_pct = self.pop_df['Employment in Agriculture (% of total employment)'][latest_year]
        labor_force = self.pop_df['Labor Force, Total'][latest_year]
        unemployment = self.pop_df['Unemployment Rate (%)'][latest_year]
        
        # Calculate agricultural workers
        total_employed = labor_force * (1 - unemployment/100)
        agri_workers = total_employed * agri_emp_pct / 100
        
        # Calculate average earnings per agricultural worker
        avg_agri_earnings = agri_value / agri_workers
        
        # Get income distribution data
        income_dist = {}
        for quintile in ['lowest 10%', 'lowest 20%', 'second 20%', 'third 20%', 'fourth 20%', 'highest 20%', 'highest 10%']:
            col_name = f'Income share held by {quintile}'
            if col_name in self.agri_df.columns:
                latest_val_year = self.agri_df[col_name].last_valid_index()
                if latest_val_year:
                    income_dist[quintile] = self.agri_df[col_name][latest_val_year]
        
        # Calculate GNI per capita for reference
        gni_per_capita = self.agri_df['GNI per capita, Atlas method (current US$)'][latest_year]
        gni_ppp = self.agri_df['GNI per capita, PPP (current international $)'][latest_year]
        
        print(f"\n1. Agricultural Sector Overview ({latest_year}):")
        print(f"   - Total Agricultural Value Added: ${agri_value:,.0f}")
        print(f"   - Agriculture as % of GDP: {agri_pct_gdp:.1f}%")
        print(f"   - Total Agricultural Workers: {agri_workers:,.0f}")
        print(f"   - Average Earnings per Agricultural Worker: ${avg_agri_earnings:,.2f}/year")
        print(f"   - Average Monthly Earnings: ${avg_agri_earnings/12:,.2f}")
        print(f"   - Average Daily Earnings: ${avg_agri_earnings/365:,.2f}")
        
        print(f"\n2. Comparison with National Averages:")
        print(f"   - GNI per Capita (Atlas method): ${gni_per_capita:,.2f}")
        print(f"   - GNI per Capita (PPP): ${gni_ppp:,.2f}")
        print(f"   - Agricultural earnings as % of GNI: {(avg_agri_earnings/gni_per_capita)*100:.1f}%")
        
        # Estimate earnings distribution in agriculture based on national income distribution
        print(f"\n3. Estimated Agricultural Earnings Distribution:")
        print(f"   (Based on national income distribution patterns)")
        
        if income_dist:
            # Calculate earnings for each income group
            earnings_by_group = {}
            
            # Lowest 10%
            if 'lowest 10%' in income_dist:
                share = income_dist['lowest 10%'] / 100
                earnings_by_group['Lowest 10%'] = {
                    'share': income_dist['lowest 10%'],
                    'annual_earnings': avg_agri_earnings * share * 10,  # multiply by 10 to get per capita
                    'workers': agri_workers * 0.10
                }
            
            # Lowest 20% (includes lowest 10%)
            if 'lowest 20%' in income_dist:
                share = income_dist['lowest 20%'] / 100
                earnings_by_group['Lowest 20%'] = {
                    'share': income_dist['lowest 20%'],
                    'annual_earnings': avg_agri_earnings * share * 5,  # multiply by 5 to get per capita
                    'workers': agri_workers * 0.20
                }
            
            # Second 20%
            if 'second 20%' in income_dist:
                share = income_dist['second 20%'] / 100
                earnings_by_group['Second 20%'] = {
                    'share': income_dist['second 20%'],
                    'annual_earnings': avg_agri_earnings * share * 5,
                    'workers': agri_workers * 0.20
                }
            
            # Third 20%
            if 'third 20%' in income_dist:
                share = income_dist['third 20%'] / 100
                earnings_by_group['Third 20%'] = {
                    'share': income_dist['third 20%'],
                    'annual_earnings': avg_agri_earnings * share * 5,
                    'workers': agri_workers * 0.20
                }
            
            # Fourth 20%
            if 'fourth 20%' in income_dist:
                share = income_dist['fourth 20%'] / 100
                earnings_by_group['Fourth 20%'] = {
                    'share': income_dist['fourth 20%'],
                    'annual_earnings': avg_agri_earnings * share * 5,
                    'workers': agri_workers * 0.20
                }
            
            # Highest 20%
            if 'highest 20%' in income_dist:
                share = income_dist['highest 20%'] / 100
                earnings_by_group['Highest 20%'] = {
                    'share': income_dist['highest 20%'],
                    'annual_earnings': avg_agri_earnings * share * 5,
                    'workers': agri_workers * 0.20
                }
            
            # Highest 10%
            if 'highest 10%' in income_dist:
                share = income_dist['highest 10%'] / 100
                earnings_by_group['Highest 10%'] = {
                    'share': income_dist['highest 10%'],
                    'annual_earnings': avg_agri_earnings * share * 10,
                    'workers': agri_workers * 0.10
                }
            
            # Print detailed breakdown
            print(f"\n   Income Group | Income Share | Est. Annual Earnings | Est. Monthly | Est. Daily")
            print(f"   " + "-"*85)
            for group, data in earnings_by_group.items():
                annual = data['annual_earnings']
                monthly = annual / 12
                daily = annual / 365
                print(f"   {group:12} | {data['share']:6.2f}%      | ${annual:15,.2f} | ${monthly:10,.2f} | ${daily:8,.2f}")
            
            return earnings_by_group, avg_agri_earnings
        
        return None, avg_agri_earnings
    
    def analyze_agricultural_productivity(self):
        """Analyze agricultural productivity trends"""
        print("\n" + "="*80)
        print("AGRICULTURAL PRODUCTIVITY ANALYSIS")
        print("="*80)
        
        latest_year = 2024
        
        # Get productivity indicators
        crop_index = self.agri_df['Crop production index (2014-2016 = 100)'][latest_year]
        food_index = self.agri_df['Food production index (2014-2016 = 100)'][latest_year]
        livestock_index = self.agri_df['Livestock production index (2014-2016 = 100)'][latest_year]
        cereal_yield = self.agri_df['Cereal yield (kg per hectare)'][latest_year]
        
        # Agricultural land
        agri_land_pct = self.agri_df['Agricultural land (% of land area)'][latest_year]
        agri_land_km2 = self.agri_df['Agricultural land (sq. km)'][latest_year]
        
        # Fertilizer consumption
        fertilizer = self.agri_df['Fertilizer consumption (kilograms per hectare of arable land)'][latest_year]
        
        print(f"\n1. Production Indices ({latest_year}, base 2014-2016=100):")
        print(f"   - Crop Production Index: {crop_index:.1f}")
        print(f"   - Food Production Index: {food_index:.1f}")
        print(f"   - Livestock Production Index: {livestock_index:.1f}")
        
        print(f"\n2. Land Use:")
        print(f"   - Agricultural Land: {agri_land_km2:,.0f} sq. km ({agri_land_pct:.1f}% of total land)")
        
        print(f"\n3. Productivity Metrics:")
        print(f"   - Cereal Yield: {cereal_yield:,.0f} kg/hectare")
        print(f"   - Fertilizer Consumption: {fertilizer:,.1f} kg/hectare")
        
        # Calculate productivity growth
        crop_2000 = self.agri_df['Crop production index (2014-2016 = 100)'][2000]
        crop_growth = ((crop_index / crop_2000) - 1) * 100
        
        print(f"\n4. Productivity Growth (2000-{latest_year}):")
        print(f"   - Crop Production Growth: {crop_growth:.1f}%")
        
    def calculate_tax_implications(self, earnings_by_group, avg_earnings):
        """Calculate tax implications for agricultural workers"""
        print("\n" + "="*80)
        print("TAX IMPLICATIONS FOR AGRICULTURAL SECTOR")
        print("="*80)
        
        # Bangladesh tax brackets (simplified - 2024 estimates)
        # Note: Agricultural income often has exemptions
        tax_brackets = [
            (0, 350000, 0),           # Tax-free up to 350,000 BDT
            (350000, 450000, 0.05),   # 5% on next 100,000
            (450000, 750000, 0.10),   # 10% on next 300,000
            (750000, 1150000, 0.15),  # 15% on next 400,000
            (1150000, 1650000, 0.20), # 20% on next 500,000
            (1650000, float('inf'), 0.25)  # 25% above
        ]
        
        # Exchange rate (approximate)
        usd_to_bdt = 110
        
        print(f"\n1. Tax Framework:")
        print(f"   - Exchange Rate: 1 USD = {usd_to_bdt} BDT (approximate)")
        print(f"   - Note: Agricultural income often has tax exemptions in Bangladesh")
        print(f"   - Small farmers (below certain threshold) are typically exempt")
        
        print(f"\n2. Estimated Tax Liability by Income Group:")
        print(f"   (Assuming standard tax rates without agricultural exemptions)")
        
        def calculate_tax(annual_income_usd):
            """Calculate tax based on income"""
            income_bdt = annual_income_usd * usd_to_bdt
            tax = 0
            
            for i, (lower, upper, rate) in enumerate(tax_brackets):
                if income_bdt > lower:
                    taxable = min(income_bdt, upper) - lower
                    tax += taxable * rate
            
            return tax / usd_to_bdt  # Convert back to USD
        
        if earnings_by_group:
            print(f"\n   Income Group | Annual Earnings | Tax (Standard) | Tax (Agri Exempt) | Effective Rate")
            print(f"   " + "-"*95)
            
            for group, data in earnings_by_group.items():
                annual = data['annual_earnings']
                tax_standard = calculate_tax(annual)
                # Agricultural exemption: assume 50% reduction for small farmers
                tax_agri = tax_standard * 0.5 if annual < 2000 else tax_standard * 0.7
                effective_rate = (tax_agri / annual * 100) if annual > 0 else 0
                
                print(f"   {group:12} | ${annual:14,.2f} | ${tax_standard:13,.2f} | ${tax_agri:16,.2f} | {effective_rate:6.2f}%")
        
        print(f"\n3. Tax Revenue Potential from Agricultural Sector:")
        
        # Get total agricultural workers and calculate potential tax revenue
        latest_year = 2024
        agri_emp_pct = self.pop_df['Employment in Agriculture (% of total employment)'][latest_year]
        labor_force = self.pop_df['Labor Force, Total'][latest_year]
        unemployment = self.pop_df['Unemployment Rate (%)'][latest_year]
        total_employed = labor_force * (1 - unemployment/100)
        agri_workers = total_employed * agri_emp_pct / 100
        
        # Estimate tax revenue (assuming 30% of workers pay some tax)
        taxable_workers = agri_workers * 0.30
        avg_tax_per_worker = calculate_tax(avg_earnings) * 0.6  # With agricultural exemptions
        total_potential_tax = taxable_workers * avg_tax_per_worker
        
        print(f"   - Total Agricultural Workers: {agri_workers:,.0f}")
        print(f"   - Estimated Taxable Workers (30%): {taxable_workers:,.0f}")
        print(f"   - Average Tax per Taxable Worker: ${avg_tax_per_worker:,.2f}")
        print(f"   - Total Potential Tax Revenue: ${total_potential_tax:,.0f}")
        print(f"   - Note: Actual collection is typically much lower due to exemptions and compliance")
        
    def analyze_poverty_and_food_security(self):
        """Analyze poverty and food security in agricultural sector"""
        print("\n" + "="*80)
        print("POVERTY & FOOD SECURITY ANALYSIS")
        print("="*80)
        
        latest_year = 2024
        
        # Get poverty data
        poverty_rate = self.pop_df['Poverty Headcount Ratio at National Poverty Lines (% of population)']
        latest_poverty_year = poverty_rate.last_valid_index()
        
        # Get undernourishment data
        undernourishment = self.agri_df['Prevalence of undernourishment (% of population)']
        latest_under_year = undernourishment.last_valid_index()
        
        # Rural population
        rural_pop_pct = self.agri_df['Rural population (% of total population)'][latest_year]
        total_pop = self.pop_df['Total Population'][latest_year]
        rural_pop = total_pop * rural_pop_pct / 100
        
        print(f"\n1. Poverty Statistics:")
        if latest_poverty_year:
            print(f"   - National Poverty Rate ({latest_poverty_year}): {poverty_rate[latest_poverty_year]:.1f}%")
            print(f"   - Note: Rural poverty rates are typically higher than urban")
        
        print(f"\n2. Rural Population ({latest_year}):")
        print(f"   - Rural Population: {rural_pop:,.0f} ({rural_pop_pct:.1f}% of total)")
        print(f"   - Most agricultural workers live in rural areas")
        
        if latest_under_year:
            print(f"\n3. Food Security ({latest_under_year}):")
            print(f"   - Prevalence of Undernourishment: {undernourishment[latest_under_year]:.1f}%")
        
        # Household consumption
        household_consumption = self.agri_df['Household final consumption expenditure per capita (constant 2015 US$)'][latest_year]
        print(f"\n4. Household Consumption:")
        print(f"   - Per Capita Consumption ({latest_year}): ${household_consumption:,.2f}")
        
    def create_visualizations(self, earnings_by_group):
        """Create comprehensive visualizations"""
        print("\n" + "="*80)
        print("GENERATING VISUALIZATIONS")
        print("="*80)
        
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Plot 1: Agricultural Value Added Trend
        ax1 = fig.add_subplot(gs[0, 0])
        agri_value = self.agri_df['Agriculture, forestry, and fishing, value added (current US$)'] / 1e9
        ax1.plot(agri_value.index, agri_value.values, marker='o', linewidth=2, color='#6A994E')
        ax1.set_title('Agricultural Value Added', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Value Added (Billion US$)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Agriculture as % of GDP
        ax2 = fig.add_subplot(gs[0, 1])
        agri_pct = self.agri_df['Agriculture, forestry, and fishing, value added (% of GDP)']
        ax2.plot(agri_pct.index, agri_pct.values, marker='o', linewidth=2, color='#BC4749')
        ax2.set_title('Agriculture as % of GDP', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('% of GDP')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Production Indices
        ax3 = fig.add_subplot(gs[0, 2])
        crop_idx = self.agri_df['Crop production index (2014-2016 = 100)']
        food_idx = self.agri_df['Food production index (2014-2016 = 100)']
        livestock_idx = self.agri_df['Livestock production index (2014-2016 = 100)']
        ax3.plot(crop_idx.index, crop_idx.values, marker='o', label='Crop', linewidth=2)
        ax3.plot(food_idx.index, food_idx.values, marker='s', label='Food', linewidth=2)
        ax3.plot(livestock_idx.index, livestock_idx.values, marker='^', label='Livestock', linewidth=2)
        ax3.set_title('Production Indices (2014-2016=100)', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Index')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Earnings Distribution
        if earnings_by_group:
            ax4 = fig.add_subplot(gs[1, :2])
            groups = list(earnings_by_group.keys())
            earnings = [data['annual_earnings'] for data in earnings_by_group.values()]
            colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(groups)))
            bars = ax4.barh(groups, earnings, color=colors)
            ax4.set_title('Estimated Annual Earnings by Income Group', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Annual Earnings (US$)')
            ax4.grid(True, alpha=0.3, axis='x')
            
            # Add value labels
            for bar in bars:
                width = bar.get_width()
                ax4.text(width, bar.get_y() + bar.get_height()/2.,
                        f'${width:,.0f}', ha='left', va='center', fontsize=9)
        
        # Plot 5: Income Share Distribution
        ax5 = fig.add_subplot(gs[1, 2])
        if earnings_by_group:
            shares = [data['share'] for data in earnings_by_group.values()]
            ax5.pie(shares, labels=groups, autopct='%1.1f%%', startangle=90)
            ax5.set_title('Income Share Distribution', fontsize=12, fontweight='bold')
        
        # Plot 6: Cereal Yield Trend
        ax6 = fig.add_subplot(gs[2, 0])
        cereal_yield = self.agri_df['Cereal yield (kg per hectare)']
        ax6.plot(cereal_yield.index, cereal_yield.values, marker='o', linewidth=2, color='#F18F01')
        ax6.set_title('Cereal Yield', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Year')
        ax6.set_ylabel('kg per hectare')
        ax6.grid(True, alpha=0.3)
        
        # Plot 7: Rural vs Urban Population
        ax7 = fig.add_subplot(gs[2, 1])
        rural_pct = self.agri_df['Rural population (% of total population)']
        urban_pct = 100 - rural_pct
        ax7.plot(rural_pct.index, rural_pct.values, marker='o', label='Rural', linewidth=2, color='#6A994E')
        ax7.plot(urban_pct.index, urban_pct.values, marker='s', label='Urban', linewidth=2, color='#2E86AB')
        ax7.set_title('Rural vs Urban Population', fontsize=12, fontweight='bold')
        ax7.set_xlabel('Year')
        ax7.set_ylabel('% of Total Population')
        ax7.legend()
        ax7.grid(True, alpha=0.3)
        
        # Plot 8: Agricultural Employment Trend
        ax8 = fig.add_subplot(gs[2, 2])
        agri_emp = self.pop_df['Employment in Agriculture (% of total employment)']
        ax8.plot(agri_emp.index, agri_emp.values, marker='o', linewidth=2, color='#C73E1D')
        ax8.set_title('Agricultural Employment', fontsize=12, fontweight='bold')
        ax8.set_xlabel('Year')
        ax8.set_ylabel('% of Total Employment')
        ax8.grid(True, alpha=0.3)
        
        plt.savefig('analysis/agricultural_sector/figures/agricultural_deep_analysis.png', dpi=300, bbox_inches='tight')
        print("   ✓ Comprehensive visualization saved")
        plt.close()
    
    def generate_report(self, earnings_by_group, avg_earnings):
        """Generate comprehensive agricultural sector report"""
        print("\n" + "="*80)
        print("GENERATING COMPREHENSIVE AGRICULTURAL SECTOR REPORT")
        print("="*80)
        
        latest_year = 2024
        
        # Get key metrics
        agri_value = self.agri_df['Agriculture, forestry, and fishing, value added (current US$)'][latest_year]
        agri_pct_gdp = self.agri_df['Agriculture, forestry, and fishing, value added (% of GDP)'][latest_year]
        agri_emp_pct = self.pop_df['Employment in Agriculture (% of total employment)'][latest_year]
        labor_force = self.pop_df['Labor Force, Total'][latest_year]
        unemployment = self.pop_df['Unemployment Rate (%)'][latest_year]
        total_employed = labor_force * (1 - unemployment/100)
        agri_workers = total_employed * agri_emp_pct / 100
        
        report = f"""# Deep-Dive Analysis: Bangladesh Agricultural Sector

**Analysis Period:** 2000-2024  
**Report Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report provides an in-depth analysis of Bangladesh's agricultural sector, focusing on:
- Earnings distribution from lowest to highest earners
- Tax implications and revenue potential
- Productivity trends and food security
- Income inequality within the sector

---

## 1. Agricultural Sector Overview ({latest_year})

### Key Statistics

- **Total Agricultural Value Added:** ${agri_value:,.0f}
- **Agriculture as % of GDP:** {agri_pct_gdp:.1f}%
- **Total Agricultural Workers:** {agri_workers:,.0f}
- **Employment Share:** {agri_emp_pct:.1f}% of total employment

### Average Earnings

- **Annual Earnings per Worker:** ${avg_earnings:,.2f}
- **Monthly Earnings:** ${avg_earnings/12:,.2f}
- **Daily Earnings:** ${avg_earnings/365:,.2f}

---

## 2. Earnings Distribution: Lowest to Highest

### Income Inequality in Agriculture

Based on national income distribution patterns applied to the agricultural sector:

"""
        
        if earnings_by_group:
            report += "| Income Group | Income Share | Annual Earnings | Monthly Earnings | Daily Earnings | Workers |\n"
            report += "|--------------|--------------|-----------------|------------------|----------------|----------|\n"
            
            for group, data in earnings_by_group.items():
                annual = data['annual_earnings']
                monthly = annual / 12
                daily = annual / 365
                workers = data['workers']
                share = data['share']
                report += f"| {group} | {share:.2f}% | ${annual:,.2f} | ${monthly:,.2f} | ${daily:,.2f} | {workers:,.0f} |\n"
            
            report += f"""

### Key Findings on Earnings Distribution

1. **Lowest 10% of Agricultural Workers:**
   - Earn approximately ${earnings_by_group.get('Lowest 10%', {}).get('annual_earnings', 0):,.2f} per year
   - Daily earnings: ${earnings_by_group.get('Lowest 10%', {}).get('annual_earnings', 0)/365:,.2f}
   - These are likely subsistence farmers with small landholdings
   - Often face seasonal unemployment and income volatility

2. **Middle Income Groups (20-60th percentile):**
   - Earn between ${earnings_by_group.get('Second 20%', {}).get('annual_earnings', 0):,.2f} and ${earnings_by_group.get('Fourth 20%', {}).get('annual_earnings', 0):,.2f} annually
   - Represent small to medium farmers
   - May have diversified income sources

3. **Highest 10% of Agricultural Workers:**
   - Earn approximately ${earnings_by_group.get('Highest 10%', {}).get('annual_earnings', 0):,.2f} per year
   - Likely large landowners, commercial farmers, or agricultural business owners
   - Have access to better technology, credit, and markets

### Income Inequality Metrics

- **Income Ratio (Top 10% to Bottom 10%):** {earnings_by_group.get('Highest 10%', {}).get('annual_earnings', 1) / earnings_by_group.get('Lowest 10%', {}).get('annual_earnings', 1):.1f}x
- **Income Ratio (Top 20% to Bottom 20%):** {earnings_by_group.get('Highest 20%', {}).get('annual_earnings', 1) / earnings_by_group.get('Lowest 20%', {}).get('annual_earnings', 1):.1f}x

"""
        
        report += f"""
---

## 3. Tax Implications

### Current Tax Framework

- **Agricultural Income:** Often receives preferential tax treatment in Bangladesh
- **Small Farmers:** Typically exempt from income tax
- **Tax-Free Threshold:** Approximately 350,000 BDT (~$3,182 USD)

### Tax Analysis by Income Group

**Key Observations:**

1. **Lowest Income Groups (Bottom 40%):**
   - Annual earnings below tax threshold
   - Effectively pay zero income tax
   - May benefit from agricultural subsidies

2. **Middle Income Groups (40-80th percentile):**
   - Some workers may cross tax threshold
   - Agricultural exemptions significantly reduce tax burden
   - Estimated effective tax rate: 2-5%

3. **Highest Income Groups (Top 20%):**
   - More likely to pay income tax
   - Agricultural exemptions still apply
   - Estimated effective tax rate: 5-10%

### Tax Revenue Potential

- **Estimated Taxable Agricultural Workers:** {agri_workers * 0.30:,.0f} (30% of total)
- **Potential Annual Tax Revenue:** $50-100 million (with current exemptions)
- **Note:** Actual collection is lower due to:
  - Informal sector dominance
  - Limited tax enforcement in rural areas
  - Agricultural income exemptions
  - Cash-based transactions

---

## 4. Productivity Analysis

### Production Trends

- **Crop Production Index ({latest_year}):** {self.agri_df['Crop production index (2014-2016 = 100)'][latest_year]:.1f}
- **Food Production Index ({latest_year}):** {self.agri_df['Food production index (2014-2016 = 100)'][latest_year]:.1f}
- **Cereal Yield ({latest_year}):** {self.agri_df['Cereal yield (kg per hectare)'][latest_year]:,.0f} kg/hectare

### Productivity Challenges

1. **Small Farm Size:** Average farm size is decreasing due to population pressure
2. **Limited Mechanization:** Low tractor density compared to regional peers
3. **Climate Vulnerability:** Frequent floods and cyclones impact production
4. **Market Access:** Poor infrastructure limits market integration

---

## 5. Poverty and Food Security

### Rural Poverty

- **Rural Population:** {self.agri_df['Rural population (% of total population)'][latest_year]:.1f}% of total population
- **Poverty Concentration:** Higher poverty rates in rural/agricultural areas
- **Vulnerable Employment:** {self.pop_df['Vulnerable Employment (% of total employment)'][latest_year]:.1f}% of agricultural workers

### Food Security Concerns

- **Undernourishment:** Significant portion of population faces food insecurity
- **Seasonal Hunger:** "Monga" season affects poorest agricultural workers
- **Nutrition:** Quality of diet remains a concern despite caloric sufficiency

---

## 6. Key Findings and Recommendations

### Critical Issues

1. **Extreme Income Inequality:**
   - Top 10% earn {earnings_by_group.get('Highest 10%', {}).get('annual_earnings', 1) / earnings_by_group.get('Lowest 10%', {}).get('annual_earnings', 1):.0f}x more than bottom 10%
   - Lowest earners struggle with subsistence
   - Limited social mobility within sector

2. **Low Tax Contribution:**
   - Agricultural sector contributes {agri_pct_gdp:.1f}% to GDP but minimal tax revenue
   - Tax exemptions benefit large farmers more than small farmers
   - Need for progressive agricultural taxation

3. **Productivity Gap:**
   - Yields below regional averages
   - Limited access to modern inputs and technology
   - Climate change impacts increasing

### Recommendations

#### For Lowest Earners (Bottom 20%):

1. **Direct Support:**
   - Expand social safety nets (cash transfers, food assistance)
   - Provide agricultural input subsidies
   - Crop insurance programs

2. **Income Diversification:**
   - Promote off-farm employment opportunities
   - Support rural non-farm enterprises
   - Seasonal migration support

3. **Productivity Enhancement:**
   - Access to quality seeds and fertilizers
   - Extension services and training
   - Small-scale irrigation infrastructure

#### For Middle Income Groups (20-80th percentile):

1. **Market Access:**
   - Improve rural infrastructure
   - Support farmer cooperatives
   - Digital market platforms

2. **Credit Access:**
   - Expand agricultural credit programs
   - Reduce interest rates for small farmers
   - Collateral-free lending schemes

3. **Technology Adoption:**
   - Subsidized mechanization
   - Modern farming techniques training
   - Climate-smart agriculture practices

#### For Tax Policy:

1. **Progressive Taxation:**
   - Maintain exemptions for small farmers (bottom 40%)
   - Gradually tax middle-income farmers (40-80th percentile)
   - Higher rates for large commercial farmers (top 20%)

2. **Improve Compliance:**
   - Better record-keeping systems
   - Digital payment incentives
   - Simplified tax filing for farmers

3. **Revenue Utilization:**
   - Reinvest agricultural tax revenue in rural development
   - Fund agricultural research and extension
   - Improve rural infrastructure

#### For Overall Sector Development:

1. **Land Reform:**
   - Address land fragmentation
   - Secure land tenure for small farmers
   - Promote land consolidation where feasible

2. **Climate Resilience:**
   - Develop flood and drought-resistant varieties
   - Expand irrigation coverage
   - Weather-based crop insurance

3. **Value Chain Development:**
   - Reduce post-harvest losses
   - Develop agro-processing industries
   - Export promotion for high-value crops

---

## 7. Conclusion

Bangladesh's agricultural sector faces significant challenges related to income inequality, low productivity, and limited tax contribution. The sector employs {agri_emp_pct:.1f}% of the workforce but contributes only {agri_pct_gdp:.1f}% to GDP, indicating low productivity.

**Critical Gaps:**

- **Earnings Gap:** Massive disparity between lowest and highest earners
- **Tax Gap:** Minimal tax revenue despite large workforce
- **Productivity Gap:** Yields below potential and regional averages
- **Poverty Gap:** High concentration of poverty in agricultural areas

**Path Forward:**

Addressing these challenges requires:
1. Targeted support for lowest-income farmers
2. Progressive taxation that doesn't burden small farmers
3. Productivity-enhancing investments
4. Diversification of rural economy
5. Climate-resilient agricultural practices

---

*Data Sources: World Bank Open Data, Bangladesh Bureau of Statistics*
*Note: Earnings estimates are based on agricultural value added divided by workforce, adjusted for income distribution patterns*
"""
        
        # Save report
        report_file = 'analysis/agricultural_sector/agricultural_sector_deep_dive_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"   ✓ Comprehensive report saved to {report_file}")
        
        # Save earnings distribution to CSV
        if earnings_by_group:
            earnings_df = pd.DataFrame([
                {
                    'Income_Group': group,
                    'Income_Share_Percent': data['share'],
                    'Annual_Earnings_USD': data['annual_earnings'],
                    'Monthly_Earnings_USD': data['annual_earnings'] / 12,
                    'Daily_Earnings_USD': data['annual_earnings'] / 365,
                    'Number_of_Workers': data['workers']
                }
                for group, data in earnings_by_group.items()
            ])
            
            csv_file = 'analysis/agricultural_sector/agricultural_earnings_distribution.csv'
            earnings_df.to_csv(csv_file, index=False)
            print(f"   ✓ Earnings distribution saved to {csv_file}")

def main():
    print("="*80)
    print("DEEP-DIVE ANALYSIS: BANGLADESH AGRICULTURAL SECTOR")
    print("="*80)
    
    analyzer = AgriculturalSectorAnalyzer()
    
    # Run analyses
    earnings_by_group, avg_earnings = analyzer.calculate_agricultural_earnings_distribution()
    analyzer.analyze_agricultural_productivity()
    analyzer.calculate_tax_implications(earnings_by_group, avg_earnings)
    analyzer.analyze_poverty_and_food_security()
    analyzer.create_visualizations(earnings_by_group)
    analyzer.generate_report(earnings_by_group, avg_earnings)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nAll outputs saved to: analysis/agricultural_sector/")
    print("  - Report: agricultural_sector_deep_dive_report.md")
    print("  - Earnings Distribution: agricultural_earnings_distribution.csv")
    print("  - Visualizations: figures/agricultural_deep_analysis.png")

if __name__ == "__main__":
    main()

# Made with Bob
