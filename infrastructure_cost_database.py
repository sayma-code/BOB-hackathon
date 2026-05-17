
"""
Global Infrastructure Cost Comparison Database
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

# BRIDGES DATABASE
BRIDGES = [
    # Bangladesh
    {'name': 'Padma Bridge', 'country': 'Bangladesh', 'length_km': 6.15, 'cost_usd_million': 3600, 'year': 2022, 'type': 'Road-Rail', 'lanes': 4, 'funding': 'China (loan)'},
    
    # China
    {'name': 'Hong Kong-Zhuhai-Macau Bridge', 'country': 'China', 'length_km': 55, 'cost_usd_million': 20000, 'year': 2018, 'type': 'Road', 'lanes': 6, 'funding': 'China (domestic)'},
    {'name': 'Danyang-Kunshan Grand Bridge', 'country': 'China', 'length_km': 164.8, 'cost_usd_million': 8500, 'year': 2011, 'type': 'Rail', 'lanes': 2, 'funding': 'China (domestic)'},
    {'name': 'Jiaozhou Bay Bridge', 'country': 'China', 'length_km': 42.5, 'cost_usd_million': 2300, 'year': 2011, 'type': 'Road', 'lanes': 6, 'funding': 'China (domestic)'},
    
    # India
    {'name': 'Bandra-Worli Sea Link', 'country': 'India', 'length_km': 5.6, 'cost_usd_million': 340, 'year': 2009, 'type': 'Road', 'lanes': 8, 'funding': 'India (domestic)'},
    {'name': 'Bogibeel Bridge', 'country': 'India', 'length_km': 4.94, 'cost_usd_million': 1000, 'year': 2018, 'type': 'Road-Rail', 'lanes': 3, 'funding': 'India (domestic)'},
    {'name': 'Dhola-Sadiya Bridge', 'country': 'India', 'length_km': 9.15, 'cost_usd_million': 320, 'year': 2017, 'type': 'Road', 'lanes': 2, 'funding': 'India (domestic)'},
    
    # Japan
    {'name': 'Akashi Kaikyo Bridge', 'country': 'Japan', 'length_km': 3.91, 'cost_usd_million': 4300, 'year': 1998, 'type': 'Road', 'lanes': 6, 'funding': 'Japan (domestic)'},
    {'name': 'Great Seto Bridge', 'country': 'Japan', 'length_km': 13.1, 'cost_usd_million': 7000, 'year': 1988, 'type': 'Road-Rail', 'lanes': 4, 'funding': 'Japan (domestic)'},
    
    # South Korea
    {'name': 'Incheon Bridge', 'country': 'South Korea', 'length_km': 21.38, 'cost_usd_million': 1900, 'year': 2009, 'type': 'Road', 'lanes': 6, 'funding': 'South Korea (domestic)'},
    {'name': 'Yi Sun-sin Bridge', 'country': 'South Korea', 'length_km': 2.26, 'cost_usd_million': 650, 'year': 2012, 'type': 'Road', 'lanes': 4, 'funding': 'South Korea (domestic)'},
    
    # USA
    {'name': 'San Francisco-Oakland Bay Bridge (New)', 'country': 'USA', 'length_km': 3.6, 'cost_usd_million': 6500, 'year': 2013, 'type': 'Road', 'lanes': 10, 'funding': 'USA (domestic)'},
    {'name': 'Verrazano-Narrows Bridge', 'country': 'USA', 'length_km': 4.18, 'cost_usd_million': 320, 'year': 1964, 'type': 'Road', 'lanes': 12, 'funding': 'USA (domestic)'},
    
    # Europe
    {'name': 'Øresund Bridge', 'country': 'Denmark-Sweden', 'length_km': 7.85, 'cost_usd_million': 4000, 'year': 2000, 'type': 'Road-Rail', 'lanes': 4, 'funding': 'EU (joint)'},
    {'name': 'Vasco da Gama Bridge', 'country': 'Portugal', 'length_km': 17.2, 'cost_usd_million': 1100, 'year': 1998, 'type': 'Road', 'lanes': 6, 'funding': 'EU (loan)'},
    
    # Other Asian
    {'name': 'Penang Bridge', 'country': 'Malaysia', 'length_km': 13.5, 'cost_usd_million': 180, 'year': 1985, 'type': 'Road', 'lanes': 4, 'funding': 'Japan (loan)'},
    {'name': 'Sultan Abdul Halim Muadzam Shah Bridge', 'country': 'Malaysia', 'length_km': 24, 'cost_usd_million': 1000, 'year': 2014, 'type': 'Road', 'lanes': 4, 'funding': 'China (loan)'},
]

# METRO RAIL SYSTEMS DATABASE
METRO_SYSTEMS = [
    # Bangladesh
    {'name': 'Dhaka Metro Rail (MRT Line 6)', 'country': 'Bangladesh', 'length_km': 20.1, 'cost_usd_million': 2800, 'year': 2022, 'stations': 16, 'funding': 'Japan (loan)', 'daily_capacity': 60000},
    
    # India
    {'name': 'Delhi Metro Phase 1', 'country': 'India', 'length_km': 65, 'cost_usd_million': 2300, 'year': 2006, 'stations': 59, 'funding': 'Japan (loan)', 'daily_capacity': 2800000},
    {'name': 'Mumbai Metro Line 1', 'country': 'India', 'length_km': 11.4, 'cost_usd_million': 650, 'year': 2014, 'stations': 12, 'funding': 'India (domestic)', 'daily_capacity': 350000},
    {'name': 'Bangalore Metro Phase 1', 'country': 'India', 'length_km': 42.3, 'cost_usd_million': 1800, 'year': 2017, 'stations': 40, 'funding': 'Japan (loan)', 'daily_capacity': 400000},
    {'name': 'Kolkata Metro Extension', 'country': 'India', 'length_km': 16.5, 'cost_usd_million': 900, 'year': 2020, 'stations': 12, 'funding': 'India (domestic)', 'daily_capacity': 200000},
    
    # China
    {'name': 'Beijing Subway Line 16', 'country': 'China', 'length_km': 49.8, 'cost_usd_million': 4500, 'year': 2016, 'stations': 29, 'funding': 'China (domestic)', 'daily_capacity': 800000},
    {'name': 'Shanghai Metro Line 11', 'country': 'China', 'length_km': 82.4, 'cost_usd_million': 3200, 'year': 2013, 'stations': 38, 'funding': 'China (domestic)', 'daily_capacity': 1000000},
    {'name': 'Guangzhou Metro Line 3', 'country': 'China', 'length_km': 67.3, 'cost_usd_million': 2800, 'year': 2010, 'stations': 30, 'funding': 'China (domestic)', 'daily_capacity': 900000},
    
    # Japan
    {'name': 'Tokyo Metro Fukutoshin Line', 'country': 'Japan', 'length_km': 20.2, 'cost_usd_million': 5500, 'year': 2008, 'stations': 16, 'funding': 'Japan (domestic)', 'daily_capacity': 500000},
    {'name': 'Osaka Metro Imazatosuji Line', 'country': 'Japan', 'length_km': 11.9, 'cost_usd_million': 3200, 'year': 2006, 'stations': 11, 'funding': 'Japan (domestic)', 'daily_capacity': 200000},
    
    # South Korea
    {'name': 'Seoul Metro Line 9', 'country': 'South Korea', 'length_km': 40.6, 'cost_usd_million': 2900, 'year': 2009, 'stations': 38, 'funding': 'South Korea (domestic)', 'daily_capacity': 800000},
    {'name': 'Busan Metro Line 3', 'country': 'South Korea', 'length_km': 18.3, 'cost_usd_million': 1600, 'year': 2005, 'stations': 17, 'funding': 'South Korea (domestic)', 'daily_capacity': 300000},
    
    # Europe
    {'name': 'Copenhagen Metro City Ring', 'country': 'Denmark', 'length_km': 15.5, 'cost_usd_million': 3800, 'year': 2019, 'stations': 17, 'funding': 'Denmark (domestic)', 'daily_capacity': 300000},
    {'name': 'Paris Metro Line 14 Extension', 'country': 'France', 'length_km': 14, 'cost_usd_million': 2500, 'year': 2020, 'stations': 9, 'funding': 'France (domestic)', 'daily_capacity': 400000},
    {'name': 'London Crossrail (Elizabeth Line)', 'country': 'UK', 'length_km': 118, 'cost_usd_million': 23000, 'year': 2022, 'stations': 41, 'funding': 'UK (domestic)', 'daily_capacity': 1500000},
    
    # Other Asian
    {'name': 'Singapore MRT Circle Line', 'country': 'Singapore', 'length_km': 35.5, 'cost_usd_million': 6000, 'year': 2011, 'stations': 30, 'funding': 'Singapore (domestic)', 'daily_capacity': 500000},
    {'name': 'Dubai Metro Red Line', 'country': 'UAE', 'length_km': 52.1, 'cost_usd_million': 7600, 'year': 2009, 'stations': 29, 'funding': 'UAE (domestic)', 'daily_capacity': 600000},
]

# POWER PLANTS DATABASE
POWER_PLANTS = [
    # Bangladesh
    {'name': 'Rooppur Nuclear Power Plant', 'country': 'Bangladesh', 'capacity_mw': 2400, 'cost_usd_million': 12650, 'year': 2024, 'type': 'Nuclear', 'funding': 'Russia (loan)'},
    {'name': 'Payra Thermal Power Plant', 'country': 'Bangladesh', 'capacity_mw': 1320, 'cost_usd_million': 1500, 'year': 2020, 'type': 'Coal', 'funding': 'China (loan)'},
    {'name': 'Rampal Power Station', 'country': 'Bangladesh', 'capacity_mw': 1320, 'cost_usd_million': 1800, 'year': 2022, 'type': 'Coal', 'funding': 'India (loan)'},
    {'name': 'Matarbari Coal Power Plant', 'country': 'Bangladesh', 'capacity_mw': 1200, 'cost_usd_million': 4500, 'year': 2024, 'type': 'Coal', 'funding': 'Japan (loan)'},
    
    # India
    {'name': 'Kudankulam Nuclear Power Plant', 'country': 'India', 'capacity_mw': 2000, 'cost_usd_million': 3500, 'year': 2013, 'type': 'Nuclear', 'funding': 'Russia (loan)'},
    {'name': 'Mundra Ultra Mega Power Plant', 'country': 'India', 'capacity_mw': 4620, 'cost_usd_million': 4000, 'year': 2012, 'type': 'Coal', 'funding': 'India (private)'},
    {'name': 'Bhadla Solar Park', 'country': 'India', 'capacity_mw': 2245, 'cost_usd_million': 1400, 'year': 2020, 'type': 'Solar', 'funding': 'India (private)'},
    
    # China
    {'name': 'Three Gorges Dam', 'country': 'China', 'capacity_mw': 22500, 'cost_usd_million': 37000, 'year': 2012, 'type': 'Hydro', 'funding': 'China (domestic)'},
    {'name': 'Yangjiang Nuclear Power Station', 'country': 'China', 'capacity_mw': 6000, 'cost_usd_million': 11000, 'year': 2019, 'type': 'Nuclear', 'funding': 'China (domestic)'},
    {'name': 'Huaneng Yuhuan Power Station', 'country': 'China', 'capacity_mw': 4000, 'cost_usd_million': 2800, 'year': 2006, 'type': 'Coal', 'funding': 'China (domestic)'},
    
    # Japan
    {'name': 'Kashiwazaki-Kariwa Nuclear', 'country': 'Japan', 'capacity_mw': 8212, 'cost_usd_million': 20000, 'year': 1997, 'type': 'Nuclear', 'funding': 'Japan (domestic)'},
    {'name': 'Futtsu Thermal Power Station', 'country': 'Japan', 'capacity_mw': 5040, 'cost_usd_million': 4500, 'year': 2010, 'type': 'Gas', 'funding': 'Japan (domestic)'},
    
    # South Korea
    {'name': 'Shin Kori Nuclear Power Plant', 'country': 'South Korea', 'capacity_mw': 5600, 'cost_usd_million': 10000, 'year': 2016, 'type': 'Nuclear', 'funding': 'South Korea (domestic)'},
    {'name': 'Dangjin Thermal Power Plant', 'country': 'South Korea', 'capacity_mw': 6040, 'cost_usd_million': 5000, 'year': 2012, 'type': 'Coal', 'funding': 'South Korea (domestic)'},
    
    # USA
    {'name': 'Vogtle Nuclear Plant (Units 3&4)', 'country': 'USA', 'capacity_mw': 2234, 'cost_usd_million': 30000, 'year': 2023, 'type': 'Nuclear', 'funding': 'USA (private)'},
    {'name': 'Ivanpah Solar Power Facility', 'country': 'USA', 'capacity_mw': 392, 'cost_usd_million': 2200, 'year': 2014, 'type': 'Solar', 'funding': 'USA (private)'},
    
    # Europe
    {'name': 'Hinkley Point C', 'country': 'UK', 'capacity_mw': 3200, 'cost_usd_million': 33000, 'year': 2027, 'type': 'Nuclear', 'funding': 'China-France (loan)'},
    {'name': 'Olkiluoto 3 Nuclear', 'country': 'Finland', 'capacity_mw': 1600, 'cost_usd_million': 11000, 'year': 2023, 'type': 'Nuclear', 'funding': 'Finland (domestic)'},
]

class InfrastructureCostAnalyzer:
    def __init__(self):
        """Initialize with infrastructure databases"""
        self.bridges_df = pd.DataFrame(BRIDGES)
        self.metro_df = pd.DataFrame(METRO_SYSTEMS)
        self.power_df = pd.DataFrame(POWER_PLANTS)
        
        # Calculate normalized costs
        self.bridges_df['cost_per_km'] = self.bridges_df['cost_usd_million'] / self.bridges_df['length_km']
        self.bridges_df['cost_per_lane_km'] = self.bridges_df['cost_usd_million'] / (self.bridges_df['length_km'] * self.bridges_df['lanes'])
        
        self.metro_df['cost_per_km'] = self.metro_df['cost_usd_million'] / self.metro_df['length_km']
        self.metro_df['cost_per_station'] = self.metro_df['cost_usd_million'] / self.metro_df['stations']
        
        self.power_df['cost_per_mw'] = self.power_df['cost_usd_million'] / self.power_df['capacity_mw']
        
        # Create output directories
        os.makedirs('analysis/infrastructure_costs', exist_ok=True)
        os.makedirs('analysis/infrastructure_costs/figures', exist_ok=True)
    
    def analyze_bridges(self):
        """Analyze bridge construction costs"""
        print("\n" + "="*80)
        print("BRIDGE CONSTRUCTION COST ANALYSIS")
        print("="*80)
        
        # Get Padma Bridge data
        padma = self.bridges_df[self.bridges_df['name'] == 'Padma Bridge'].iloc[0]
        
        print(f"\nPadma Bridge (Bangladesh):")
        print(f"  - Length: {padma['length_km']:.2f} km")
        print(f"  - Total Cost: ${padma['cost_usd_million']:.0f} million")
        print(f"  - Cost per km: ${padma['cost_per_km']:.2f} million")
        print(f"  - Cost per lane-km: ${padma['cost_per_lane_km']:.2f} million")
        print(f"  - Funding: {padma['funding']}")
        
        # Compare with global averages
        print(f"\n{'='*100}")
        print(f"GLOBAL COMPARISON")
        print(f"{'='*100}")
        
        # Group by country
        country_avg = self.bridges_df.groupby('country').agg({
            'cost_per_km': 'mean',
            'cost_per_lane_km': 'mean',
            'length_km': 'mean'
        }).round(2)
        
        print(f"\n{'Country':<25} | {'Avg Cost/km':<15} | {'Avg Cost/lane-km':<18} | {'vs Padma'}")
        print(f"{'-'*100}")
        
        for country, row in country_avg.sort_values('cost_per_km', ascending=False).iterrows():
            vs_padma = row['cost_per_km'] / padma['cost_per_km']
            print(f"{country:<25} | ${row['cost_per_km']:>13,.2f}M | ${row['cost_per_lane_km']:>16,.2f}M | {vs_padma:>7.2f}x")
        
        # Calculate statistics
        global_avg = self.bridges_df['cost_per_km'].mean()
        global_median = self.bridges_df['cost_per_km'].median()
        
        print(f"\n{'='*100}")
        print(f"STATISTICAL ANALYSIS")
        print(f"{'='*100}")
        print(f"  - Global Average: ${global_avg:.2f} million per km")
        print(f"  - Global Median: ${global_median:.2f} million per km")
        print(f"  - Padma Bridge: ${padma['cost_per_km']:.2f} million per km")
        print(f"  - Padma vs Global Avg: {padma['cost_per_km']/global_avg:.2f}x")
        print(f"  - Padma vs Global Median: {padma['cost_per_km']/global_median:.2f}x")
        
        # Identify similar bridges
        similar_bridges = self.bridges_df[
            (self.bridges_df['length_km'] >= 4) & 
            (self.bridges_df['length_km'] <= 10) &
            (self.bridges_df['type'] == 'Road-Rail')
        ].sort_values('cost_per_km')
        
        print(f"\nSimilar Bridges (4-10 km, Road-Rail):")
        print(f"{'='*100}")
        for _, bridge in similar_bridges.iterrows():
            vs_padma = bridge['cost_per_km'] / padma['cost_per_km']
            print(f"  - {bridge['name']} ({bridge['country']}): ${bridge['cost_per_km']:.2f}M/km ({vs_padma:.2f}x Padma)")
        
        return padma
    
    def analyze_metro_systems(self):
        """Analyze metro rail construction costs"""
        print("\n" + "="*80)
        print("METRO RAIL CONSTRUCTION COST ANALYSIS")
        print("="*80)
        
        # Get Dhaka Metro data
        dhaka_metro = self.metro_df[self.metro_df['name'] == 'Dhaka Metro Rail (MRT Line 6)'].iloc[0]
        
        print(f"\nDhaka Metro Rail (Bangladesh):")
        print(f"  - Length: {dhaka_metro['length_km']:.2f} km")
        print(f"  - Stations: {dhaka_metro['stations']}")
        print(f"  - Total Cost: ${dhaka_metro['cost_usd_million']:.0f} million")
        print(f"  - Cost per km: ${dhaka_metro['cost_per_km']:.2f} million")
        print(f"  - Cost per station: ${dhaka_metro['cost_per_station']:.2f} million")
        print(f"  - Funding: {dhaka_metro['funding']}")
        
        # Compare with global averages
        print(f"\n{'='*110}")
        print(f"GLOBAL COMPARISON")
        print(f"{'='*110}")
        
        # Group by country
        country_avg = self.metro_df.groupby('country').agg({
            'cost_per_km': 'mean',
            'cost_per_station': 'mean',
            'length_km': 'mean'
        }).round(2)
        
        print(f"\n{'Country':<25} | {'Avg Cost/km':<15} | {'Avg Cost/station':<18} | {'vs Dhaka'}")
        print(f"{'-'*110}")
        
        for country, row in country_avg.sort_values('cost_per_km', ascending=False).iterrows():
            vs_dhaka = row['cost_per_km'] / dhaka_metro['cost_per_km']
            print(f"{country:<25} | ${row['cost_per_km']:>13,.2f}M | ${row['cost_per_station']:>16,.2f}M | {vs_dhaka:>7.2f}x")
        
        # Calculate statistics
        global_avg = self.metro_df['cost_per_km'].mean()
        global_median = self.metro_df['cost_per_km'].median()
        
        print(f"\n{'='*110}")
        print(f"STATISTICAL ANALYSIS")
        print(f"{'='*110}")
        print(f"  - Global Average: ${global_avg:.2f} million per km")
        print(f"  - Global Median: ${global_median:.2f} million per km")
        print(f"  - Dhaka Metro: ${dhaka_metro['cost_per_km']:.2f} million per km")
        print(f"  - Dhaka vs Global Avg: {dhaka_metro['cost_per_km']/global_avg:.2f}x")
        print(f"  - Dhaka vs Global Median: {dhaka_metro['cost_per_km']/global_median:.2f}x")
        
        return dhaka_metro
    
    def analyze_power_plants(self):
        """Analyze power plant construction costs"""
        print("\n" + "="*80)
        print("POWER PLANT CONSTRUCTION COST ANALYSIS")
        print("="*80)
        
        # Get Bangladesh power plants
        bd_plants = self.power_df[self.power_df['country'] == 'Bangladesh']
        
        print(f"\nBangladesh Power Plants:")
        for _, plant in bd_plants.iterrows():
            print(f"\n{plant['name']}:")
            print(f"  - Capacity: {plant['capacity_mw']:.0f} MW")
            print(f"  - Total Cost: ${plant['cost_usd_million']:.0f} million")
            print(f"  - Cost per MW: ${plant['cost_per_mw']:.2f} million")
            print(f"  - Type: {plant['type']}")
            print(f"  - Funding: {plant['funding']}")
        
        # Compare by type
        print(f"\n{'='*120}")
        print(f"GLOBAL COMPARISON BY PLANT TYPE")
        print(f"{'='*120}")
        
        for plant_type in ['Nuclear', 'Coal', 'Solar']:
            type_plants = self.power_df[self.power_df['type'] == plant_type]
            if len(type_plants) > 0:
                print(f"\n{plant_type} Power Plants:")
                print(f"{'Country':<25} | {'Plant Name':<40} | {'Cost/MW':<15} | {'Capacity'}")
                print(f"{'-'*120}")
                
                for _, plant in type_plants.sort_values('cost_per_mw').iterrows():
                    print(f"{plant['country']:<25} | {plant['name']:<40} | ${plant['cost_per_mw']:>13,.2f}M | {plant['capacity_mw']:>8,.0f} MW")
        
        # Calculate statistics by type
        print(f"\n{'='*120}")
        print(f"STATISTICAL ANALYSIS BY TYPE")
        print(f"{'='*120}")
        
        type_stats = self.power_df.groupby('type').agg({
            'cost_per_mw': ['mean', 'median', 'min', 'max'],
            'capacity_mw': 'mean'
        }).round(2)
        
        print(type_stats)
        
        return bd_plants
    
    def create_visualizations(self, padma, dhaka_metro, bd_plants):
        """Create comprehensive cost comparison visualizations"""
        print("\n" + "="*80)
        print("GENERATING VISUALIZATIONS")
        print("="*80)
        
        fig = plt.figure(figsize=(20, 14))
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
        
        # Plot 1: Bridge Cost Comparison
        ax1 = fig.add_subplot(gs[0, :2])
        bridges_sorted = self.bridges_df.sort_values('cost_per_km', ascending=False).head(15)
        colors = ['#C73E1D' if 'Bangladesh' in c else '#6A994E' for c in bridges_sorted['country']]
        
        bars = ax1.barh(bridges_sorted['name'], bridges_sorted['cost_per_km'], color=colors, alpha=0.8)
        ax1.set_xlabel('Cost per km (Million USD)', fontsize=12, fontweight='bold')
        ax1.set_title('Bridge Construction Costs: Top 15 Most Expensive', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Plot 2: Metro Cost Comparison
        ax2 = fig.add_subplot(gs[0, 2])
        metro_sorted = self.metro_df.sort_values('cost_per_km', ascending=False).head(10)
        colors_metro = ['#C73E1D' if 'Bangladesh' in c else '#6A994E' for c in metro_sorted['country']]
        
        bars = ax2.barh(metro_sorted['name'].str[:20], metro_sorted['cost_per_km'], color=colors_metro, alpha=0.8)
        ax2.set_xlabel('Cost per km (Million USD)')
        ax2.set_title('Metro Rail Costs: Top 10', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Plot 3: Power Plant Cost by Type
        ax3 = fig.add_subplot(gs[1, 0])
        power_by_type = self.power_df.groupby('type')['cost_per_mw'].mean().sort_values(ascending=False)
        bars = ax3.bar(power_by_type.index, power_by_type.values, color='#2E86AB', alpha=0.8)
        ax3.set_ylabel('Avg Cost per MW (Million USD)')
        ax3.set_title('Power Plant Costs by Type', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.tick_params(axis='x', rotation=45)
        
        # Plot 4: Bangladesh vs Global Average (Bridges)
        ax4 = fig.add_subplot(gs[1, 1])
        categories = ['Padma\nBridge', 'Global\nAverage', 'Global\nMedian']
        values = [
            padma['cost_per_km'],
            self.bridges_df['cost_per_km'].mean(),
            self.bridges_df['cost_per_km'].median()
        ]
        colors_comp = ['#C73E1D', '#6A994E', '#F18F01']
        bars = ax4.bar(categories, values, color=colors_comp, alpha=0.8)
        ax4.set_ylabel('Cost per km (Million USD)')
        ax4.set_title('Padma Bridge vs Global', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.0f}M', ha='center', va='bottom', fontweight='bold')
        
        # Plot 5: Bangladesh vs Global Average (Metro)
        ax5 = fig.add_subplot(gs[1, 2])
        categories_metro = ['Dhaka\nMetro', 'Global\nAverage', 'Global\nMedian']
        values_metro = [
            dhaka_metro['cost_per_km'],
            self.metro_df['cost_per_km'].mean(),
            self.metro_df['cost_per_km'].median()
        ]
        bars = ax5.bar(categories_metro, values_metro, color=colors_comp, alpha=0.8)
        ax5.set_ylabel('Cost per km (Million USD)')
        ax5.set_title('Dhaka Metro vs Global', fontsize=12, fontweight='bold')
        ax5.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.0f}M', ha='center', va='bottom', fontweight='bold')
        
        # Plot 6: Nuclear Power Plant Costs
        ax6 = fig.add_subplot(gs[2, :])
        nuclear_plants = self.power_df[self.power_df['type'] == 'Nuclear'].sort_values('cost_per_mw')
        colors_nuclear = ['#C73E1D' if 'Bangladesh' in c else '#6A994E' for c in nuclear_plants['country']]
        
        bars = ax6.barh(nuclear_plants['name'], nuclear_plants['cost_per_mw'], color=colors_nuclear, alpha=0.8)
        ax6.set_xlabel('Cost per MW (Million USD)', fontsize=12, fontweight='bold')
        ax6.set_title('Nuclear Power Plant Construction Costs', fontsize=14, fontweight='bold')
        ax6.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax6.text(width, bar.get_y() + bar.get_height()/2.,
                    f'${width:.2f}M', ha='left', va='center', fontsize=9)
        
        plt.savefig('analysis/infrastructure_costs/figures/infrastructure_cost_comparison.png', 
                   dpi=300, bbox_inches='tight')
        print("   ✓ Comprehensive visualization saved")
        plt.close()
    
    def generate_report(self, padma, dhaka_metro, bd_plants):
        """Generate comprehensive infrastructure cost comparison report"""
        print("\n" + "="*80)
        print("GENERATING INFRASTRUCTURE COST REPORT")
        print("="*80)
        
        # Calculate key statistics
        bridge_global_avg = self.bridges_df['cost_per_km'].mean()
        metro_global_avg = self.metro_df['cost_per_km'].mean()
        
        report = f"""# Infrastructure Cost Comparison Analysis
