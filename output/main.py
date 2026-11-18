import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Get project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset path
dataset_path = os.path.join(
    BASE_DIR, "dataset", "student.csv"
)

# Create output folder
output_path = os.path.join(BASE_DIR, "output", "results")
os.makedirs(output_path, exist_ok=True)

# Load dataset
df = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")

print(df.head())





print("\n========== DATASET INFORMATION ==========")

# Dataset shape
print("Dataset Shape:", df.shape)

# Column names
print("\nColumn Names:")
print(df.columns.tolist())

# Data types
print("\nData Types:")
print(df.dtypes)

# Dataset information
print("\nDataset Information:")
df.info()

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())






print("\n========== DATA QUALITY CHECK ==========")

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Total missing values
print("\nTotal Missing Values:", df.isnull().sum().sum())

# Duplicate records
print("\nDuplicate Records:", df.duplicated().sum())





#step 2

print("\n========== OUTLIER DETECTION ==========")

# Select numerical columns
numeric_columns = df.select_dtypes(
    include=np.number
).columns

# Exclude student_id because it is an identifier
numeric_columns = numeric_columns.drop("student_id")

outlier_results = []

for col in numeric_columns:

    # Calculate Q1 and Q3
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    # Calculate IQR
    IQR = Q3 - Q1

    # Calculate limits
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = df[
        (df[col] < lower_limit) |
        (df[col] > upper_limit)
    ]

    outlier_count = len(outliers)

    # Store results
    outlier_results.append({
        "Column": col,
        "Lower Limit": lower_limit,
        "Upper Limit": upper_limit,
        "Outlier Count": outlier_count
    })

    print(f"{col}: {outlier_count} outliers")

# Convert results into DataFrame
outlier_df = pd.DataFrame(outlier_results)

print("\n========== OUTLIER SUMMARY ==========")

print(outlier_df.to_string(index=False))

# Save outlier report
outlier_df.to_csv(
    os.path.join(output_path, "outlier_report.csv"),
    index=False
)

print("\nOutlier report saved successfully!")




#step 3

print("\n========== OUTLIER VISUALIZATION ==========")

# Columns selected for outlier analysis
selected_columns = [
    "cgpa",
    "internships_count",
    "projects_count",
    "github_repos",
    "backlogs",
    "study_hours_per_day",
    "attendance_percentage",
    "salary_package_lpa"
]

for col in selected_columns:

    plt.figure(figsize=(8, 4))

    sns.boxplot(x=df[col])

    plt.title(f"Outlier Analysis - {col}")
    plt.xlabel(col)

    plt.tight_layout()

    plt.savefig(
        os.path.join(output_path, f"{col}_boxplot.png"),
        dpi=300
    )

    plt.show()

print("Box plots generated successfully!")





#step 4






print("\n========== DATA VALIDATION ==========")

# Check logically invalid values

checks = {
    "Age below 18 or above 100":
        (df["age"] < 18) | (df["age"] > 100),

    "CGPA outside 0-10":
        (df["cgpa"] < 0) | (df["cgpa"] > 10),

    "Attendance outside 0-100":
        (df["attendance_percentage"] < 0) |
        (df["attendance_percentage"] > 100),

    "Study hours outside 0-24":
        (df["study_hours_per_day"] < 0) |
        (df["study_hours_per_day"] > 24),

    "Sleep hours outside 0-24":
        (df["sleep_hours"] < 0) |
        (df["sleep_hours"] > 24),

    "Negative salary":
        df["salary_package_lpa"] < 0
}

for name, condition in checks.items():

    print(name, ":", condition.sum())

print("\nData validation completed!")



#step 5




plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="cgpa",
    bins=30,
    kde=True
)

plt.title("Distribution of Student CGPA")

plt.xlabel("CGPA")
plt.ylabel("Number of Students")

plt.tight_layout()

plt.savefig(
    os.path.join(output_path, "cgpa_distribution.png"),
    dpi=300
)

plt.show()


# Placement status analysis

plt.figure(figsize=(8, 5))

sns.countplot(data=df, x="placement_status")

plt.title("Student Placement Status")
plt.xlabel("Placement Status")
plt.ylabel("Number of Students")

plt.tight_layout()

plt.savefig(
    os.path.join(output_path, "placement_status.png"),
    dpi=300
)


# Branch-wise Placement Rate

branch_placement = pd.crosstab(
    df["branch"],
    df["placement_status"],
    normalize="index"
) * 100

branch_placement.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Branch-wise Placement Rate")
plt.xlabel("Branch")
plt.ylabel("Placement Percentage")
plt.xticks(rotation=45)
plt.legend(title="Placement Status")

plt.tight_layout()
plt.savefig(os.path.join(output_path, "branch_placement.png"), dpi=300)
plt.show()



# Salary Analysis of Placed Students

placed_df = df[
    df["placement_status"].str.strip().str.lower() == "placed"
]

plt.figure(figsize=(10, 5))

sns.histplot(
    data=placed_df,
    x="salary_package_lpa",
    bins=30,
    kde=True
)

plt.title("Salary Package Distribution")
plt.xlabel("Salary Package (LPA)")
plt.ylabel("Number of Students")

plt.tight_layout()
plt.savefig(os.path.join(output_path, "salary_distribution.png"), dpi=300)
plt.show()




print("\nPLACEMENT SUMMARY")

print("Total Students:", len(df))
print("Placed Students:", len(placed_df))
print("Not Placed Students:", len(df) - len(placed_df))

print("Placement Percentage:",
      round((len(placed_df) / len(df)) * 100, 2), "%")

print("Average Salary:",
      round(placed_df["salary_package_lpa"].mean(), 2), "LPA")

print("\nBranch-wise Average Salary:")
print(placed_df.groupby("branch")["salary_package_lpa"].mean().round(2))




# Step 7: Correlation Analysis

# Select numerical columns
numeric_df = df.select_dtypes(include=np.number)

# Remove student_id because it is only an ID
numeric_df = numeric_df.drop(columns=["student_id"])

# Calculate correlation
correlation = numeric_df.corr()

# Create heatmap
plt.figure(figsize=(16, 10))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Correlation Between Student Features")

plt.tight_layout()
plt.savefig(
    os.path.join(output_path, "correlation_heatmap.png"),
    dpi=300
)

plt.show()




# Correlation with salary among placed students

placed_df = df[
    df["placement_status"].str.strip().str.lower() == "placed"
]

salary_correlation = (
    placed_df.select_dtypes(include=np.number)
    .drop(columns=["student_id", "salary_package_lpa"])
    .corrwith(placed_df["salary_package_lpa"])
    .sort_values(ascending=False)
)

print("\nFactors Related to Salary:")
print(salary_correlation.round(3))




print("\nTop 5 Factors Related to Salary:")
print(salary_correlation.head(5).round(3))



# Step 8: Final Data Cleaning

cleaned_df = df.copy()

print("Original Dataset Shape:", df.shape)



cleaned_df = cleaned_df.drop_duplicates()

print("After Removing Duplicates:", cleaned_df.shape)



# Clean text columns

text_columns = cleaned_df.select_dtypes(include="object").columns

for col in text_columns:
    cleaned_df[col] = cleaned_df[col].str.strip()

print("Text columns cleaned successfully!")


print("\nMissing Values After Cleaning:")
print(cleaned_df.isnull().sum().sum())





cleaned_file = os.path.join(output_path, "cleaned_student_data.csv")

cleaned_df.to_csv(cleaned_file, index=False)

print("\nCleaned Dataset Saved Successfully!")
print("File Location:", cleaned_file)