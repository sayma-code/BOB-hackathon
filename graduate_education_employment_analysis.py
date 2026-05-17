"""
Graduate Education & Employment Analysis
Analyzes graduate employment, salaries, and opportunities for better earnings
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
from pathlib import Path

def analyze_graduate_education_system():
    """Analyze Bangladesh's graduate education system"""
    
    print("="*80)
    print("GRADUATE EDUCATION & EMPLOYMENT ANALYSIS")
    print("="*80)
    
    # Education statistics (approximate based on available data)
    total_pop = 173.56e6
    youth_15_24 = total_pop * 0.18  # 18% are 15-24
    
    # Higher education enrollment
    tertiary_enrollment_rate = 0.20  # 20% gross enrollment
    total_tertiary_students = youth_15_24 * tertiary_enrollment_rate
    
    # Annual graduates (4-year cycle)
    annual_graduates = total_tertiary_students / 4
    
    # By degree type
    bachelors = annual_graduates * 0.75  # 75% bachelor's
    masters = annual_graduates * 0.20  # 20% master's
    phd = annual_graduates * 0.02  # 2% PhD
    diploma = annual_graduates * 0.03  # 3% diploma
    
    print(f"\nHIGHER EDUCATION SYSTEM:")
    print(f"Youth Population (15-24): {youth_15_24/1e6:.2f}M")
    print(f"Tertiary Enrollment Rate: {tertiary_enrollment_rate*100:.0f}%")
    print(f"Total Tertiary Students: {total_tertiary_students/1e6:.2f}M")
    print(f"\nANNUAL GRADUATES: {annual_graduates/1e6:.2f}M")
    print(f"  Bachelor's: {bachelors/1e6:.2f}M (75%)")
    print(f"  Master's: {masters/1e6:.2f}M (20%)")
    print(f"  PhD: {phd/1e3:.0f}K (2%)")
    print(f"  Diploma: {diploma/1e3:.0f}K (3%)")
    
    return {
        'annual_graduates': annual_graduates,
        'bachelors': bachelors,
        'masters': masters,
        'phd': phd,
        'diploma': diploma
    }