## Bangladesh vs Global Benchmarks

**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}  
**Projects Analyzed:** {len(self.bridges_df)} Bridges, {len(self.metro_df)} Metro Systems, {len(self.power_df)} Power Plants

---

## Executive Summary

This analysis compares the construction costs of Bangladesh's major infrastructure projects with similar projects globally. The findings reveal significant cost variations and potential inefficiencies.

### Key Findings

1. **Padma Bridge:** {padma['cost_per_km']/bridge_global_avg:.2f}x global average cost per km
2. **Dhaka Metro:** {dhaka_metro['cost_per_km']/metro_global_avg:.2f}x global average cost per km
3. **Power Plants:** Significant cost variations depending on technology and funding source

---

## 1. Padma Bridge Analysis

### Project Details

- **Length:** {padma['length_km']:.2f} km
- **Type:** {padma['type']}
- **Lanes:** {padma['lanes']}
- **Total Cost:** ${padma['cost_usd_million']:,.0f} million
- **Cost per km:** ${padma['cost_per_km']:,.2f} million
- **Cost per lane-km:** ${padma['cost_per_lane_km']:,.2f} million
- **Funding Source:** {padma['funding']}
- **Completion Year:** {padma['year']}

### Global Comparison

| Metric | Padma Bridge | Global Average | Global Median | Padma vs Avg |
|--------|-------------|----------------|---------------|--------------|
| Cost per km | ${padma['cost_per_km']:,.2f}M | ${bridge_global_avg:,.2f}M | ${self.bridges_df['cost_per_km'].median():,.2f}M | {padma['cost_per_km']/bridge_global_avg:.2f}x |
| Cost per lane-km | ${padma['cost_per_lane_km']:,.2f}M | ${self.bridges_df['cost_per_lane_km'].mean():,.2f}M | ${self.bridges_df['cost_per_lane_km'].median():,.2f}M | {padma['cost_per_lane_km']/self.bridges_df['cost_per_lane_km'].mean():.2f}x |

