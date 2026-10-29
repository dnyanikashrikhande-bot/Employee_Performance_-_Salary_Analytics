import csv
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -----------------------------
# Output File Name
# -----------------------------
file_name = "Data_Analysis_Python_Pandas_Task.csv"

# -----------------------------
# Sample Data
# -----------------------------
department = ["IT", "HR", "Sales", "Finance", "Marketing"]
job_roles = ["Data Analyst", "Developer","HR Executive","Finance Manager","Accountant","Developer","Software Engineer","Recruiter",
             "CEO","HR Manager","Data Scientist"]
genders = ["Male", "Female"]
attrition = ["Yes","No"]

first_names = [
    "Amit", "Rahul", "Sneha", "Pooja", "Vikas",
    "Neha", "Rohit", "Anjali", "Sagar", "Priya",
    "Akash", "Kiran", "Meena", "Rakesh", "Komal",
    "Nitin", "Sachin", "Swati", "Deepak", "Riya",
    "Sachin", "Tejas", "Sailee", "Lakshya", "Roshni",
    "Karan", "Farhana", "Rubina", "Deepali", "Manasvi"
]

last_names = [
    "Sharma", "Patil", "Deshmukh", "Joshi", "Verma",
    "Singh", "Pawar", "Gupta", "Kulkarni", "Yadav",
    "Kapoor", "Bhatt", "Gupta", "Dube", "Johare",
    "Lokhande", "Shinde", "Wahi", "Kulkarni", "More"
]

header = [
    "Employee ID",
    "Employee Name",
    "Department",
    "Job Role",
    "Gender",
    "Age",
    "Experience Years",
    "Monthly Salary",
    "Performance Score",
    "Projects Completed",
    "Training Hours",
    "Joining Date",
    "Attrition"
   
]