def create_graduate_employment_database():
    """Create database of graduate employment by field"""
    
    fields = [
        # Engineering & Technology
        {
            'Field': 'Computer Science & IT',
            'Annual_Graduates': 50000,
            'Employment_Rate_Percent': 75,
            'Avg_Starting_Salary_BDT': 35000,
            'Avg_Starting_Salary_USD': 320,
            'Avg_5Year_Salary_BDT': 80000,
            'Avg_5Year_Salary_USD': 730,
            'Underemployment_Rate_Percent': 15,
            'Foreign_Employment_Potential': 'Very High',
            'Domestic_Demand': 'Very High',
            'Global_Avg_Salary_USD': 5000,
            'Skill_Gap': 'Medium',
            'Better_Earning_Options': 'Freelancing, foreign jobs, startups, upskilling',
            'Potential_Increase_USD': 2000
        },
        {
            'Field': 'Electrical & Electronics Engineering',
            'Annual_Graduates': 30000,
            'Employment_Rate_Percent': 70,
            'Avg_Starting_Salary_BDT': 30000,
            'Avg_Starting_Salary_USD': 275,
            'Avg_5Year_Salary_BDT': 70000,
            'Avg_5Year_Salary_USD': 640,
            'Underemployment_Rate_Percent': 20,
            'Foreign_Employment_Potential': 'High',
            'Domestic_Demand': 'High',
            'Global_Avg_Salary_USD': 4500,
            'Skill_Gap': 'Medium-High',
            'Better_Earning_Options': 'Specialized certifications, foreign jobs, R&D',
            'Potential_Increase_USD': 1800
        },
        {
            'Field': 'Civil Engineering',
            'Annual_Graduates': 25000,
            'Employment_Rate_Percent': 65,
            'Avg_Starting_Salary_BDT': 28000,
            'Avg_Starting_Salary_USD': 255,
            'Avg_5Year_Salary_BDT': 65000,
            'Avg_5Year_Salary_USD': 595,
            'Underemployment_Rate_Percent': 25,
            'Foreign_Employment_Potential': 'High',
            'Domestic_Demand': 'High',
            'Global_Avg_Salary_USD': 4000,
            'Skill_Gap': 'Medium',
            'Better_Earning_Options': 'Project management, foreign projects, specialization',
            'Potential_Increase_USD': 1500
        },
        {
            'Field': 'Mechanical Engineering',
            'Annual_Graduates': 20000,
            'Employment_Rate_Percent': 60,
            'Avg_Starting_Salary_BDT': 27000,
            'Avg_Starting_Salary_USD': 245,
            'Avg_5Year_Salary_BDT': 60000,
            'Avg_5Year_Salary_USD': 545,
            'Underemployment_Rate_Percent': 30,
            'Foreign_Employment_Potential': 'Medium-High',
            'Domestic_Demand': 'Medium',
            'Global_Avg_Salary_USD': 4200,
            'Skill_Gap': 'High',
            'Better_Earning_Options': 'Automation, robotics, foreign jobs, manufacturing',
            'Potential_Increase_USD': 1600
        },
        {
            'Field': 'Textile Engineering',
            'Annual_Graduates': 15000,
            'Employment_Rate_Percent': 80,
            'Avg_Starting_Salary_BDT': 25000,
            'Avg_Starting_Salary_USD': 230,
            'Avg_5Year_Salary_BDT': 55000,
            'Avg_5Year_Salary_USD': 500,
            'Underemployment_Rate_Percent': 10,
            'Foreign_Employment_Potential': 'Medium',
            'Domestic_Demand': 'Very High',
            'Global_Avg_Salary_USD': 3500,
            'Skill_Gap': 'Low',
            'Better_Earning_Options': 'Management roles, quality control, exports',
            'Potential_Increase_USD': 1000
        },
        
        # Business & Management
        {
            'Field': 'Business Administration (BBA/MBA)',
            'Annual_Graduates': 80000,
            'Employment_Rate_Percent': 55,
            'Avg_Starting_Salary_BDT': 25000,
            'Avg_Starting_Salary_USD': 230,
            'Avg_5Year_Salary_BDT': 60000,
            'Avg_5Year_Salary_USD': 545,
            'Underemployment_Rate_Percent': 35,
            'Foreign_Employment_Potential': 'Medium',
            'Domestic_Demand': 'High',
            'Global_Avg_Salary_USD': 4500,
            'Skill_Gap': 'Medium-High',
            'Better_Earning_Options': 'Specialized MBA, certifications, entrepreneurship',
            'Potential_Increase_USD': 1500
        },
        {
            'Field': 'Accounting & Finance',
            'Annual_Graduates': 40000,
            'Employment_Rate_Percent': 65,
            'Avg_Starting_Salary_BDT': 28000,
            'Avg_Starting_Salary_USD': 255,
            'Avg_5Year_Salary_BDT': 70000,
            'Avg_5Year_Salary_USD': 640,
            'Underemployment_Rate_Percent': 25,
            'Foreign_Employment_Potential': 'High',
            'Domestic_Demand': 'High',
            'Global_Avg_Salary_USD': 5000,
            'Skill_Gap': 'Medium',
            'Better_Earning_Options': 'CA, CFA, ACCA, foreign jobs, consulting',
            'Potential_Increase_USD': 2000
        },
        
        # Medical & Health Sciences
        {
            'Field': 'Medicine (MBBS)',
            'Annual_Graduates': 8000,
            'Employment_Rate_Percent': 90,
            'Avg_Starting_Salary_BDT': 50000,
            'Avg_Starting_Salary_USD': 455,
            'Avg_5Year_Salary_BDT': 120000,
            'Avg_5Year_Salary_USD': 1090,
            'Underemployment_Rate_Percent': 5,
            'Foreign_Employment_Potential': 'Very High',
            'Domestic_Demand': 'Very High',
            'Global_Avg_Salary_USD': 8000,
            'Skill_Gap': 'Low-Medium',
            'Better_Earning_Options': 'Specialization, foreign practice, private practice',
            'Potential_Increase_USD': 4000
        },
        {
            'Field': 'Nursing',
            'Annual_Graduates': 12000,
            'Employment_Rate_Percent': 85,
            'Avg_Starting_Salary_BDT': 20000,
            'Avg_Starting_Salary_USD': 180,
            'Avg_5Year_Salary_BDT': 40000,
            'Avg_5Year_Salary_USD': 365,
            'Underemployment_Rate_Percent': 10,
            'Foreign_Employment_Potential': 'Very High',
            'Domestic_Demand': 'High',
            'Global_Avg_Salary_USD': 3500,
            'Skill_Gap': 'Medium',
            'Better_Earning_Options': 'Foreign jobs (Europe, Middle East, USA)',
            'Potential_Increase_USD': 2000
        },
        {
            'Field': 'Pharmacy',
            'Annual_Graduates': 10000,
            'Employment_Rate_Percent': 70,
            'Avg_Starting_Salary_BDT': 25000,
            'Avg_Starting_Salary_USD': 230,
            'Avg_5Year_Salary_BDT': 55000,
            'Avg_5Year_Salary_USD': 500,
            'Underemployment_Rate_Percent': 20,
            'Foreign_Employment_Potential': 'Medium-High',
            'Domestic_Demand': 'High',
            'Global_Avg_Salary_USD': 4000,
            'Skill_Gap': 'Medium',
            'Better_Earning_Options': 'Clinical pharmacy, research, foreign jobs',
            'Potential_Increase_USD': 1500
        },
        
        # Sciences
        {
            'Field': 'Mathematics & Statistics',
            'Annual_Graduates': 8000,
            'Employment_Rate_Percent': 50,
            'Avg_Starting_Salary_BDT': 22000,
            'Avg_Starting_Salary_USD': 200,
            'Avg_5Year_Salary_BDT': 50000,
            'Avg_5Year_Salary_USD': 455,
            'Underemployment_Rate_Percent': 40,
            'Foreign_Employment_Potential': 'High',
            'Domestic_Demand': 'Medium',
            'Global_Avg_Salary_USD': 5500,
            'Skill_Gap': 'High',
            'Better_Earning_Options': 'Data science, AI/ML, actuarial science, research',
            'Potential_Increase_USD': 2500
        },
        {
            'Field': 'Physics & Chemistry',
            'Annual_Graduates': 10000,
            'Employment_Rate_Percent': 45,
            'Avg_Starting_Salary_BDT': 20000,
            'Avg_Starting_Salary_USD': 180,
            'Avg_5Year_Salary_BDT': 45000,
            'Avg_5Year_Salary_USD': 410,
            'Underemployment_Rate_Percent': 45,
            'Foreign_Employment_Potential': 'Medium',
            'Domestic_Demand': 'Low-Medium',
            'Global_Avg_Salary_USD': 5000,
            'Skill_Gap': 'High',
            'Better_Earning_Options': 'Research, teaching abroad, industry R&D, upskilling',
            'Potential_Increase_USD': 2000
        },
        
        # Social Sciences & Humanities
        {
            'Field': 'Economics',
            'Annual_Graduates': 15000,
            'Employment_Rate_Percent': 55,
            'Avg_Starting_Salary_BDT': 24000,
            'Avg_Starting_Salary_USD': 220,
            'Avg_5Year_Salary_BDT': 55000,
            'Avg_5Year_Salary_USD': 500,
            'Underemployment_Rate_Percent': 35,
            'Foreign_Employment_Potential': 'Medium-High',
            'Domestic_Demand': 'Medium',
            'Global_Avg_Salary_USD': 5000,
            'Skill_Gap': 'Medium-High',
            'Better_Earning_Options': 'Data analytics, policy research, international orgs',
            'Potential_Increase_USD': 2000
        },
        {
            'Field': 'English & Literature',
            'Annual_Graduates': 20000,
            'Employment_Rate_Percent': 50,
            'Avg_Starting_Salary_BDT': 20000,
            'Avg_Starting_Salary_USD': 180,
            'Avg_5Year_Salary_BDT': 40000,
            'Avg_5Year_Salary_USD': 365,
            'Underemployment_Rate_Percent': 40,
            'Foreign_Employment_Potential': 'Medium',
            'Domestic_Demand': 'Medium',
            'Global_Avg_Salary_USD': 3500,
            'Skill_Gap': 'Medium',
            'Better_Earning_Options': 'Content writing, teaching abroad, translation, editing',
            'Potential_Increase_USD': 1200
        },
        {
            'Field': 'Law',
            'Annual_Graduates': 12000,
            'Employment_Rate_Percent': 60,
            'Avg_Starting_Salary_BDT': 30000,
            'Avg_Starting_Salary_USD': 275,
            'Avg_5Year_Salary_BDT': 80000,
            'Avg_5Year_Salary_USD': 730,
            'Underemployment_Rate_Percent': 30,
            'Foreign_Employment_Potential': 'Medium',
            'Domestic_Demand': 'High',
            'Global_Avg_Salary_USD': 6000,
            'Skill_Gap': 'Medium',
            'Better_Earning_Options': 'Corporate law, international law, LLM abroad',
            'Potential_Increase_USD': 2500
        },
        
        # Agriculture
        {
            'Field': 'Agriculture',
            'Annual_Graduates': 8000,
            'Employment_Rate_Percent': 55,
            'Avg_Starting_Salary_BDT': 22000,
            'Avg_Starting_Salary_USD': 200,
            'Avg_5Year_Salary_BDT': 45000,
            'Avg_5Year_Salary_USD': 410,
            'Underemployment_Rate_Percent': 35,
            'Foreign_Employment_Potential': 'Medium',
            'Domestic_Demand': 'Medium',
            'Global_Avg_Salary_USD': 4000,
            'Skill_Gap': 'Medium',
            'Better_Earning_Options': 'Agri-tech, research, consulting, entrepreneurship',
            'Potential_Increase_USD': 1500
        }
    ]
    
    return pd.DataFrame(fields)