### Similar Bridges Comparison

"""
        
        # Add similar bridges
        similar_bridges = self.bridges_df[
            (self.bridges_df['length_km'] >= 4) & 
            (self.bridges_df['length_km'] <= 10) &
            (self.bridges_df['type'] == 'Road-Rail')
        ].sort_values('cost_per_km')
        
        report += "| Bridge | Country | Length (km) | Cost/km | vs Padma |\n"
        report += "|--------|---------|-------------|---------|----------|\n"
        
        for _, bridge in similar_bridges.iterrows():
            vs_padma = bridge['cost_per_km'] / padma['cost_per_km']
            report += f"| {bridge['name']} | {bridge['country']} | {bridge['length_km']:.2f} | ${bridge['cost_per_km']:,.2f}M | {vs_padma:.2f}x |\n"
        
        report += f"""

### Cost Analysis

**Why is Padma Bridge expensive?**

1. **Geological Challenges:**
   - Built on Padma River with strong currents
   - Deep foundation required (up to 122m)
   - Seismic zone considerations

2. **Technical Specifications:**
   - Dual-purpose (road + rail)
   - 6.15 km length over water
   - High-capacity design

3. **Funding Structure:**
   - 100% loan from China
   - Interest costs included
   - Currency exchange risks

4. **Comparison with Similar Projects:**
   - Øresund Bridge (Denmark-Sweden): ${self.bridges_df[self.bridges_df['name']=='Øresund Bridge']['cost_per_km'].values[0]:.2f}M/km
   - Great Seto Bridge (Japan): ${self.bridges_df[self.bridges_df['name']=='Great Seto Bridge']['cost_per_km'].values[0]:.2f}M/km
   - Padma Bridge: ${padma['cost_per_km']:.2f}M/km