with open(file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    start_date = datetime(2025, 1, 1)

    for i in range(1, 1001):
        employee_id = f"E{i:04}"
        employee_namee = random.choice(first_names) + " " + random.choice(last_names)
        department_name = random.choice(department)
        job_role = random.choice(job_roles)
        gender = random.choice(genders)
        age = random.randint(21, 60)
        experience_year = random.randint(1,9)
        performance_score = random.randint(1,10)
        project_completed = random.randint(1,10)
        training_hours=random.randint(10,120)
        monthly_salary=random.randrange(20000,150001,1000)
        joining_date = start_date + timedelta(days=random.randint(0,364))
        attritionn = random.choice(attrition)
        

        writer.writerow([
            employee_id,
            employee_namee,
            department_name,
            job_role,
            gender,
            age,
            experience_year,
            monthly_salary,
            performance_score,
            project_completed,
            training_hours,
            joining_date.strftime("%d-%m-%Y"),
            attritionn,
        ])

print("========================================")
print("Data_Analysis_Python_Pandas_Task.csv Created Successfully!")
print("Total Records : 1000")
print("========================================")



df=pd.read_csv("Data_Analysis_Python_Pandas_Task.csv")
print(df)

#Task.1(Data Loading and Inspection)
print("=====================First 10 records================")
print(df.head(10))
print("======================Last 5 records=====================")
print(df.tail(5))
print("==================Find the number of rows and columns===============")
print(df.shape)
print("=====================Display columns names and datatypes============")
print(df.dtypes)
print("====================Statistical Summmary using describe()===========")
print(df.describe())
print("=============Filling missing salary values with the departments median salary================")
data = df.groupby("Department")["Monthly Salary"].median()
print(data)
print(df.fillna(data))
#Task.2(Data Cleaning)
print("===========Identifying and remove duplicate records=================")
print(df.isnull())
print("=========Finding Missing Value in each Column=======================")
print(df.isna())
print("=============Correct inconsistent department names and extra spaces===========")
df["Department"] = df["Department"].str.strip()
df["Department"] = df["Department"].replace({
    "it": "IT",
    "It": "IT",
    "hr": "HR",
    "sales": "Sales",
    "finance": "Finance",
    "marketing": "Marketing"
})
print("=========Identify negative salaries and invalid performance scores===========")
print(df[df["Monthly Salary"] < 0])
df.loc[
    ~df["Performance Score"].between(1, 10),
    "Performance Score"
] = np.nan


#Task.3(Data Transformation)
print("===============Creating Annual Salary Column======================")
df["Annual_Salary"]=(df["Monthly Salary"]*12)
print(df)
print("===============Creating Experience level column=================")
df["Expreience_Level"]=(np.where(df["Experience Years"]<=2,"Fresher",
                                 np.where(df["Experience Years"]<=5,"Mid Level","senior")))
print(df)
print("===========Creating Performance Category Column=================")
df["Performance_Category"]=(np.where(df["Performance Score"]<=2,"low",
                                     np.where(df["Performance Score"]>=4,"mid level",
                                     np.where(df["Performance Score"]>=8,"high level","highest"))))
print(df)
print("===========Creating Salary Band Column=================")
df["Salary_Band"]=(np.where(df["Monthly Salary"]<=20000,"low",
                                     np.where(df["Monthly Salary"]>=40000,"Medium",
                                     np.where(df["Monthly Salary"]>=80000,"High","Highest"))))

#Task.4(Business Analysis)
print("=============Average Salary by Department==============")
data = df.groupby("Department")["Monthly Salary"].mean()
print(data)
print("===========Identifying Highest Paid Employee===========")
print(df.loc[df["Monthly Salary"].idxmax()])
print("===========Find top 10 Employees by performance=========")
data2 = df.groupby(["Employee Name","Employee ID"])["Performance Score"].max()
print(data2)
print(data2.head(10))
print("==========Calculate Average Salary by Job Role===========")
data3 = df.groupby("Job Role")["Monthly Salary"].mean()
print(data3)
print("=======Compare average experience across departments=======")
data4= df.groupby("Department")[ "Experience Years"].mean()
print(data4)
print("=============Calculate Employees Attrition percentage===============")
attrition_rate = (
    df["Attrition"].astype(str).str.strip().str.lower()
    .eq("yes").mean() * 100
)
print("Attrition percentage:", round(attrition_rate, 2), "%")
print("============Employees whose High salary but low performance=============")
print(df[
    (df["Monthly Salary"] > 60000) &
    (df["Performance Score"] < 5)
])
#Task.5 (Advanced pandas) 
print("==========Use Groupby to Summarize Department Performance==========")
data6 = df.groupby("Department")["Performance Score"].mean()
print(data6)
print("==========Use agg() to calculate multiple statistics===============")
print(df.groupby("Department").agg({
        "Monthly Salary": ["mean", "max", "min"],
        "Performance Score": "mean",
        "Employee ID": "count"
    })
)
print("===============Use sort_values() to rank employees================")
print(df.sort_values("Monthly Salary", ascending=False))
print("==============Use Loc[] and iloc[] to filter records==============")
print(df.loc[df["Monthly Salary"] > 50000])
print(df.iloc[0:5])
print("=============Use pivot_table() to compare salary and performance=========")
print(pd.pivot_table(
    df,
    index="Department",
    columns="Performance Score",
    values="Monthly Salary",
    aggfunc="mean"
))
print("================Use merge() to combine employee and department budget datasets=========")
budget = pd.DataFrame({
    "Department": ["IT", "HR", "Sales", "Finance", "Marketing"],
    "Department_Budget": [500000, 200000, 350000, 300000, 250000]
})

merged_df = pd.merge(df, budget, on="Department", how="left")
print(merged_df.head())
print("================Use apply()or vectorized operations to classify employees==============")
df["Employee_Status"] = df["Performance Score"].apply(
    lambda x: "Good" if pd.notna(x) and x >= 7 else "Needs Review"
)

print(df[["Employee Name", "Employee_Status"]].head())
#Task.6(Bussiness Deliverables)
df.to_excel("cleaned_Data_Analysis_Python_Pandas_Task.xlsx")
print(df)
print("Successfully load excel file")
print("===========Department summaries to a separate excel sheet========")
data7 = df.groupby("Department")["Monthly Salary"].sum()
print(data7)
data8 = df.groupby("Job Role")["Monthly Salary"].sum()
print(data8)








