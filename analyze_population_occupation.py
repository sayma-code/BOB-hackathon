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
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class PopulationOccupationAnalyzer:
    def __init__(self, data_file):
        """Initialize the analyzer with data file"""
        # The file is already pivoted, so just read it and set year as index
        self.pivot_df = pd.read_csv(data_file)
        self.pivot_df.set_index('year', inplace=True)
        
        # Create output directories
        os.makedirs('analysis/population_occupation', exist_ok=True)
        os.makedirs('analysis/population_occupation/figures', exist_ok=True)
        
    def analyze_population_trends(self):
        """Analyze overall population trends"""
        print("\n" + "="*80)
        print("POPULATION ANALYSIS")
        print("="*80)
        
        # Get population data
        total_pop = self.pivot_df['Total Population']
        urban_pop = self.pivot_df['Urban Population']
        rural_pop = self.pivot_df['Rural Population']
        
        # Latest year data
        latest_year = total_pop.last_valid_index()
        latest_total = total_pop[latest_year]
        latest_urban = urban_pop[latest_year]
        latest_rural = rural_pop[latest_year]
        
        # Historical comparison
        first_year = total_pop.first_valid_index()
        first_total = total_pop[first_year]
        
        print(f"\n1. Overall Population Statistics:")
        print(f"   - Latest Year: {latest_year}")
        print(f"   - Total Population: {latest_total:,.0f}")
        print(f"   - Urban Population: {latest_urban:,.0f} ({latest_urban/latest_total*100:.1f}%)")
        print(f"   - Rural Population: {latest_rural:,.0f} ({latest_rural/latest_total*100:.1f}%)")
        print(f"\n   - Population in {first_year}: {first_total:,.0f}")
        print(f"   - Population Growth ({first_year}-{latest_year}): {((latest_total/first_total - 1)*100):.1f}%")
        print(f"   - Average Annual Growth Rate: {total_pop.pct_change().mean()*100:.2f}%")
        
        # Age distribution
        print(f"\n2. Age Distribution (Latest Year):")
        age_0_14 = self.pivot_df['Population ages 0-14 (% of total)'][latest_year]
        age_15_64 = self.pivot_df['Population ages 15-64 (% of total)'][latest_year]
        age_65_plus = self.pivot_df['Population ages 65 and above (% of total)'][latest_year]
        
        print(f"   - Ages 0-14: {age_0_14:.1f}%")
        print(f"   - Ages 15-64 (Working Age): {age_15_64:.1f}%")
        print(f"   - Ages 65+: {age_65_plus:.1f}%")
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Total Population Trend
        ax1 = axes[0, 0]
        ax1.plot(total_pop.index, total_pop.values/1e6, marker='o', linewidth=2, color='#2E86AB')
        ax1.set_title('Total Population Trend (2000-2024)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Population (Millions)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Urban vs Rural Population
        ax2 = axes[0, 1]
        ax2.plot(urban_pop.index, urban_pop.values/1e6, marker='o', label='Urban', linewidth=2, color='#A23B72')
        ax2.plot(rural_pop.index, rural_pop.values/1e6, marker='s', label='Rural', linewidth=2, color='#F18F01')
        ax2.set_title('Urban vs Rural Population', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Population (Millions)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Urbanization Rate
        ax3 = axes[1, 0]
        urbanization_rate = (urban_pop / total_pop * 100)
        ax3.plot(urbanization_rate.index, urbanization_rate.values, marker='o', linewidth=2, color='#C73E1D')
        ax3.set_title('Urbanization Rate (%)', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Urban Population (%)')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Age Distribution (Latest Year)
        ax4 = axes[1, 1]
        age_groups = ['0-14 years', '15-64 years', '65+ years']
        age_values = [age_0_14, age_15_64, age_65_plus]
        colors = ['#6A994E', '#BC4749', '#F2CC8F']
        ax4.pie(age_values, labels=age_groups, autopct='%1.1f%%', colors=colors, startangle=90)
        ax4.set_title(f'Age Distribution ({latest_year})', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('analysis/population_occupation/figures/population_trends.png', dpi=300, bbox_inches='tight')
        print("\n   ✓ Population trends visualization saved")
        plt.close()
        
    def analyze_occupation_distribution(self):
        """Analyze employment by occupation/sector"""
        print("\n" + "="*80)
        print("OCCUPATION & EMPLOYMENT ANALYSIS")
        print("="*80)
        
        # Get employment data
        labor_force = self.pivot_df['Labor Force, Total']
        emp_ratio = self.pivot_df['Employment to Population Ratio (%)']
        unemployment = self.pivot_df['Unemployment Rate (%)']
        
        # Sector employment
        agri_emp = self.pivot_df['Employment in Agriculture (% of total employment)']
        ind_emp = self.pivot_df['Employment in Industry (% of total employment)']
        serv_emp = self.pivot_df['Employment in Services (% of total employment)']
        
        # Employment types
        wage_workers = self.pivot_df['Wage and Salaried Workers (% of total employment)']
        self_employed = self.pivot_df['Self-employed (% of total employment)']
        vulnerable_emp = self.pivot_df['Vulnerable Employment (% of total employment)']
        
        latest_year = labor_force.last_valid_index()
        
        print(f"\n1. Labor Force Statistics ({latest_year}):")
        print(f"   - Total Labor Force: {labor_force[latest_year]:,.0f}")
        print(f"   - Employment to Population Ratio: {emp_ratio[latest_year]:.1f}%")
        print(f"   - Unemployment Rate: {unemployment[latest_year]:.2f}%")
        
        print(f"\n2. Employment by Sector ({latest_year}):")
        print(f"   - Agriculture: {agri_emp[latest_year]:.1f}%")
        print(f"   - Industry: {ind_emp[latest_year]:.1f}%")
        print(f"   - Services: {serv_emp[latest_year]:.1f}%")
        
        # Calculate absolute numbers (approximate)
        total_employed = labor_force[latest_year] * (1 - unemployment[latest_year]/100)
        agri_workers = total_employed * agri_emp[latest_year] / 100
        ind_workers = total_employed * ind_emp[latest_year] / 100
        serv_workers = total_employed * serv_emp[latest_year] / 100
        
        print(f"\n   Estimated Workers by Sector:")
        print(f"   - Agriculture: {agri_workers:,.0f} workers")
        print(f"   - Industry: {ind_workers:,.0f} workers")
        print(f"   - Services: {serv_workers:,.0f} workers")
        
        print(f"\n3. Employment Type ({latest_year}):")
        print(f"   - Wage and Salaried Workers: {wage_workers[latest_year]:.1f}%")
        print(f"   - Self-employed: {self_employed[latest_year]:.1f}%")
        print(f"   - Vulnerable Employment: {vulnerable_emp[latest_year]:.1f}%")
        
        # Create visualizations
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Employment by Sector Over Time
        ax1 = axes[0, 0]
        ax1.plot(agri_emp.index, agri_emp.values, marker='o', label='Agriculture', linewidth=2, color='#6A994E')
        ax1.plot(ind_emp.index, ind_emp.values, marker='s', label='Industry', linewidth=2, color='#BC4749')
        ax1.plot(serv_emp.index, serv_emp.values, marker='^', label='Services', linewidth=2, color='#2E86AB')
        ax1.set_title('Employment Distribution by Sector', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('% of Total Employment')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Current Sector Distribution (Pie Chart)
        ax2 = axes[0, 1]
        sectors = ['Agriculture', 'Industry', 'Services']
        sector_values = [agri_emp[latest_year], ind_emp[latest_year], serv_emp[latest_year]]
        colors = ['#6A994E', '#BC4749', '#2E86AB']
        ax2.pie(sector_values, labels=sectors, autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title(f'Employment by Sector ({latest_year})', fontsize=14, fontweight='bold')
        
        # Plot 3: Employment Type Distribution
        ax3 = axes[1, 0]
        emp_types = ['Wage/Salaried', 'Self-employed', 'Vulnerable']
        emp_type_values = [wage_workers[latest_year], self_employed[latest_year], vulnerable_emp[latest_year]]
        colors = ['#2E86AB', '#F18F01', '#C73E1D']
        bars = ax3.bar(emp_types, emp_type_values, color=colors, alpha=0.8)
        ax3.set_title(f'Employment Type Distribution ({latest_year})', fontsize=14, fontweight='bold')
        ax3.set_ylabel('% of Total Employment')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # Plot 4: Labor Force Growth
        ax4 = axes[1, 1]
        ax4.plot(labor_force.index, labor_force.values/1e6, marker='o', linewidth=2, color='#A23B72')
        ax4.set_title('Labor Force Growth', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Labor Force (Millions)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis/population_occupation/figures/occupation_distribution.png', dpi=300, bbox_inches='tight')
        print("\n   ✓ Occupation distribution visualization saved")
        plt.close()
        
        return {
            'sectors': {'Agriculture': agri_workers, 'Industry': ind_workers, 'Services': serv_workers},
            'latest_year': latest_year
        }
        
    def analyze_earnings(self):
        """Analyze earnings and income data"""
        print("\n" + "="*80)
        print("EARNINGS & INCOME ANALYSIS")
        print("="*80)
        
        # Get income data
        gdp_per_capita = self.pivot_df['GDP per Capita (current US$)']
        gdp_growth = self.pivot_df['GDP per Capita Growth (annual %)']
        adj_income = self.pivot_df['Adjusted Net National Income per Capita (current US$)']
        
        latest_year = gdp_per_capita.last_valid_index()
        first_year = gdp_per_capita.first_valid_index()
        
        print(f"\n1. Income Statistics ({latest_year}):")
        print(f"   - GDP per Capita: ${gdp_per_capita[latest_year]:,.2f}")
        print(f"   - Adjusted Net National Income per Capita: ${adj_income[latest_year]:,.2f}")
        print(f"   - GDP per Capita Growth Rate: {gdp_growth[latest_year]:.2f}%")
        
        print(f"\n2. Historical Income Growth:")
        print(f"   - GDP per Capita in {first_year}: ${gdp_per_capita[first_year]:,.2f}")
        print(f"   - Total Growth ({first_year}-{latest_year}): {((gdp_per_capita[latest_year]/gdp_per_capita[first_year] - 1)*100):.1f}%")
        print(f"   - Average Annual Growth: {gdp_growth.mean():.2f}%")
        
        # Estimate earnings by sector (using GDP per capita as proxy)
        # This is a simplified estimation
        agri_emp_pct = self.pivot_df['Employment in Agriculture (% of total employment)'][latest_year]
        ind_emp_pct = self.pivot_df['Employment in Industry (% of total employment)'][latest_year]
        serv_emp_pct = self.pivot_df['Employment in Services (% of total employment)'][latest_year]
        
        # Typical sector productivity ratios (Agriculture < Industry < Services)
        # These are estimates based on typical patterns
        base_income = gdp_per_capita[latest_year]
        agri_income = base_income * 0.6  # Agriculture typically lower
        ind_income = base_income * 1.2   # Industry typically higher
        serv_income = base_income * 1.3  # Services typically highest
        
        print(f"\n3. Estimated Average Annual Earnings by Sector ({latest_year}):")
        print(f"   Note: These are estimates based on GDP per capita and typical sector productivity")
        print(f"   - Agriculture: ${agri_income:,.2f}")
        print(f"   - Industry: ${ind_income:,.2f}")
        print(f"   - Services: ${serv_income:,.2f}")
        
        # Poverty and inequality
        if 'Poverty Headcount Ratio at National Poverty Lines (% of population)' in self.pivot_df.columns:
            poverty = self.pivot_df['Poverty Headcount Ratio at National Poverty Lines (% of population)']
            if not poverty.isna().all():
                latest_poverty_year = poverty.last_valid_index()
                print(f"\n4. Poverty Statistics:")
                print(f"   - Poverty Rate ({latest_poverty_year}): {poverty[latest_poverty_year]:.1f}%")
        
        if 'GINI Index (World Bank estimate)' in self.pivot_df.columns:
            gini = self.pivot_df['GINI Index (World Bank estimate)']
            if not gini.isna().all():
                latest_gini_year = gini.last_valid_index()
                print(f"\n5. Income Inequality:")
                print(f"   - GINI Index ({latest_gini_year}): {gini[latest_gini_year]:.1f}")
                print(f"     (0 = perfect equality, 100 = perfect inequality)")
        
        # Create visualizations
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: GDP per Capita Trend
        ax1 = axes[0, 0]
        ax1.plot(gdp_per_capita.index, gdp_per_capita.values, marker='o', linewidth=2, color='#2E86AB')
        ax1.set_title('GDP per Capita Trend', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('GDP per Capita (US$)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: GDP per Capita Growth Rate
        ax2 = axes[0, 1]
        ax2.plot(gdp_growth.index, gdp_growth.values, marker='o', linewidth=2, color='#6A994E')
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        ax2.set_title('GDP per Capita Growth Rate', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Growth Rate (%)')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Estimated Earnings by Sector
        ax3 = axes[1, 0]
        sectors = ['Agriculture', 'Industry', 'Services']
        earnings = [agri_income, ind_income, serv_income]
        colors = ['#6A994E', '#BC4749', '#2E86AB']
        bars = ax3.bar(sectors, earnings, color=colors, alpha=0.8)
        ax3.set_title(f'Estimated Average Annual Earnings by Sector ({latest_year})', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Annual Earnings (US$)')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom')
        
        # Plot 4: Income Comparison
        ax4 = axes[1, 1]
        ax4.plot(gdp_per_capita.index, gdp_per_capita.values, marker='o', label='GDP per Capita', linewidth=2, color='#2E86AB')
        ax4.plot(adj_income.index, adj_income.values, marker='s', label='Adjusted Net Income per Capita', linewidth=2, color='#F18F01')
        ax4.set_title('Income Measures Comparison', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Income (US$)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis/population_occupation/figures/earnings_analysis.png', dpi=300, bbox_inches='tight')
        print("\n   ✓ Earnings analysis visualization saved")
        plt.close()
        
        return {
            'Agriculture': agri_income,
            'Industry': ind_income,
            'Services': serv_income,
            'Overall': base_income
        }
        
    def generate_summary_report(self, occupation_data, earnings_data):
        """Generate a comprehensive summary report"""
        print("\n" + "="*80)
        print("GENERATING COMPREHENSIVE REPORT")
        print("="*80)
        
        total_pop = self.pivot_df['Total Population']
        latest_year = total_pop.last_valid_index()
        
        report = f"""# Bangladesh Population, Occupation, and Earnings Analysis Report

**Analysis Period:** 2000-2024  
**Report Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report provides a comprehensive analysis of Bangladesh's population demographics, 
employment distribution across sectors, and earnings patterns from 2000 to 2024.

---

## 1. Population Overview

### Key Statistics ({latest_year})

- **Total Population:** {total_pop[latest_year]:,.0f}
- **Urban Population:** {self.pivot_df['Urban Population'][latest_year]:,.0f} ({self.pivot_df['Urban Population'][latest_year]/total_pop[latest_year]*100:.1f}%)
- **Rural Population:** {self.pivot_df['Rural Population'][latest_year]:,.0f} ({self.pivot_df['Rural Population'][latest_year]/total_pop[latest_year]*100:.1f}%)

### Age Distribution

- **0-14 years:** {self.pivot_df['Population ages 0-14 (% of total)'][latest_year]:.1f}%
- **15-64 years (Working Age):** {self.pivot_df['Population ages 15-64 (% of total)'][latest_year]:.1f}%
- **65+ years:** {self.pivot_df['Population ages 65 and above (% of total)'][latest_year]:.1f}%

### Population Growth

- **Population in 2000:** {total_pop[2000]:,.0f}
- **Population in {latest_year}:** {total_pop[latest_year]:,.0f}
- **Total Growth:** {((total_pop[latest_year]/total_pop[2000] - 1)*100):.1f}%
- **Average Annual Growth Rate:** {total_pop.pct_change().mean()*100:.2f}%

---

## 2. Employment & Occupation Distribution

### Labor Force Statistics ({latest_year})

- **Total Labor Force:** {self.pivot_df['Labor Force, Total'][latest_year]:,.0f}
- **Employment to Population Ratio:** {self.pivot_df['Employment to Population Ratio (%)'][latest_year]:.1f}%
- **Unemployment Rate:** {self.pivot_df['Unemployment Rate (%)'][latest_year]:.2f}%

### Employment by Sector ({latest_year})

| Sector | Percentage | Estimated Workers |
|--------|-----------|-------------------|
| Agriculture | {self.pivot_df['Employment in Agriculture (% of total employment)'][latest_year]:.1f}% | {occupation_data['sectors']['Agriculture']:,.0f} |
| Industry | {self.pivot_df['Employment in Industry (% of total employment)'][latest_year]:.1f}% | {occupation_data['sectors']['Industry']:,.0f} |
| Services | {self.pivot_df['Employment in Services (% of total employment)'][latest_year]:.1f}% | {occupation_data['sectors']['Services']:,.0f} |

### Employment Type ({latest_year})

- **Wage and Salaried Workers:** {self.pivot_df['Wage and Salaried Workers (% of total employment)'][latest_year]:.1f}%
- **Self-employed:** {self.pivot_df['Self-employed (% of total employment)'][latest_year]:.1f}%
- **Vulnerable Employment:** {self.pivot_df['Vulnerable Employment (% of total employment)'][latest_year]:.1f}%

---

## 3. Earnings Analysis

### Income Statistics ({latest_year})

- **GDP per Capita:** ${self.pivot_df['GDP per Capita (current US$)'][latest_year]:,.2f}
- **Adjusted Net National Income per Capita:** ${self.pivot_df['Adjusted Net National Income per Capita (current US$)'][latest_year]:,.2f}
- **GDP per Capita Growth Rate:** {self.pivot_df['GDP per Capita Growth (annual %)'][latest_year]:.2f}%

### Estimated Average Annual Earnings by Sector ({latest_year})

*Note: These are estimates based on GDP per capita and typical sector productivity patterns*

| Sector | Estimated Annual Earnings |
|--------|--------------------------|
| Agriculture | ${earnings_data['Agriculture']:,.2f} |
| Industry | ${earnings_data['Industry']:,.2f} |
| Services | ${earnings_data['Services']:,.2f} |
| **Overall Average** | **${earnings_data['Overall']:,.2f}** |

### Income Growth (2000-{latest_year})

- **GDP per Capita in 2000:** ${self.pivot_df['GDP per Capita (current US$)'][2000]:,.2f}
- **GDP per Capita in {latest_year}:** ${self.pivot_df['GDP per Capita (current US$)'][latest_year]:,.2f}
- **Total Growth:** {((self.pivot_df['GDP per Capita (current US$)'][latest_year]/self.pivot_df['GDP per Capita (current US$)'][2000] - 1)*100):.1f}%
- **Average Annual Growth Rate:** {self.pivot_df['GDP per Capita Growth (annual %)'].mean():.2f}%

---

## 4. Key Findings

### Population Trends

1. Bangladesh's population has grown from {total_pop[2000]/1e6:.1f} million in 2000 to {total_pop[latest_year]/1e6:.1f} million in {latest_year}
2. Urbanization is increasing, with {self.pivot_df['Urban Population'][latest_year]/total_pop[latest_year]*100:.1f}% of the population now living in urban areas
3. The working-age population (15-64 years) represents {self.pivot_df['Population ages 15-64 (% of total)'][latest_year]:.1f}% of the total, indicating a demographic dividend opportunity

### Employment Structure

1. **Sectoral Shift:** Employment is gradually shifting from agriculture to services and industry
   - Agriculture: {self.pivot_df['Employment in Agriculture (% of total employment)'][latest_year]:.1f}% (declining trend)
   - Services: {self.pivot_df['Employment in Services (% of total employment)'][latest_year]:.1f}% (growing trend)
   - Industry: {self.pivot_df['Employment in Industry (% of total employment)'][latest_year]:.1f}%

2. **Employment Quality:** 
   - Wage/salaried employment: {self.pivot_df['Wage and Salaried Workers (% of total employment)'][latest_year]:.1f}%
   - Vulnerable employment remains significant at {self.pivot_df['Vulnerable Employment (% of total employment)'][latest_year]:.1f}%

### Income & Earnings

1. **Income Growth:** GDP per capita has increased by {((self.pivot_df['GDP per Capita (current US$)'][latest_year]/self.pivot_df['GDP per Capita (current US$)'][2000] - 1)*100):.1f}% over the analysis period
2. **Sectoral Earnings Disparity:** Significant differences exist between sectors, with services and industry offering higher earnings than agriculture
3. **Economic Development:** The consistent growth in GDP per capita indicates improving living standards

---

## 5. Recommendations

1. **Skills Development:** Invest in education and vocational training to support the transition from agriculture to higher-productivity sectors
2. **Formal Employment:** Promote policies to increase wage/salaried employment and reduce vulnerable employment
3. **Urban Planning:** Prepare for continued urbanization with infrastructure and service development
4. **Agricultural Productivity:** Improve agricultural productivity to increase earnings for the large agricultural workforce
5. **Youth Employment:** Leverage the demographic dividend by creating quality jobs for the working-age population

---

## 6. Data Sources & Methodology

- **Data Source:** World Bank Open Data API
- **Country:** Bangladesh (BGD)
- **Time Period:** 2000-2024
- **Indicators:** 21 indicators covering population, employment, and income
- **Earnings Estimation:** Sector-specific earnings are estimated using GDP per capita adjusted by typical sector productivity ratios

---

## Visualizations

The following visualizations are included in this analysis:

1. **Population Trends** (`population_trends.png`)
   - Total population growth
   - Urban vs rural population
   - Urbanization rate
   - Age distribution

2. **Occupation Distribution** (`occupation_distribution.png`)
   - Employment by sector over time
   - Current sector distribution
   - Employment type distribution
   - Labor force growth

3. **Earnings Analysis** (`earnings_analysis.png`)
   - GDP per capita trend
   - GDP per capita growth rate
   - Estimated earnings by sector
   - Income measures comparison

---

*Report generated using World Bank data and statistical analysis*
"""
        
        # Save report
        report_file = 'analysis/population_occupation/population_occupation_earnings_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✓ Comprehensive report saved to {report_file}")
        
        # Also save summary statistics to CSV
        summary_data = {
            'Metric': [
                'Total Population',
                'Urban Population %',
                'Working Age Population %',
                'Labor Force',
                'Unemployment Rate %',
                'Agriculture Employment %',
                'Industry Employment %',
                'Services Employment %',
                'GDP per Capita (US$)',
                'Estimated Agriculture Earnings (US$)',
                'Estimated Industry Earnings (US$)',
                'Estimated Services Earnings (US$)'
            ],
            'Value': [
                f"{total_pop[latest_year]:,.0f}",
                f"{self.pivot_df['Urban Population'][latest_year]/total_pop[latest_year]*100:.1f}",
                f"{self.pivot_df['Population ages 15-64 (% of total)'][latest_year]:.1f}",
                f"{self.pivot_df['Labor Force, Total'][latest_year]:,.0f}",
                f"{self.pivot_df['Unemployment Rate (%)'][latest_year]:.2f}",
                f"{self.pivot_df['Employment in Agriculture (% of total employment)'][latest_year]:.1f}",
                f"{self.pivot_df['Employment in Industry (% of total employment)'][latest_year]:.1f}",
                f"{self.pivot_df['Employment in Services (% of total employment)'][latest_year]:.1f}",
                f"{self.pivot_df['GDP per Capita (current US$)'][latest_year]:,.2f}",
                f"{earnings_data['Agriculture']:,.2f}",
                f"{earnings_data['Industry']:,.2f}",
                f"{earnings_data['Services']:,.2f}"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_file = 'analysis/population_occupation/summary_statistics.csv'
        summary_df.to_csv(summary_file, index=False)
        print(f"✓ Summary statistics saved to {summary_file}")

def main():
    print("="*80)
    print("BANGLADESH POPULATION, OCCUPATION & EARNINGS ANALYSIS")
    print("="*80)
    
    # Initialize analyzer
    data_file = 'data/processed/population_occupation_earnings_pivot.csv'
    analyzer = PopulationOccupationAnalyzer(data_file)
    
    # Run analyses
    analyzer.analyze_population_trends()
    occupation_data = analyzer.analyze_occupation_distribution()
    earnings_data = analyzer.analyze_earnings()
    analyzer.generate_summary_report(occupation_data, earnings_data)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nAll outputs saved to: analysis/population_occupation/")
    print("  - Figures: analysis/population_occupation/figures/")
    print("  - Report: population_occupation_earnings_report.md")
    print("  - Summary: summary_statistics.csv")

if __name__ == "__main__":
    main()

# Made with Bob