**Verdict:** Padma Bridge is {padma['cost_per_km']/bridge_global_avg:.1f}x more expensive than global average, but within range for complex water crossings.

---

## 2. Dhaka Metro Rail Analysis

### Project Details

- **Length:** {dhaka_metro['length_km']:.2f} km
- **Stations:** {dhaka_metro['stations']}
- **Total Cost:** ${dhaka_metro['cost_usd_million']:,.0f} million
- **Cost per km:** ${dhaka_metro['cost_per_km']:,.2f} million
- **Cost per station:** ${dhaka_metro['cost_per_station']:,.2f} million
- **Funding Source:** {dhaka_metro['funding']}
- **Completion Year:** {dhaka_metro['year']}

### Global Comparison

| Metric | Dhaka Metro | Global Average | Global Median | Dhaka vs Avg |
|--------|------------|----------------|---------------|--------------|
| Cost per km | ${dhaka_metro['cost_per_km']:,.2f}M | ${metro_global_avg:,.2f}M | ${self.metro_df['cost_per_km'].median():,.2f}M | {dhaka_metro['cost_per_km']/metro_global_avg:.2f}x |
| Cost per station | ${dhaka_metro['cost_per_station']:,.2f}M | ${self.metro_df['cost_per_station'].mean():,.2f}M | ${self.metro_df['cost_per_station'].median():,.2f}M | {dhaka_metro['cost_per_station']/self.metro_df['cost_per_station'].mean():.2f}x |

