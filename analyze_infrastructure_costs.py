"""
Global Infrastructure Cost Comparison Analysis
Comparing Bangladesh's major infrastructure projects with global benchmarks
"""

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

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (18, 12)
plt.rcParams['font.size'] = 10

# Create output directories
os.makedirs('analysis/infrastructure_costs', exist_ok=True)
os.makedirs('analysis/infrastructure_costs/figures', exist_ok=True)

# BRIDGES DATABASE
bridges_data = {
    'name': ['Padma Bridge', 'Hong Kong-Zhuhai-Macau Bridge', 'Danyang-Kunshan Grand Bridge', 
             'Bandra-Worli Sea Link', 'Bogibeel Bridge', 'Akashi Kaikyo Bridge', 'Great Seto Bridge',
             'Incheon Bridge', 'Øresund Bridge', 'Penang Bridge'],
    'country': ['Bangladesh', 'China', 'China', 'India', 'India', 'Japan', 'Japan', 
                'South Korea', 'Denmark-Sweden', 'Malaysia'],
    'length_km': [6.15, 55, 164.8, 5.6, 4.94, 3.91, 13.1, 21.38, 7.85, 13.5],
    'cost_usd_million': [3600, 20000, 8500, 340, 1000, 4300, 7000, 1900, 4000, 180],
    'year': [2022, 2018, 2011, 2009, 2018, 1998, 1988, 2009, 2000, 1985],
    'type': ['Road-Rail', 'Road', 'Rail', 'Road', 'Road-Rail', 'Road', 'Road-Rail', 
             'Road', 'Road-Rail', 'Road'],
    'lanes': [4, 6, 2, 8, 3, 6, 4, 6, 4, 4],
    'funding': ['China (loan)', 'China (domestic)', 'China (domestic)', 'India (domestic)',
                'India (domestic)', 'Japan (domestic)', 'Japan (domestic)', 
                'South Korea (domestic)', 'EU (joint)', 'Japan (loan)']
}

# METRO SYSTEMS DATABASE
metro_data = {
    'name': ['Dhaka Metro Rail (MRT Line 6)', 'Delhi Metro Phase 1', 'Mumbai Metro Line 1',
             'Beijing Subway Line 16', 'Shanghai Metro Line 11', 'Tokyo Metro Fukutoshin Line',
             'Seoul Metro Line 9', 'Singapore MRT Circle Line', 'Dubai Metro Red Line'],
    'country': ['Bangladesh', 'India', 'India', 'China', 'China', 'Japan', 
                'South Korea', 'Singapore', 'UAE'],
    'length_km': [20.1, 65, 11.4, 49.8, 82.4, 20.2, 40.6, 35.5, 52.1],
    'cost_usd_million': [2800, 2300, 650, 4500, 3200, 5500, 2900, 6000, 7600],
    'year': [2022, 2006, 2014, 2016, 2013, 2008, 2009, 2011, 2009],
    'stations': [16, 59, 12, 29, 38, 16, 38, 30, 29],
    'funding': ['Japan (loan)', 'Japan (loan)', 'India (domestic)', 'China (domestic)',
                'China (domestic)', 'Japan (domestic)', 'South Korea (domestic)',
                'Singapore (domestic)', 'UAE (domestic)']
}

