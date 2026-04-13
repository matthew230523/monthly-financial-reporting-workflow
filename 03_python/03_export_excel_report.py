import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/your_database")
query = "SELECT * FROM budget_actuals;"
df = pd.read_sql(query, engine)

# ----------------------------
# STAGE 3 / 4 DATA PREPARATION
# ----------------------------

# Add variance columns
df['variance_amount'] = df['actual_amount'] - df['budget_amount']
df['variance_percent'] = (df['variance_amount'] / df['budget_amount']) * 100

# Rounding to 2 decimals

df['variance_amount'] = df['variance_amount'].round(2)
df['variance_percent'] = df['variance_percent'].round(2)


# Convert month column to datetime
df['report_month'] = pd.to_datetime(df['report_month'])

# Create quarter column (Q1, Q2, Q3, Q4)
df['quarter'] = df['report_month'].dt.to_period('Q').astype(str)


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

# ------------------------------------------------------------
# 1. SUMMARY KPIs
# ------------------------------------------------------------

total_budget = df['budget_amount'].sum()
total_actual = df['actual_amount'].sum()
total_variance = df['variance_amount'].sum()
total_variance_percent = (total_variance / total_budget) * 100 if total_budget != 0 else 0

total_budget_net = df['signed_budget'].sum()
total_actual_net = df['signed_actual'].sum()
total_variance_net = total_actual_net - total_budget_net

summary_kpis = pd.DataFrame({
    'KPI': [
        'Total Budget',
        'Total Actual',
        'Total Variance',
        'Total Variance %', 
        'Budget Net Result',
        'Actual Net Result',
        'Net Result Variance'
    ],
    'Value': [ 
        round(total_budget, 2),
        round(total_actual, 2),
        round(total_variance, 2),
        round(total_variance_percent, 2),
        round(total_budget_net, 2),
        round(total_actual_net, 2),
        round(total_variance_net, 2)
    ]
})


# ----------------------------------------------
# 2. QUARTER VARIANCE 
# ----------------------------------------------

quarter_variance = df.groupby('quarter').agg(
    total_budget = ('budget_amount', 'sum'),
    total_actual = ('actual_amount','sum'),
    total_variance = ('variance_amount','sum')
).reset_index()

quarter_variance['variance_percent'] = (
    quarter_variance['total_variance'] / quarter_variance['total_budget']
) * 100

quarter_variance = quarter_variance.round(2)


# -------------------------------------------------
# 3. DEPARTMENT VARIANCE
# -------------------------------------------------

department_variance = df.groupby(['quarter', 'department']).agg(
    total_budget = ('budget_amount', 'sum'),
    total_actual = ('actual_amount','sum'),
    total_variance = ('variance_amount','sum')
).reset_index()

department_variance['variance_percent'] = (
    department_variance['total_variance'] / department_variance['total_budget']
) * 100 

department_variance['absolute_variance'] = department_variance['total_variance'].abs()
department_variance = department_variance.round(2)

# Closest to budget by quarter 
best_department_by_quarter = department_variance.loc[
    department_variance.groupby('quarter')['absolute_variance'].idxmin()
].reset_index(drop = True)



# --------------------------------------------------------
# 4. QUARTER NET RESULTS
# --------------------------------------------------------

quarter_net_result = df.groupby('quarter').agg(
    budget_net_result = ('signed_budget','sum'),
    actual_net_result = ('signed_actual','sum')
).reset_index()

quarter_net_result['net_result_variance'] = (
    quarter_net_result['actual_net_result'] - quarter_net_result['budget_net_result']
)


# --------------------------------------------------
# 5. MONTHLY TREND
# -------------------------------------------------

monthly_trend = df.groupby('report_month').agg(
    total_budget = ('budget_amount', 'sum'),
    total_actual = ('actual_amount','sum'),
    total_variance = ('variance_amount','sum'),
    budget_net_result = ('signed_budget','sum'),
    actual_net_result = ('signed_actual','sum')
).reset_index()

monthly_trend['variance_percent'] = (
    monthly_trend['total_variance'] / monthly_trend['total_budget']
) * 100

monthly_trend['net_result_variance'] = (
    monthly_trend['actual_net_result'] - monthly_trend['budget_net_result']
)
monthly_trend = monthly_trend.round(2)


# Prettier month format for Excel display
monthly_trend['report_month'] = monthly_trend['report_month'].dt.strftime('%Y-%m')


# ----------------------------------------------------------
# 6. CATEGORY ANALYSIS
# ---------------------------------------------------------


category_analysis = df.groupby(['quarter', 'account_category']).agg(
    total_budget = ('budget_amount', 'sum'),
    total_actual = ('actual_amount','sum'),
    total_variance = ('variance_amount','sum')
).reset_index()

category_analysis['variance_percent'] = (
    category_analysis['total_variance'] / category_analysis['total_budget']
) * 100

category_analysis = category_analysis.round(2)

# ------------------------------------------------------------
# 7. FULL DATA
# -----------------------------------------------------------

full_data = df.copy()

# Prettier month format in full_data too
full_data['report_month'] = full_data['report_month'].dt.strftime('%Y - %m - %d')

# ----------------------------------------------------------------
# STAGE 4 - EXPORT TO EXCEL 
# ----------------------------------------------------------------

output_path = r"C:\Users\ziore\OneDrive\Documents\Python\Github portfolio\monthly-financial-reporting-workflow\04_output\monthly_financial_report.xlsx"

with pd.ExcelWriter(output_path, engine = 'openpyxl') as writer:
    summary_kpis.to_excel(writer, sheet_name = 'summary_kpis', index = False)
    quarter_variance.to_excel(writer, sheet_name = 'quarter_variance', index = False)
    department_variance.to_excel(writer, sheet_name = 'department_variance', index = False)
    best_department_by_quarter.to_excel(writer, sheet_name = 'best_department_qtr', index = False)
    quarter_net_result.to_excel(writer, sheet_name = 'quarter_net_result', index = False)
    monthly_trend.to_excel(writer, sheet_name = 'monthly_trend', index = False)
    category_analysis.to_excel(writer, sheet_name = 'category_analysis', index = False)
    full_data.to_excel(writer, sheet_name = 'full_data', index = False) 

print(f"Business-style Excel report exported succesfully to:\n{output_path}")