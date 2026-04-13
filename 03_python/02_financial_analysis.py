import pandas as pd
from sqlalchemy import create_engine

# Connecting to PostgreSQL:

engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/database_name")
query = "SELECT * FROM budget_actuals;"
df = pd.read_sql(query, engine)


# Add variance columns
df['variance_amount'] = df['actual_amount'] - df['budget_amount']
df['variance_percent'] = (df['variance_amount'] / df['budget_amount']) * 100

# Rounding variance columns to 2 decimals
df['variance_amount'] = df['variance_amount'].round(2)
df['variance_percent'] = df['variance_percent'].round(2)

# Convert month column to datetime
df['report_month'] = pd.to_datetime(df['report_month'])


# -------- QUARTER ANALYSIS --------------

# Create quarter column (Q1, Q2, Q3, Q4)
df['quarter'] = df['report_month'].dt.to_period('Q').astype(str)


# Quarterly variance summary 
quarter_summary = df.groupby('quarter').agg(
    total_budget = ('budget_amount', 'sum'),
    total_actual = ('actual_amount', 'sum'), 
    total_variance = ('variance_amount', 'sum')
).reset_index()


# Calculate quarterly variance %
quarter_summary['variance_percent'] = (
    quarter_summary['total_variance'] / quarter_summary['total_budget']
) * 100

# Round values
quarter_summary['total_budget'] = quarter_summary['total_budget'].round(2)
quarter_summary['total_actual'] = quarter_summary['total_actual'].round(2)
quarter_summary['total_variance'] = quarter_summary['total_variance'].round(2)
quarter_summary['variance_percent'] = quarter_summary['variance_percent'].round(2)


print("Quarterly Variance Summary:")
print(quarter_summary)


# ------- DEPARTMENT BY QUARTER ANALYSIS ----------

# Best performing department by quarter
department_quarter_summary = df.groupby(['quarter', 'department']).agg(
    total_variance = ('variance_amount', 'sum')
).reset_index()

# Adding absolute variance column
department_quarter_summary['absolute_variance'] = department_quarter_summary['total_variance'].abs()

# Best performing department in each quarter (lowest variance)
best_department_by_quarter = department_quarter_summary.loc[
    department_quarter_summary.groupby('quarter')['absolute_variance'].idxmin()
].reset_index(drop = True)

best_department_by_quarter['total_variance'] = best_department_by_quarter['total_variance'].round(2)
best_department_by_quarter['absolute_variance'] = best_department_by_quarter['absolute_variance'].round(2)

print ('\nBest Performing Department by Quarter:')
print(best_department_by_quarter[['quarter', 'department', 'absolute_variance']])


# ------ NET RESULTS ANALYSIS ---------------------------------

# Create signed actual values: revenue positive, all other categories negative
df['signed_actual'] = df.apply(
    lambda row: row['actual_amount'] if row['account_category'].lower() =='revenue' else - row['actual_amount'],
    axis = 1
)

# Create signed budget values: revenue positive, all other categories negative

df['signed_budget'] = df.apply(

    lambda row: row['budget_amount'] if row['account_category'].lower() == 'revenue' else - row ['budget_amount'],
    axis = 1
)

# Quaterly net result summary
quarter_net_result = df.groupby('quarter').agg(
    budget_net_result = ('signed_budget', 'sum'),
    actual_net_result = ('signed_actual', 'sum')
).reset_index()

quarter_net_result['net_result_variance'] = (
    quarter_net_result['actual_net_result'] - quarter_net_result['budget_net_result']
)

quarter_net_result['budget_net_result'] = quarter_net_result['budget_net_result'].round(2)
quarter_net_result['actual_net_result'] = quarter_net_result['actual_net_result'].round(2)
quarter_net_result['net_result_variance'] = quarter_net_result['net_result_variance'].round(2)

print('\nQuarterly Net Result Summary:')
print(quarter_net_result)