# POWER PLANTS DATABASE
power_data = {
    'name': ['Rooppur Nuclear Power Plant', 'Payra Thermal Power Plant', 'Rampal Power Station',
             'Matarbari Coal Power Plant', 'Kudankulam Nuclear Power Plant', 
             'Mundra Ultra Mega Power Plant', 'Yangjiang Nuclear Power Station',
             'Kashiwazaki-Kariwa Nuclear', 'Shin Kori Nuclear Power Plant',
             'Vogtle Nuclear Plant (Units 3&4)', 'Hinkley Point C'],
    'country': ['Bangladesh', 'Bangladesh', 'Bangladesh', 'Bangladesh', 'India', 'India',
                'China', 'Japan', 'South Korea', 'USA', 'UK'],
    'capacity_mw': [2400, 1320, 1320, 1200, 2000, 4620, 6000, 8212, 5600, 2234, 3200],
    'cost_usd_million': [12650, 1500, 1800, 4500, 3500, 4000, 11000, 20000, 10000, 30000, 33000],
    'year': [2024, 2020, 2022, 2024, 2013, 2012, 2019, 1997, 2016, 2023, 2027],
    'type': ['Nuclear', 'Coal', 'Coal', 'Coal', 'Nuclear', 'Coal', 'Nuclear', 
             'Nuclear', 'Nuclear', 'Nuclear', 'Nuclear'],
    'funding': ['Russia (loan)', 'China (loan)', 'India (loan)', 'Japan (loan)',
                'Russia (loan)', 'India (private)', 'China (domestic)', 'Japan (domestic)',
                'South Korea (domestic)', 'USA (private)', 'China-France (loan)']
}

# Create DataFrames
bridges_df = pd.DataFrame(bridges_data)
metro_df = pd.DataFrame(metro_data)
power_df = pd.DataFrame(power_data)

# Calculate normalized costs
bridges_df['cost_per_km'] = bridges_df['cost_usd_million'] / bridges_df['length_km']
bridges_df['cost_per_lane_km'] = bridges_df['cost_usd_million'] / (bridges_df['length_km'] * bridges_df['lanes'])

metro_df['cost_per_km'] = metro_df['cost_usd_million'] / metro_df['length_km']
metro_df['cost_per_station'] = metro_df['cost_usd_million'] / metro_df['stations']

power_df['cost_per_mw'] = power_df['cost_usd_million'] / power_df['capacity_mw']

print("\n" + "="*80)
print("INFRASTRUCTURE COST COMPARISON ANALYSIS")
print("Bangladesh vs Global Benchmarks")
print("="*80)

# BRIDGE ANALYSIS
print("\n" + "="*80)
print("1. BRIDGE CONSTRUCTION COST ANALYSIS")
print("="*80)

padma = bridges_df[bridges_df['name'] == 'Padma Bridge'].iloc[0]
bridge_global_avg = bridges_df['cost_per_km'].mean()
bridge_global_median = bridges_df['cost_per_km'].median()

print(f"\nPadma Bridge (Bangladesh):")
print(f"  - Length: {padma['length_km']:.2f} km")
print(f"  - Total Cost: ${padma['cost_usd_million']:,.0f} million")
print(f"  - Cost per km: ${padma['cost_per_km']:,.2f} million")
print(f"  - Funding: {padma['funding']}")

print(f"\nGlobal Comparison:")
print(f"  - Global Average: ${bridge_global_avg:,.2f} million per km")
print(f"  - Global Median: ${bridge_global_median:,.2f} million per km")
print(f"  - Padma vs Global Avg: {padma['cost_per_km']/bridge_global_avg:.2f}x")
print(f"  - Padma vs Global Median: {padma['cost_per_km']/bridge_global_median:.2f}x")

print(f"\nSimilar Road-Rail Bridges:")
similar_bridges = bridges_df[bridges_df['type'] == 'Road-Rail'].sort_values('cost_per_km')
for _, bridge in similar_bridges.iterrows():
    vs_padma = bridge['cost_per_km'] / padma['cost_per_km']
    print(f"  - {bridge['name']} ({bridge['country']}): ${bridge['cost_per_km']:,.2f}M/km ({vs_padma:.2f}x)")

# METRO ANALYSIS
print("\n" + "="*80)
print("2. METRO RAIL CONSTRUCTION COST ANALYSIS")
print("="*80)

dhaka_metro = metro_df[metro_df['name'] == 'Dhaka Metro Rail (MRT Line 6)'].iloc[0]
metro_global_avg = metro_df['cost_per_km'].mean()
metro_global_median = metro_df['cost_per_km'].median()

