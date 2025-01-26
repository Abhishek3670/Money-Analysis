import os
import pandas as pd

def generate_monthly_report(df, output_dir, month):
    """Generate a brief report for the month with rating and user performance."""
    reports_dir = os.path.join(output_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    total_income = df['Deposit Amount (INR )'].sum()
    total_expenses = df['Withdrawal Amount (INR )'].sum()
    savings = total_income - total_expenses
    savings_rate = (savings / total_income) * 100 if total_income > 0 else 0
    
    rating = 'Excellent' if savings_rate > 20 else 'Good' if savings_rate > 10 else 'Average' if savings_rate > 0 else 'Poor'
    
    report_text = f"Monthly Report for {month}\n"
    report_text += f"Total Income: {total_income}\n"
    report_text += f"Total Expenses: {total_expenses}\n"
    report_text += f"Savings: {savings}\n"
    report_text += f"Savings Rate: {savings_rate:.2f}%\n"
    report_text += f"Rating: {rating}\n"
    
    with open(os.path.join(reports_dir, f'{month}_report.txt'), 'w') as f:
        f.write(report_text)

def generate_yearly_report(all_monthly_data, output_dir):
    """Generate a brief yearly report with rating and user performance."""
    reports_dir = os.path.join(output_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    yearly_data = pd.concat(all_monthly_data, ignore_index=True)
    total_income = yearly_data['Deposit Amount (INR )'].sum()
    total_expenses = yearly_data['Withdrawal Amount (INR )'].sum()
    savings = total_income - total_expenses
    savings_rate = (savings / total_income) * 100 if total_income > 0 else 0
    
    rating = 'Excellent' if savings_rate > 20 else 'Good' if savings_rate > 10 else 'Average' if savings_rate > 0 else 'Poor'
    
    report_text = "Yearly Report\n"
    report_text += f"Total Income: {total_income}\n"
    report_text += f"Total Expenses: {total_expenses}\n"
    report_text += f"Savings: {savings}\n"
    report_text += f"Savings Rate: {savings_rate:.2f}%\n"
    report_text += f"Rating: {rating}\n"
    
    with open(os.path.join(reports_dir, 'yearly_report.txt'), 'w') as f:
        f.write(report_text)
