
-------------------------------------
-- analysis----
-------------------------------------

-- Q1: Total Budget vs Actual for a year and overall variance ---

SELECT 
	ROUND (SUM(budget_amount),0) AS total_budget, 
	ROUND (SUM(actual_amount),0) AS total_actual, 
	ROUND (SUM(actual_amount) - SUM(budget_amount),0) AS variance_amount,
	ROUND ((SUM(actual_amount) - SUM(budget_amount)) / SUM(budget_amount) * 100, 2) AS variance_percent
FROM budget_actuals; 


-- Q2: Department-level variance summary (largest unfavorable variance) --

SELECT
    department,
    ROUND(SUM(budget_amount),0) AS dept_budget,
    ROUND(SUM(actual_amount),0) AS dept_actual,
    ROUND(SUM(actual_amount) - SUM(budget_amount),0) AS dept_variance,
    ROUND((SUM(actual_amount) - SUM(budget_amount)) / SUM(budget_amount) * 100,2) AS dept_variance_pct
FROM budget_actuals
GROUP BY department
ORDER BY dept_variance DESC;  -- largest over-budget first



-- Q3: Account category variance frequency (how often categories exceed budget) --
	
WITH category_monthly AS (
    SELECT
        account_category,
        DATE_TRUNC('month', report_month) AS month,
        SUM(budget_amount) AS month_budget,
        SUM(actual_amount) AS month_actual,
        SUM(actual_amount) - SUM(budget_amount) AS month_variance
    FROM budget_actuals
    GROUP BY account_category, DATE_TRUNC('month', report_month)
)
SELECT
    account_category,
    COUNT(*) FILTER (WHERE month_variance > 0) AS months_over_budget,
    ROUND(SUM(month_variance)::numeric, 2) AS total_variance
FROM category_monthly
GROUP BY account_category
ORDER BY months_over_budget DESC, total_variance DESC;


-- Q4: Monthly variance trend with ranking (which month actual results are the closest to budget forecast - CTE + window function) --

WITH monthly_summary AS (
    SELECT
        DATE_TRUNC('month', report_month) AS month,
        SUM(budget_amount) AS total_budget,
        SUM(actual_amount) AS total_actual,
        SUM(actual_amount) - SUM(budget_amount) AS variance_amount,
        ROUND(ABS((SUM(actual_amount) - SUM(budget_amount)) / SUM(budget_amount) * 100),2) AS variance_percent
    FROM budget_actuals
    GROUP BY DATE_TRUNC('month', report_month)
)
SELECT
    month,
    total_budget,
    total_actual,
    variance_amount,
    variance_percent,
    RANK() OVER (ORDER BY variance_percent) AS closest_month_to_budget_rank
FROM monthly_summary
ORDER BY variance_percent;