def analyze_employment_outcomes(df):
    """Analyze employment outcomes"""
    
    print(f"\n{'='*80}")
    print("GRADUATE EMPLOYMENT OUTCOMES")
    print(f"{'='*80}")
    
    total_graduates = df['Annual_Graduates'].sum()
    weighted_employment = (df['Annual_Graduates'] * df['Employment_Rate_Percent']).sum() / total_graduates
    weighted_underemployment = (df['Annual_Graduates'] * df['Underemployment_Rate_Percent']).sum() / total_graduates
    
    employed = total_graduates * (weighted_employment / 100)
    underemployed = employed * (weighted_underemployment / 100)
    unemployed = total_graduates - employed
    
    print(f"\nTotal Annual Graduates: {total_graduates/1e3:.0f}K")
    print(f"Employment Rate: {weighted_employment:.1f}%")
    print(f"Employed: {employed/1e3:.0f}K")
    print(f"Underemployed: {underemployed/1e3:.0f}K ({weighted_underemployment:.1f}%)")
    print(f"Unemployed: {unemployed/1e3:.0f}K ({(unemployed/total_graduates)*100:.1f}%)")
    
    # Salary analysis
    weighted_starting = (df['Annual_Graduates'] * df['Avg_Starting_Salary_USD']).sum() / total_graduates
    weighted_5year = (df['Annual_Graduates'] * df['Avg_5Year_Salary_USD']).sum() / total_graduates
    
    print(f"\n{'-'*80}")
    print("SALARY ANALYSIS:")
    print(f"{'-'*80}")
    print(f"Average Starting Salary: ${weighted_starting:.0f}/month (BDT {weighted_starting*110:.0f})")
    print(f"Average 5-Year Salary: ${weighted_5year:.0f}/month (BDT {weighted_5year*110:.0f})")
    print(f"Growth: {((weighted_5year/weighted_starting)-1)*100:.0f}%")
    
    # By field
    print(f"\n{'-'*80}")
    print("TOP 5 FIELDS BY EMPLOYMENT RATE:")
    print(f"{'-'*80}")
    top_employment = df.nlargest(5, 'Employment_Rate_Percent')[['Field', 'Employment_Rate_Percent', 'Avg_Starting_Salary_USD']]
    for _, row in top_employment.iterrows():
        print(f"{row['Field']:<40} {row['Employment_Rate_Percent']:>3.0f}% | ${row['Avg_Starting_Salary_USD']:>4.0f}/mo")
    
    print(f"\n{'-'*80}")
    print("TOP 5 FIELDS BY STARTING SALARY:")
    print(f"{'-'*80}")
    top_salary = df.nlargest(5, 'Avg_Starting_Salary_USD')[['Field', 'Avg_Starting_Salary_USD', 'Employment_Rate_Percent']]
    for _, row in top_salary.iterrows():
        print(f"{row['Field']:<40} ${row['Avg_Starting_Salary_USD']:>4.0f}/mo | {row['Employment_Rate_Percent']:>3.0f}%")
    
    return {
        'total_graduates': total_graduates,
        'employed': employed,
        'underemployed': underemployed,
        'unemployed': unemployed,
        'avg_starting': weighted_starting,
        'avg_5year': weighted_5year
    }

