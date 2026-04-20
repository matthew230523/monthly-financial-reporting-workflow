    # 📊 Monthly Financial Reporting Workflow

    ## 📚 Table of Contents
    - [Project Overview](#-project-overview)
    - [Features](#-feautures)
    - [Tech Stack](#-tech-stack)
    - [Project Structure](#-project-structure)
    - [Business Case](#-business-case)
    - [Workflow](#-workflow-overview)
    - [How to Run](#-how-to-run-the-project)                                                                                                           -
    - [Requirements](#-requirements)
    - [Output](#-output)    
    - [Notes](#-notes)
    - [Author](#-author)

---



    ## 📌 Project Overview
    This project demonstrates an end-to-end financial reporting workflow using SQL and Python.

    It simulates a real-world business scenario where financial data is processed, analyzed, and transformed into a structured Excel report for decision-making.

    The workflow covers:
    - Data generation (synthetic dataset using Python)
    - Data storage in PostgreSQL
    - Financial analysis (variance, trends, performance)
    - Automated Excel report generation

    ---


    ## ✨ Features

    - End-to-end financial reporting workflow (Python + SQL)
    - Budget vs Actual variance analysis
    - Quarterly and monthly performance tracking
    - Department-level analysis
    - Net result (profitability) calculation
    - Automated Excel report generation

    ## ⚙️ Tech Stack
    - Python (pandas, sqlalchemy, openpyxl)
    - PostgreSQL
    - SQL

    ---

    ## 📂 Project Structure

    monthly-financial-reporting-workflow/
    │
    ├── README.md
    ├── requirements.txt
    │
    ├── 01_data/
    │ └── budget_actuals.csv
    │
    ├── 02_sql/
    │ ├── 01_create_table.sql
    │ ├── 02_load_data.sql
    │ └── 03_business_questions.sql
    │
    ├── 03_python/
    │ ├── 00_generate_sample_data.py
    │ ├── 01_load_csv_to_postgresql.py
    │ ├── 02_financial_analysis.py
    │ └── 03_export_excel_report.py
    │
    ├── 04_output/
    │ └── monthly_financial_report.xlsx


    ---

    ## 📊 Business Case
    The objective of this project is to replicate a typical financial reporting process used in companies.

    The generated report provides insights such as:
    - Budget vs Actual performance
    - Variance analysis (absolute and percentage)
    - Quarterly financial summaries
    - Department-level performance evaluation
    - Net financial results (profitability view)
    - Monthly trends and category breakdowns

    This type of reporting supports management in monitoring performance and making data-driven decisions.

    ---

    ## 🔄 Workflow Overview

    1. **Data Generation**
    - Synthetic financial dataset is created using Python

    2. **Data Storage**
    - Data is loaded into PostgreSQL using SQL scripts

    3. **Data Analysis**
    - Python is used to calculate:
        - Variances
        - Aggregations
        - Performance metrics

    4. **Report Generation**
    - A structured Excel report is generated with multiple sheets

    ---

    ## 🚀 How to Run the Project

    1. Ensure PostgreSQL is installed and running  
    2. Update database connection details in Python scripts  

    3. Run the scripts in order:

    ```bash
    python 03_python/00_generate_sample_data.py
    python 03_python/01_load_csv_to_postgresql.py
    python 03_python/02_financial_analysis.py
    python 03_python/03_export_business_report.py 
    ```

    The final report will be saved in:
    04_output/monthly_financial_report.xlsx

    📦 Requirements

    Install dependencies using:

    pip install -r requirements.txt


    📈 Output

    The generated Excel report includes:

    Summary KPIs
    Quarterly variance analysis
    Department performance
    Net financial results
    Monthly trends
    Category analysis
    Full dataset view

    🔒 Notes
    Database credentials are not included for security reasons
    Replace the connection string with your own PostgreSQL credentials

    👤 Author

    Mateusz Cyruk


    ---