print(f"\nDhaka Metro Rail (Bangladesh):")
print(f"  - Length: {dhaka_metro['length_km']:.2f} km")
print(f"  - Stations: {dhaka_metro['stations']}")
print(f"  - Total Cost: ${dhaka_metro['cost_usd_million']:,.0f} million")
print(f"  - Cost per km: ${dhaka_metro['cost_per_km']:,.2f} million")
print(f"  - Funding: {dhaka_metro['funding']}")

print(f"\nGlobal Comparison:")
print(f"  - Global Average: ${metro_global_avg:,.2f} million per km")
print(f"  - Global Median: ${metro_global_median:,.2f} million per km")
print(f"  - Dhaka vs Global Avg: {dhaka_metro['cost_per_km']/metro_global_avg:.2f}x")
print(f"  - Dhaka vs Global Median: {dhaka_metro['cost_per_km']/metro_global_median:.2f}x")

print(f"\nJapan-funded Metro Systems:")
japan_metros = metro_df[metro_df['funding'].str.contains('Japan', na=False)].sort_values('cost_per_km')
for _, metro in japan_metros.iterrows():
    vs_dhaka = metro['cost_per_km'] / dhaka_metro['cost_per_km']
    print(f"  - {metro['name']} ({metro['country']}): ${metro['cost_per_km']:,.2f}M/km ({vs_dhaka:.2f}x)")

# POWER PLANT ANALYSIS
print("\n" + "="*80)
print("3. POWER PLANT CONSTRUCTION COST ANALYSIS")
print("="*80)

bd_plants = power_df[power_df['country'] == 'Bangladesh']
print(f"\nBangladesh Power Plants:")
for _, plant in bd_plants.iterrows():
    type_avg = power_df[power_df['type']==plant['type']]['cost_per_mw'].mean()
    print(f"\n{plant['name']}:")
    print(f"  - Capacity: {plant['capacity_mw']:,.0f} MW")
    print(f"  - Total Cost: ${plant['cost_usd_million']:,.0f} million")
    print(f"  - Cost per MW: ${plant['cost_per_mw']:.2f} million")
    print(f"  - Type: {plant['type']}")
    print(f"  - Funding: {plant['funding']}")
    print(f"  - vs Global {plant['type']} Avg: {plant['cost_per_mw']/type_avg:.2f}x")

# Nuclear comparison
print(f"\nNuclear Power Plants Comparison:")
nuclear_plants = power_df[power_df['type'] == 'Nuclear'].sort_values('cost_per_mw')
nuclear_avg = nuclear_plants['cost_per_mw'].mean()
for _, plant in nuclear_plants.iterrows():
    print(f"  - {plant['name']} ({plant['country']}): ${plant['cost_per_mw']:.2f}M/MW")

rooppur = bd_plants[bd_plants['name']=='Rooppur Nuclear Power Plant'].iloc[0]
print(f"\nRooppur Analysis:")
print(f"  - Rooppur: ${rooppur['cost_per_mw']:.2f}M/MW")
print(f"  - Global Nuclear Avg: ${nuclear_avg:.2f}M/MW")
print(f"  - Rooppur vs Global: {rooppur['cost_per_mw']/nuclear_avg:.2f}x")

# VISUALIZATIONS
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

# Plot 1: Bridge Cost Comparison
ax1 = fig.add_subplot(gs[0, :2])
bridges_sorted = bridges_df.sort_values('cost_per_km', ascending=False)
colors = ['#C73E1D' if 'Bangladesh' in c else '#6A994E' for c in bridges_sorted['country']]
ax1.barh(bridges_sorted['name'], bridges_sorted['cost_per_km'], color=colors, alpha=0.8)
ax1.set_xlabel('Cost per km (Million USD)', fontsize=12, fontweight='bold')
ax1.set_title('Bridge Construction Costs Comparison', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='x')