def analyze_earning_potential(df):
    """Analyze potential for better earnings"""
    
    print(f"\n{'='*80}")
    print("BETTER EARNING OPPORTUNITIES")
    print(f"{'='*80}")
    
    # Calculate gaps
    df['Salary_Gap_USD'] = df['Global_Avg_Salary_USD'] - df['Avg_5Year_Salary_USD']
    df['Potential_Annual_Increase_USD'] = df['Potential_Increase_USD'] * 12
    
    # Total potential
    total_graduates = df['Annual_Graduates'].sum()
    total_current_earning = (df['Annual_Graduates'] * df['Avg_5Year_Salary_USD'] * 12).sum()
    total_potential_earning = (df['Annual_Graduates'] * (df['Avg_5Year_Salary_USD'] + df['Potential_Increase_USD']) * 12).sum()
    total_increase = total_potential_earning - total_current_earning
    
    print(f"\nCurrent Annual Earnings (All Graduates): ${total_current_earning/1e9:.2f}B")
    print(f"Potential Annual Earnings: ${total_potential_earning/1e9:.2f}B")
    print(f"Increase Potential: ${total_increase/1e9:.2f}B ({(total_increase/total_current_earning)*100:.0f}%)")
    
    print(f"\n{'-'*80}")
    print("TOP OPPORTUNITIES BY EARNING INCREASE:")
    print(f"{'-'*80}")
    
    top_opportunities = df.nlargest(10, 'Potential_Increase_USD')[
        ['Field', 'Annual_Graduates', 'Avg_5Year_Salary_USD', 'Potential_Increase_USD', 'Better_Earning_Options']
    ]
    
    for _, row in top_opportunities.iterrows():
        current = row['Avg_5Year_Salary_USD']
        potential = row['Potential_Increase_USD']
        increase_pct = (potential / current) * 100
        print(f"\n{row['Field']}:")
        print(f"  Graduates: {row['Annual_Graduates']/1000:.0f}K/year")
        print(f"  Current: ${current:.0f}/mo | Potential: +${potential:.0f}/mo ({increase_pct:.0f}% increase)")
        print(f"  Options: {row['Better_Earning_Options']}")
    
    return total_increase

