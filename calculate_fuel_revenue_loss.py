"""
Calculate Potential Revenue Loss from Foreign-Controlled Fuel Resources
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path

# Natural Gas Revenue Loss (Chevron)
print("="*80)
print("FUEL REVENUE LOSS CALCULATION")
print("="*80)

print("\n1. NATURAL GAS - Chevron Control")
print("-"*80)
chevron_production_bcf = 500  # 50% of Bangladesh production
gas_price = 2.75  # USD per MCF (thousand cubic feet)
production_cost = 0.80  # USD per MCF
# BCF to MCF: 1 BCF = 1,000,000 MCF
chevron_revenue = chevron_production_bcf * 1_000_000 * gas_price
chevron_costs = chevron_production_bcf * 1_000_000 * production_cost
chevron_profit = chevron_revenue - chevron_costs
chevron_share = chevron_profit * 0.55  # PSC share
bangladesh_share = chevron_profit * 0.45
print(f"Annual Production: {chevron_production_bcf} BCF")
print(f"Revenue: ${chevron_revenue:,.0f}")
print(f"Costs: ${chevron_costs:,.0f}")
print(f"Profit: ${chevron_profit:,.0f}")
print(f"Chevron Takes: ${chevron_share:,.0f}")
print(f"Bangladesh Gets: ${bangladesh_share:,.0f}")
print(f"LOSS TO FOREIGN COMPANY: ${chevron_share:,.0f}")

# Coal Opportunity Loss
print("\n2. COAL - Undeveloped Reserves")
print("-"*80)
potential_production_mt = 15  # Million tons/year
coal_price = 150  # USD per ton
production_cost_coal = 45  # USD per ton
export_cost = 15  # USD per ton
coal_revenue = potential_production_mt * 1_000_000 * coal_price
coal_costs = potential_production_mt * 1_000_000 * (production_cost_coal + export_cost)
coal_profit = coal_revenue - coal_costs
import_savings = 8 * 1_000_000 * coal_price  # 8 MT imports
total_coal_loss = coal_profit + import_savings
print(f"Potential Production: {potential_production_mt} million tons/year")
print(f"Revenue: ${coal_revenue:,.0f}")
print(f"Costs: ${coal_costs:,.0f}")
print(f"Profit: ${coal_profit:,.0f}")
print(f"Import Savings: ${import_savings:,.0f}")
print(f"TOTAL OPPORTUNITY LOSS: ${total_coal_loss:,.0f}")

# LNG Import Cost
print("\n3. LNG IMPORTS - Avoidable Cost")
print("-"*80)
lng_import_bcf = 274  # Annual imports
lng_price = 8.50  # USD per MCF
domestic_cost = 0.80  # USD per MCF if produced locally
lng_import_cost = lng_import_bcf * 1_000_000 * lng_price
domestic_production_cost = lng_import_bcf * 1_000_000 * domestic_cost
lng_savings = lng_import_cost - domestic_production_cost
print(f"Annual LNG Imports: {lng_import_bcf} BCF")
print(f"Import Cost: ${lng_import_cost:,.0f}")
print(f"Domestic Cost: ${domestic_production_cost:,.0f}")
print(f"AVOIDABLE COST: ${lng_savings:,.0f}")

# Renewable Opportunity
print("\n4. RENEWABLE ENERGY - Untapped Potential")
print("-"*80)
solar_potential_mw = 5000
wind_potential_mw = 1000
solar_gen_gwh = solar_potential_mw * 8760 * 0.18 / 1000
wind_gen_gwh = wind_potential_mw * 8760 * 0.25 / 1000
fossil_cost_kwh = 0.12
renewable_cost_kwh = 0.05
total_gen_gwh = solar_gen_gwh + wind_gen_gwh
renewable_savings = total_gen_gwh * 1000 * (fossil_cost_kwh - renewable_cost_kwh)
fuel_import_reduction = renewable_savings * 0.7
print(f"Solar Potential: {solar_potential_mw:,.0f} MW")
print(f"Wind Potential: {wind_potential_mw:,.0f} MW")
print(f"Annual Generation: {total_gen_gwh:,.0f} GWh")
print(f"Cost Savings: ${renewable_savings:,.0f}")
print(f"Fuel Import Reduction: ${fuel_import_reduction:,.0f}")

# TOTAL
print("\n" + "="*80)
print("TOTAL ANNUAL REVENUE LOSS")
print("="*80)
total_loss = chevron_share + total_coal_loss + lng_savings + fuel_import_reduction
print(f"\n1. Gas (Foreign Control): ${chevron_share:,.0f}")
print(f"2. Coal (Undeveloped): ${total_coal_loss:,.0f}")
print(f"3. LNG (Avoidable Import): ${lng_savings:,.0f}")
print(f"4. Renewable (Untapped): ${fuel_import_reduction:,.0f}")
print(f"\nTOTAL: ${total_loss:,.0f}")
print(f"TOTAL: ${total_loss/1e9:.2f} BILLION USD PER YEAR")

# Save summary
output_dir = Path('analysis/fuel_resources')
output_dir.mkdir(parents=True, exist_ok=True)

summary = pd.DataFrame([
    {'Category': 'Natural Gas (Foreign Control)', 'Annual_Loss_USD': chevron_share},
    {'Category': 'Coal (Undeveloped)', 'Annual_Loss_USD': total_coal_loss},
    {'Category': 'LNG (Avoidable Import)', 'Annual_Loss_USD': lng_savings},
    {'Category': 'Renewable (Untapped)', 'Annual_Loss_USD': fuel_import_reduction},
    {'Category': 'TOTAL', 'Annual_Loss_USD': total_loss}
])

summary.to_csv(output_dir / 'revenue_loss_summary.csv', index=False)
print(f"\n✓ Summary saved to: {output_dir / 'revenue_loss_summary.csv'}")

# Made with Bob