### Regional Comparison

"""
        
        # Add regional metro comparison
        asian_metros = self.metro_df[self.metro_df['country'].isin(['India', 'China', 'Japan', 'South Korea', 'Singapore', 'Bangladesh'])]
        
        report += "| Metro System | Country | Cost/km | vs Dhaka |\n"
        report += "|--------------|---------|---------|----------|\n"
        
        for _, metro in asian_metros.sort_values('cost_per_km').iterrows():
            vs_dhaka = metro['cost_per_km'] / dhaka_metro['cost_per_km']
            report += f"| {metro['name']} | {metro['country']} | ${metro['cost_per_km']:,.2f}M | {vs_dhaka:.2f}x |\n"
        
        report += f"""

### Cost Analysis

**Why is Dhaka Metro expensive?**

1. **Elevated Structure:**
   - Mostly elevated (not underground)
   - Should be cheaper than underground systems
   - But costs are comparable to underground metros

2. **Comparison with Similar Systems:**
   - Delhi Metro Phase 1: ${self.metro_df[self.metro_df['name']=='Delhi Metro Phase 1']['cost_per_km'].values[0]:.2f}M/km (similar funding source)
   - Mumbai Metro Line 1: ${self.metro_df[self.metro_df['name']=='Mumbai Metro Line 1']['cost_per_km'].values[0]:.2f}M/km
   - Dhaka Metro: ${dhaka_metro['cost_per_km']:.2f}M/km

