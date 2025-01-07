# ICICI Bank Transaction Analyzer

## Overview
The ICICI Bank Transaction Analyzer is a Python script designed to process, categorize, and analyze bank transaction statements. It generates detailed reports in Excel format, including summaries, insights, and trends for monthly and yearly data.

## Features
- **Transaction Categorization**: Classifies transactions based on remarks and codes (e.g., Bill Payment, Fund Transfer, Investment, etc.).
- **Insights Generation**: Provides insights for transactions such as charges, investments, and loan payments.
- **Summarized Reports**: Creates summary sheets grouped by transaction type, category, and weekly trends.
- **Cumulative Calculations**: Tracks cumulative inflow, outflow, and net cash flow.
- **Formatted Output**: Displays monetary values in Indian Rupee format for better readability.
- **Batch Processing**: Analyzes transactions for multiple months and combines them into a single report.

## Requirements
- Python 3.8 or higher
- Required Libraries:
  - `pandas`
  - `numpy`
  - `openpyxl`
  - `xlsxwriter`

You can install the required libraries using:
```bash
pip install pandas numpy openpyxl xlsxwriter

Folder Structure
The script expects the following folder structure:

markdown
Copy code
statements/
  JAN/
    transaction.xlsx
  FEB/
    transaction.xlsx
  ...
  DEC/
    transaction.xlsx
Input files must be named transaction.xlsx and placed in the respective month's folder.
Output files will be saved in the same structure under statements/{month}/{month}_Transaction_Analysis.xlsx.
Usage
1. Run the Script
To analyze transactions for all months:

bash
Copy code
python transaction_analyzer.py
2. File Outputs
Monthly Analysis: For each month, a detailed Excel report is saved in statements/{month}/{month}_Transaction_Analysis.xlsx.
Combined Analysis: All months' data is compiled into statements/all_months_transaction_analysis.xlsx.
3. Customization
To process specific months, edit the months list in the script:

python
Copy code
months = ['JAN', 'FEB', 'MAR']
Script Functions
categorize_transaction(row)
Classifies transactions based on their remarks using predefined keywords.

generate_transaction_insights(row)
Provides insights for transactions, such as:

"Other bank ATM usage - May incur charges"
"Banking charges applied"
"Investment transaction"
analyze_transactions(month, input_dir, output_dir)
Processes transactions for a single month:

Reads the input Excel file.
Categorizes transactions and generates insights.
Calculates cumulative inflow, outflow, and net cash flow.
Formats monetary values and saves a detailed Excel report.
analyze_transactions_for_all_months(months, input_dir, output_dir)
Processes transactions for all specified months:

Iterates through the list of months.
Calls analyze_transactions for each available month.
Combines all monthly data into a single Excel file (all_months_transaction_analysis.xlsx).
format_inr(amount)
Formats monetary amounts into Indian Rupee format for better readability, including handling negative values.

determine_transaction_type(row)
Identifies the transaction type based on the withdrawal or deposit amount and transaction remarks.

create_summary_sheets(df, writer)
Generates summary sheets in the Excel file:

Grouped by transaction type and category.
Weekly trends with metrics like count, sum, mean, and median.
Error Handling
Missing folders or files are skipped with a warning message.
Invalid or missing columns in the input files raise a ValueError.
Invalid dates are logged as warnings.
Example Output
Detailed Transactions: A sheet containing all transactions with columns like Transaction Type, Category, Insights, Cumulative Inflow/Outflow, and Net Cash Flow.
Summaries:
Grouped by transaction type or category with metrics.
Weekly trends showing balance statistics.
Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or a pull request.