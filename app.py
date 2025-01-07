import numpy as np
import pandas as pd
import os
from datetime import datetime
import numpy as np
import pandas as pd
import os
from datetime import datetime


def categorize_transaction(row):
    """Categorize transaction based on ICICI Bank transaction codes and remarks."""
    remarks = str(row['Transaction Remarks']).lower()
    
    categories = [
        (['bbps', 'bil', 'bpay'], 'Bill Payment'),
        (['imps', 'inf', 'inft', 'neft', 'mmt', 'payc'], 'Fund Transfer'),
        (['bctt', 'n chg', 't chg'], 'Banking Tax'),
        (['dtax', 'idtx'], 'Tax Payment'),
        (['ccwd', 'vat', 'mat', 'nfs'], 'Cardless/ATM Usage'),
        (['eba', 'sgb'], 'Investment'),
        (['lccbrn', 'uccbrn'], 'Cheque Transaction'),
        (['lnpy'], 'Loan Payment'),
        (['onl', 'pac', 'rchg', 'top', 'smo'], 'Other Services'),
    ]
    
    for keywords, category in categories:
        if any(keyword in remarks for keyword in keywords):
            return category
    
    return 'Miscellaneous'

def generate_transaction_insights(row):
    """Generate insights based on ICICI Bank transaction types"""
    remarks = str(row['Transaction Remarks']).lower()
    insights = []
    
    if any(code in remarks for code in ['vat', 'mat', 'nfs']):
        insights.append("Other bank ATM usage - May incur charges")
    elif any(code in remarks for code in ['n chg', 't chg', 'bctt']):
        insights.append("Banking charges applied")
    elif any(code in remarks for code in ['eba', 'sgb']):
        insights.append("Investment transaction")
    elif any(code in remarks for code in ['bbps', 'bil', 'bpay']):
        insights.append("Utility/Bill payment")
    elif any(code in remarks for code in ['dtax', 'idtx']):
        insights.append("Tax payment")
    elif any(code in remarks for code in ['lnpy']):
        insights.append("Loan payment - Check for timely credit")
    
    return '; '.join(insights) if insights else 'Regular transaction'

def analyze_transactions_for_all_months(months, input_dir='statements', output_dir='statements'):
    """
    Comprehensive transaction analysis and reporting for multiple months.
    """
    all_monthly_data = []
    
    for month in months:
        print(f"Processing transactions for {month}...")
        month_folder = os.path.join(input_dir, month)
        if not os.path.exists(month_folder):
            print(f"Warning: Folder for {month} not found. Skipping.")
            continue
        
        result = analyze_transactions(month, input_dir, output_dir)
        if result is not None:
            all_monthly_data.append(result)
    
    if all_monthly_data:
        all_data = pd.concat(all_monthly_data, ignore_index=True)
        all_data_file = os.path.join(output_dir, 'all_months_transaction_analysis.xlsx')
        all_data.to_excel(all_data_file, index=False)
        print(f"All months combined analysis saved to: {all_data_file}")
    
    return all_monthly_data

def analyze_transactions(month, input_dir='statements', output_dir='statements'):
    """
    Comprehensive transaction analysis and reporting for a single month.
    """
    file_path = os.path.join(input_dir, month, 'transaction.xlsx')
    output_file = os.path.join(output_dir, month, f'{month}_Transaction_Analysis.xlsx')
    
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df = pd.read_excel(file_path)
        
        required_columns = ['Transaction Date', 'Deposit Amount (INR )', 'Withdrawal Amount (INR )', 'Transaction Remarks', 'Balance (INR )']
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], dayfirst=True, errors='coerce')
        if df['Transaction Date'].isna().any():
            print(f"Warning: Invalid dates found in {month}")

        df['Transaction Type'] = df.apply(determine_transaction_type, axis=1)
        df['Transaction Category'] = df.apply(categorize_transaction, axis=1)
        df['Transaction Insights'] = df.apply(generate_transaction_insights, axis=1)
        
        df['Cumulative Inflow'] = df['Deposit Amount (INR )'].fillna(0).cumsum()
        df['Cumulative Outflow'] = df['Withdrawal Amount (INR )'].fillna(0).cumsum()
        df['Net Cash Flow'] = df['Cumulative Inflow'] - df['Cumulative Outflow']
        
        # Format amounts
        for col in ['Withdrawal Amount (INR )', 'Deposit Amount (INR )', 'Balance (INR )', 'Net Cash Flow']:
            df[f'Formatted_{col}'] = df[col].apply(format_inr)
        
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Detailed Transactions', index=False)
            create_summary_sheets(df, writer)
        
        print(f"Analysis completed for {month}")
        return df
    
    except Exception as e:
        print(f"Error processing {month}: {e}")
        return None

def format_inr(amount):
    """Format amount in Indian Rupee format"""
    if pd.isna(amount):
        return "N/A"
    
    is_negative = amount < 0
    amount = abs(amount)
    amount_str = f"{amount:,.2f}"
    integer_part, decimal_part = amount_str.split('.')
    integer_part = integer_part.replace(',', '')
    
    if len(integer_part) <= 3:
        formatted_integer = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        
        groups = []
        for i in range(len(remaining), 0, -2):
            start = max(0, i - 2)
            groups.insert(0, remaining[start:i])
        
        groups.append(last_three)
        formatted_integer = ','.join(groups)
    
    sign = '-' if is_negative else ''
    return f"{sign}₹{formatted_integer}.{decimal_part}"

def determine_transaction_type(row):
    """Determine transaction type based on amount and remarks"""
    withdrawal = row['Withdrawal Amount (INR )']
    deposit = row['Deposit Amount (INR )']
    remarks = str(row['Transaction Remarks']).lower()
    
    if pd.notna(withdrawal) and withdrawal > 0:
        return 'Fund Transfer (Outgoing)' if 'transfer' in remarks else \
               'Salary Deduction' if 'salary' in remarks else 'Expense'
    
    if pd.notna(deposit) and deposit > 0:
        return 'Salary Credit' if 'salary' in remarks else \
               'Refund' if 'refund' in remarks else \
               'Fund Transfer (Incoming)' if 'transfer' in remarks else 'Income'
    
    return 'Unknown'

def create_summary_sheets(df, writer):
    """Create summary sheets in Excel"""
    metrics = ['count', 'sum', 'mean', 'median']
    
    # Transaction summaries
    for group_by in ['Transaction Type', 'Transaction Category']:
        summary = df.groupby(group_by)['Balance (INR )'].agg(metrics)
        summary.to_excel(writer, sheet_name=f'{group_by} Summary')
    
    # Weekly trend
    weekly_trend = df.groupby(pd.Grouper(key='Transaction Date', freq='W'))['Balance (INR )'].agg(metrics)
    weekly_trend.to_excel(writer, sheet_name='Weekly Trend')

if __name__ == "__main__":
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    analyze_transactions_for_all_months(months)