3. **Funding Structure:**
   - JICA loan (Japan)
   - Includes technical assistance costs
   - Japanese technology and standards

**Verdict:** Dhaka Metro is {dhaka_metro['cost_per_km']/metro_global_avg:.1f}x more expensive than global average. Significantly more expensive than comparable Indian metros.

---

## 3. Power Plant Analysis

### Bangladesh Power Plants

"""
        
        for _, plant in bd_plants.iterrows():
            type_avg = self.power_df[self.power_df['type']==plant['type']]['cost_per_mw'].mean()
            report += f"""
#### {plant['name']}

- **Capacity:** {plant['capacity_mw']:,.0f} MW
- **Type:** {plant['type']}
- **Total Cost:** ${plant['cost_usd_million']:,.0f} million
- **Cost per MW:** ${plant['cost_per_mw']:.2f} million
- **Funding:** {plant['funding']}
- **vs Global {plant['type']} Average:** {plant['cost_per_mw']/type_avg:.2f}x

"""
        
        report += """

### Global Power Plant Cost Comparison

#### Nuclear Power Plants

"""
        
        nuclear_plants = self.power_df[self.power_df['type']=='Nuclear'].sort_values('cost_per_mw')
        report += "| Plant | Country | Cost/MW | Capacity (MW) |\n"
        report += "|-------|---------|---------|---------------|\n"
        
        for _, plant in nuclear_plants.iterrows():
            report += f"| {plant['name']} | {plant['country']} | ${plant['cost_per_mw']:.2f}M | {plant['capacity_mw']:,.0f} |\n"
        
        report += """

