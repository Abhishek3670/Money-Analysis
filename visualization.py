import os
import matplotlib.pyplot as plt
import pandas as pd

def visualize_transactions(df, output_dir, month):
    """Generate and save visualizations for the transactions."""
    reports_dir = os.path.join(output_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Total Income vs. Total Expenses
    monthly_summary = df.groupby(df['Transaction Date'].dt.to_period('M')).agg({
        'Deposit Amount (INR )': 'sum',
        'Withdrawal Amount (INR )': 'sum'
    }).rename(columns={'Deposit Amount (INR )': 'Total Income', 'Withdrawal Amount (INR )': 'Total Expenses'})
    
    monthly_summary.plot(kind='bar', stacked=True)
    plt.title('Total Income vs. Total Expenses')
    plt.xlabel('Month')
    plt.ylabel('Amount (INR)')
    plt.savefig(os.path.join(reports_dir, 'total_income_expenses.png'))
    plt.close()
    
    # Category Breakdown
    category_summary = df['Transaction Category'].value_counts()
    category_summary.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Category Breakdown')
    plt.ylabel('')
    plt.savefig(os.path.join(reports_dir, 'category_breakdown.png'))
    plt.close()
    
    # Cumulative Balance Over Time
    df.set_index('Transaction Date')['Balance (INR )'].plot()
    plt.title('Cumulative Balance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Balance (INR)')
    plt.savefig(os.path.join(reports_dir, 'balance_over_time.png'))
    plt.close()
    
    # Income vs. Expense Trend
    trend_summary = monthly_summary.copy()
    trend_summary.plot(kind='bar', stacked=True)
    plt.title('Income vs. Expense Trend')
    plt.xlabel('Month')
    plt.ylabel('Amount (INR)')
    plt.savefig(os.path.join(reports_dir, 'income_expense_trend.png'))
    plt.close()
    
    # Large Transactions
    large_transactions = df[(df['Deposit Amount (INR )'] > 100000) | (df['Withdrawal Amount (INR )'] > 100000)]
    with pd.ExcelWriter(os.path.join(reports_dir, 'large_transactions_report.xlsx')) as writer:
        large_transactions.to_excel(writer, sheet_name='Large Transactions', index=False)

def extract_insights(df, output_dir):
    """Extract and save insights from the transactions."""
    reports_dir = os.path.join(output_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Monthly savings rate
    monthly_summary = df.groupby(df['Transaction Date'].dt.to_period('M')).agg({
        'Deposit Amount (INR )': 'sum',
        'Withdrawal Amount (INR )': 'sum'
    })
    monthly_summary['Savings Rate'] = (monthly_summary['Deposit Amount (INR )'] - monthly_summary['Withdrawal Amount (INR )']) / monthly_summary['Deposit Amount (INR )'] * 100
    
    # Trends in spending categories
    category_trends = df.groupby([df['Transaction Date'].dt.to_period('M'), 'Transaction Category']).agg({
        'Withdrawal Amount (INR )': 'sum'
    }).unstack().fillna(0)
    
    # Save insights to Excel
    insights_summary = monthly_summary[['Deposit Amount (INR )', 'Withdrawal Amount (INR )', 'Savings Rate']]
    with pd.ExcelWriter(os.path.join(reports_dir, 'insights_summary.xlsx')) as writer:
        insights_summary.to_excel(writer, sheet_name='Insights Summary')
        category_trends.to_excel(writer, sheet_name='Category Trends')
    
    # Save insights to text file
    insights_text = f"Total Income: {monthly_summary['Deposit Amount (INR )'].sum()}\n"
    insights_text += f"Total Expenses: {monthly_summary['Withdrawal Amount (INR )'].sum()}\n"
    insights_text += f"Savings Rate: {monthly_summary['Savings Rate'].mean():.2f}%\n"
    insights_text += "Major Spending Categories:\n"
    for category, amount in category_trends.sum().items():
        insights_text += f"  {category}: {amount}\n"
    
    with open(os.path.join(reports_dir, 'insights_summary.txt'), 'w') as f:
        f.write(insights_text)
