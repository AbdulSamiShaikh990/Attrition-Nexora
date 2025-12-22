# Employee Attrition Prediction App

## Overview
This application helps predict **employee attrition risk** and provides **actionable insights**. Employee turnover (also known as "employee churn") is a costly problem for companies. The true cost of replacing an employee can often be quite large due to factors like:
- Time spent interviewing and finding a replacement
- Sign-on bonuses
- Loss of productivity during onboarding

By leveraging machine learning, this app helps **identify employees at risk** and **provides recommendations** to improve retention.

## Features
- **Upload Data**: Provide your employee dataset in CSV format
- **Model Evaluation**: Review model performance metrics such as accuracy, F1-score, and AUC-ROC
- **Feature Analysis**: Understand key attrition drivers through feature importance visualization
- **Risk Categorization**: Employees are classified into **Low**, **Medium**, or **High** attrition risk groups
- **Actionable Recommendations**: Based on key factors like job satisfaction, monthly income, and work-life balance

## Getting Started Guide

To run this project locally, follow these steps:

### 1️⃣ Clone the Repository

First, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/yourusername/employee-attrition-app.git
cd employee-attrition-app
```

### 2️⃣ Install Dependencies

Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

Start the Streamlit app by running:

```bash
streamlit run app.py
```

This will launch the app in your default web browser.

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn

## Notes

- Ensure your dataset contains the required features before uploading.
- The model and scaler files (`rf_best.pkl` and `scaler.pkl`) should be placed in the project directory.

## **Generating Random Employee Data**
This project includes a **random employee data generator** that creates a synthetic dataset of **1,000 employees** with relevant features for attrition prediction.

### **Generate the CSV File**
Run the following script to generate `random_employee_data_1000.csv`:

```python
import csv
import random

# Define the headers for the CSV file
headers = [
    'Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EmployeeNumber',
    'EnvironmentSatisfaction', 'JobInvolvement', 'JobLevel', 'JobSatisfaction',
    'MonthlyIncome', 'OverTime', 'StockOptionLevel', 'TotalWorkingYears',
    'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany',
    'YearsInCurrentRole', 'YearsWithCurrManager', 'BusinessTravel_Travel_Frequently',
    'BusinessTravel_Travel_Rarely', 'MaritalStatus_Married', 'MaritalStatus_Single'
]

# Function to generate a random employee data row
def generate_random_row(employee_number):
    age = random.randint(20, 65)  # Age between 20 and 65
    daily_rate = random.randint(200, 2000)  # DailyRate within a reasonable range
    monthly_income = daily_rate * 22  # MonthlyIncome approximated as DailyRate * 22
    distance_from_home = random.randint(1, 30)  # DistanceFromHome within 30 km
    education = random.randint(1, 5)  # Education level (1 to 5 scale)
    environment_satisfaction = random.randint(1, 4)  # EnvironmentSatisfaction (1 to 4 scale)
    job_involvement = random.randint(1, 4)  # JobInvolvement (1 to 4 scale)
    job_level = random.randint(1, 5)  # JobLevel (1 to 5 scale)
    job_satisfaction = random.randint(1, 4)  # JobSatisfaction (1 to 4 scale)
    over_time = random.choice([True, False])  # OverTime (Boolean: Yes/No)
    stock_option_level = random.randint(0, 3)  # StockOptionLevel (0 to 3 scale)
    total_working_years = random.randint(0, age - 18)  # TotalWorkingYears ensuring logic with Age
    years_at_company = random.randint(0, total_working_years)  # Years at company should not exceed TotalWorkingYears
    years_in_current_role = random.randint(0, years_at_company)  # Should not exceed YearsAtCompany
    years_with_curr_manager = random.randint(0, years_in_current_role)  # Should not exceed YearsInCurrentRole
    training_times_last_year = random.randint(0, 6)  # TrainingTimesLastYear (0 to 6 sessions)
    work_life_balance = random.randint(1, 4)  # WorkLifeBalance (1 to 4 scale)
    
    # Business Travel (only one can be True)
    business_travel_options = ["Frequent", "Rare"]
    business_travel_choice = random.choice(business_travel_options)
    business_travel_freq = business_travel_choice == "Frequent"
    business_travel_rare = business_travel_choice == "Rare"
    
    # Marital Status (only one can be True)
    marital_status_options = ["Married", "Single"]
    marital_status_choice = random.choice(marital_status_options)
    marital_status_married = marital_status_choice == "Married"
    marital_status_single = marital_status_choice == "Single"
    
    return [
        age, daily_rate, distance_from_home, education, employee_number,
        environment_satisfaction, job_involvement, job_level, job_satisfaction,
        monthly_income, over_time, stock_option_level, total_working_years,
        training_times_last_year, work_life_balance, years_at_company,
        years_in_current_role, years_with_curr_manager, business_travel_freq,
        business_travel_rare, marital_status_married, marital_status_single
    ]

# Generate employee data for 1000 employees
data = [headers] + [generate_random_row(i) for i in range(1, 1001)]

# Write generated data to a CSV file
with open("random_employee_data_1000.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV file 'random_employee_data_1000.csv' created successfully!")
```

This will create a **synthetic dataset** to test the app without needing real employee data.

---

## License
This project is licensed under the **MIT License**. You are free to modify and use it for commercial and non-commercial purposes.

## Contributing

Feel free to submit pull requests or report issues to improve this project.

---

For any issues or questions, reach out via GitHub or email.

📧 [Reach out on LinkedIn](https://www.linkedin.com/in/joaorussofigueiredo/)

🔗 [JohnRusso Repo](https://github.com/j0hnrusso)