#### Coal Power Plants

"""
        
        coal_plants = self.power_df[self.power_df['type']=='Coal'].sort_values('cost_per_mw')
        report += "| Plant | Country | Cost/MW | Capacity (MW) |\n"
        report += "|-------|---------|---------|---------------|\n"
        
        for _, plant in coal_plants.iterrows():
            report += f"| {plant['name']} | {plant['country']} | ${plant['cost_per_mw']:.2f}M | {plant['capacity_mw']:,.0f} |\n"
        
        # Calculate Rooppur comparison
        rooppur = bd_plants[bd_plants['name']=='Rooppur Nuclear Power Plant'].iloc[0]
        nuclear_avg = self.power_df[self.power_df['type']=='Nuclear']['cost_per_mw'].mean()
        
        report += f"""

### Critical Analysis: Rooppur Nuclear Power Plant

**Project Details:**
- Capacity: {rooppur['capacity_mw']:,.0f} MW
- Cost: ${rooppur['cost_usd_million']:,.0f} million
- Cost per MW: ${rooppur['cost_per_mw']:.2f} million
- Funding: {rooppur['funding']}

**Global Comparison:**
- Global Nuclear Average: ${nuclear_avg:.2f} million per MW
- Rooppur: ${rooppur['cost_per_mw']:.2f} million per MW
- **Rooppur is {rooppur['cost_per_mw']/nuclear_avg:.2f}x more expensive than global average**

**Comparison with Similar Projects:**
- Kudankulam (India, Russian technology): ${self.power_df[self.power_df['name']=='Kudankulam Nuclear Power Plant']['cost_per_mw'].values[0]:.2f}M/MW
- Yangjiang (China): ${self.power_df[self.power_df['name']=='Yangjiang Nuclear Power Station']['cost_per_mw'].values[0]:.2f}M/MW
