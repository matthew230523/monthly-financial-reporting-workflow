import pandas as pd
import random

# Reproducibility
random.seed(49)

# 12 months
months = pd.date_range(start="2024-01-01", periods=12, freq="MS")

# Departments and realistic categories per department
department_structure = {
    "Sales": ["Revenue", "COGS", "Payroll", "Operating Expense"],
    "Marketing": ["Payroll", "Marketing Expense", "Operating Expense"],
    "Operations": ["COGS", "Payroll", "Operating Expense"],
    "Finance": ["Payroll", "Operating Expense", "Training Expense"],
    "HR": ["Payroll", "Training Expense", "Operating Expense"]
}

rows = []

for month in months:
    for department, categories in department_structure.items():
        for category in categories:

            # -------------------------
            # Set realistic budget logic
            # -------------------------
            if department == "Sales":
                if category == "Revenue":
                    budget = random.randint(150000, 300000)
                    actual = round(budget * random.uniform(0.88, 1.15), 2)

                elif category == "COGS":
                    budget = random.randint(50000, 140000)
                    actual = round(budget * random.uniform(0.92, 1.18), 2)

                elif category == "Payroll":
                    budget = random.randint(30000, 70000)
                    actual = round(budget * random.uniform(0.97, 1.08), 2)

                elif category == "Operating Expense":
                    budget = random.randint(10000, 35000)
                    actual = round(budget * random.uniform(0.90, 1.12), 2)

            elif department == "Marketing":
                if category == "Payroll":
                    budget = random.randint(25000, 60000)
                    actual = round(budget * random.uniform(0.97, 1.08), 2)

                elif category == "Marketing Expense":
                    budget = random.randint(40000, 120000)
                    actual = round(budget * random.uniform(0.80, 1.25), 2)

                elif category == "Operating Expense":
                    budget = random.randint(8000, 25000)
                    actual = round(budget * random.uniform(0.90, 1.15), 2)

            elif department == "Operations":
                if category == "COGS":
                    budget = random.randint(70000, 180000)
                    actual = round(budget * random.uniform(0.90, 1.20), 2)

                elif category == "Payroll":
                    budget = random.randint(40000, 90000)
                    actual = round(budget * random.uniform(0.97, 1.10), 2)

                elif category == "Operating Expense":
                    budget = random.randint(30000, 90000)
                    actual = round(budget * random.uniform(0.88, 1.15), 2)

            elif department == "Finance":
                if category == "Payroll":
                    budget = random.randint(25000, 55000)
                    actual = round(budget * random.uniform(0.97, 1.07), 2)

                elif category == "Operating Expense":
                    budget = random.randint(10000, 30000)
                    actual = round(budget * random.uniform(0.90, 1.12), 2)

                elif category == "Training Expense":
                    budget = random.randint(3000, 12000)
                    actual = round(budget * random.uniform(0.85, 1.20), 2)

            elif department == "HR":
                if category == "Payroll":
                    budget = random.randint(20000, 50000)
                    actual = round(budget * random.uniform(0.97, 1.08), 2)

                elif category == "Training Expense":
                    budget = random.randint(8000, 25000)
                    actual = round(budget * random.uniform(0.85, 1.20), 2)

                elif category == "Operating Expense":
                    budget = random.randint(5000, 18000)
                    actual = round(budget * random.uniform(0.90, 1.15), 2)

            # -------------------------
            # Save row
            # -------------------------
            rows.append([
                month.strftime("%Y-%m-%d"),
                department,
                category,
                budget,
                actual
            ])

# Create DataFrame
df = pd.DataFrame(rows, columns=[
    "month",
    "department",
    "account_category",
    "budget_amount",
    "actual_amount"
])

# Save to CSV
df.to_csv(r"C:\Users\ziore\OneDrive\Documents\Python\Github portfolio\Database\budget_actuals.csv", index=False)

# Preview
print("Dataset created successfully: budget_actuals.csv")
print(df.head(15))
print(f"\nTotal rows: {len(df)}")