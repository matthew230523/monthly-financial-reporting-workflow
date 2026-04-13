import pandas as pd
from sqlalchemy import create_engine


# 1. Connect to PostgreSQL
engine = create_engine("postgresql+psycopg2://username:yourpassword@localhost:5432/your_database")

# 2. SQL query
query = """
SELECT *
FROM budget_actuals;
"""

# 3. Pull SQL results into pandas DataFrame
df = pd.read_sql(query, engine)


# Add variance columns
df['variance_amount'] = df['actual_amount'] - df['budget_amount']
df['variance_percent'] = (df['variance_amount'] / df['budget_amount']) * 100

# Rounding to 2 decimals

df['variance_amount'] = df['variance_amount'].round(2)
df['variance_percent'] = df['variance_percent'].round(2)

# Biggest variances - TOP 5
top_variances = df.sort_values( by = 'variance_amount', ascending = False).head(5)

# 4. Show results
print(df.head())
print(df.columns)
print(top_variances)