# Plot 2: Metro Cost Comparison
ax2 = fig.add_subplot(gs[0, 2])
metro_sorted = metro_df.sort_values('cost_per_km', ascending=False)
colors_metro = ['#C73E1D' if 'Bangladesh' in c else '#6A994E' for c in metro_sorted['country']]
ax2.barh(metro_sorted['name'].str[:20], metro_sorted['cost_per_km'], color=colors_metro, alpha=0.8)
ax2.set_xlabel('Cost per km (Million USD)')
ax2.set_title('Metro Rail Costs', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')

# Plot 3: Bangladesh vs Global (Bridges)
ax3 = fig.add_subplot(gs[1, 0])
categories = ['Padma\nBridge', 'Global\nAverage', 'Global\nMedian']
values = [padma['cost_per_km'], bridge_global_avg, bridge_global_median]
colors_comp = ['#C73E1D', '#6A994E', '#F18F01']
bars = ax3.bar(categories, values, color=colors_comp, alpha=0.8)
ax3.set_ylabel('Cost per km (Million USD)')
ax3.set_title('Padma Bridge vs Global', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'${height:.0f}M', ha='center', va='bottom', fontweight='bold')

# Plot 4: Bangladesh vs Global (Metro)
ax4 = fig.add_subplot(gs[1, 1])
categories_metro = ['Dhaka\nMetro', 'Global\nAverage', 'Global\nMedian']
values_metro = [dhaka_metro['cost_per_km'], metro_global_avg, metro_global_median]
bars = ax4.bar(categories_metro, values_metro, color=colors_comp, alpha=0.8)
ax4.set_ylabel('Cost per km (Million USD)')
ax4.set_title('Dhaka Metro vs Global', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
            f'${height:.0f}M', ha='center', va='bottom', fontweight='bold')

# Plot 5: Power Plant Cost by Type
ax5 = fig.add_subplot(gs[1, 2])
power_by_type = power_df.groupby('type')['cost_per_mw'].mean().sort_values(ascending=False)
ax5.bar(power_by_type.index, power_by_type.values, color='#2E86AB', alpha=0.8)
ax5.set_ylabel('Avg Cost per MW (Million USD)')
ax5.set_title('Power Plant Costs by Type', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3, axis='y')
ax5.tick_params(axis='x', rotation=45)

# Plot 6: Nuclear Power Plant Costs
ax6 = fig.add_subplot(gs[2, :])
nuclear_sorted = nuclear_plants.sort_values('cost_per_mw')
colors_nuclear = ['#C73E1D' if 'Bangladesh' in c else '#6A994E' for c in nuclear_sorted['country']]
bars = ax6.barh(nuclear_sorted['name'], nuclear_sorted['cost_per_mw'], color=colors_nuclear, alpha=0.8)
ax6.set_xlabel('Cost per MW (Million USD)', fontsize=12, fontweight='bold')
ax6.set_title('Nuclear Power Plant Construction Costs', fontsize=14, fontweight='bold')
ax6.grid(True, alpha=0.3, axis='x')
for bar in bars:
    width = bar.get_width()
    ax6.text(width, bar.get_y() + bar.get_height()/2.,
            f'${width:.2f}M', ha='left', va='center', fontsize=9)

plt.savefig('analysis/infrastructure_costs/figures/infrastructure_cost_comparison.png', 
           dpi=300, bbox_inches='tight')
print("   ✓ Visualization saved")
plt.close()

# Save data to CSV
bridges_df.to_csv('analysis/infrastructure_costs/bridges_cost_data.csv', index=False)
metro_df.to_csv('analysis/infrastructure_costs/metro_cost_data.csv', index=False)
power_df.to_csv('analysis/infrastructure_costs/power_plants_cost_data.csv', index=False)
print("   ✓ Data saved to CSV files")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"  ✓ Visualizations: analysis/infrastructure_costs/figures/")
print(f"  ✓ Data files: analysis/infrastructure_costs/")

# Made with Bob
