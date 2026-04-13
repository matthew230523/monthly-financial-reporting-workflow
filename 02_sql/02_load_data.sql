COPY budget_actuals (report_month, department, account_category, budget_amount, actual_amount)
FROM 'C:/temp/budget_actuals_v2_improved.csv'
DELIMITER ','
CSV HEADER;