def generate_recommendations(df):
    """Generate recommendations"""
    
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS FOR BETTER EARNINGS")
    print(f"{'='*80}")
    
    print(f"\n1. HIGH-DEMAND SKILLS TRAINING:")
    print(f"   - Data Science & AI/ML")
    print(f"   - Cloud Computing (AWS, Azure, GCP)")
    print(f"   - Cybersecurity")
    print(f"   - Digital Marketing")
    print(f"   - Project Management (PMP, Agile)")
    
    print(f"\n2. PROFESSIONAL CERTIFICATIONS:")
    print(f"   - CA, CFA, ACCA (Finance)")
    print(f"   - PMP, Six Sigma (Management)")
    print(f"   - AWS, Google Cloud (IT)")
    print(f"   - USMLE, PLAB (Medical)")
    print(f"   - CPA, CMA (Accounting)")
    
    print(f"\n3. FOREIGN EMPLOYMENT:")
    print(f"   - IT professionals to USA, Europe, Middle East")
    print(f"   - Doctors/Nurses to UK, Germany, Middle East")
    print(f"   - Engineers to Middle East, Southeast Asia")
    print(f"   - Accountants to Middle East, Singapore")
    
    print(f"\n4. FREELANCING & REMOTE WORK:")
    print(f"   - Software development")
    print(f"   - Graphic design & animation")
    print(f"   - Content writing")
    print(f"   - Digital marketing")
    print(f"   - Consulting")
    
    print(f"\n5. ENTREPRENEURSHIP:")
    print(f"   - Tech startups")
    print(f"   - E-commerce")
    print(f"   - Consulting firms")
    print(f"   - Training institutes")
    print(f"   - Service businesses")
    
    print(f"\n6. HIGHER EDUCATION ABROAD:")
    print(f"   - Master's/PhD in developed countries")
    print(f"   - Scholarships and funding")
    print(f"   - Work opportunities post-study")
    print(f"   - Better career prospects")

def generate_report(df, employment_data, earning_increase):
    """Generate comprehensive report"""
    
    output_dir = Path('analysis/graduate_education')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save full database
    df.to_csv(output_dir / 'graduate_employment_database.csv', index=False)
    
    # High potential fields
    high_potential = df[df['Potential_Increase_USD'] >= 1500]
    high_potential.to_csv(output_dir / 'high_earning_potential_fields.csv', index=False)
    
    # Low employment fields
    low_employment = df[df['Employment_Rate_Percent'] < 60]
    low_employment.to_csv(output_dir / 'low_employment_fields.csv', index=False)
    
    print(f"\n✓ Reports saved to {output_dir}")

if __name__ == "__main__":
    edu_data = analyze_graduate_education_system()
    df = create_graduate_employment_database()
    employment_data = analyze_employment_outcomes(df)
    earning_increase = analyze_earning_potential(df)
    generate_recommendations(df)
    generate_report(df, employment_data, earning_increase)
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETED!")
    print(f"{'='*80}")

# Made with Bob
