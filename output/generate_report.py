
import os
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(
    BASE_DIR, "output", "results", "cleaned_student_data.csv"
)

RESULTS_DIR = os.path.join(BASE_DIR, "output", "results")

PDF_PATH = os.path.join(
    RESULTS_DIR, "Data_Cleaning_Project_Report.pdf"
)

# Load cleaned dataset
df = pd.read_csv(DATASET_PATH)

# Report setup
doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    textColor=colors.darkblue,
    fontSize=22,
    alignment=1,
    spaceAfter=20
)

# Title
story.append(Spacer(1, 1.5 * inch))
story.append(Paragraph(
    "DATA CLEANING AND VISUALIZATION",
    title_style
))
story.append(Paragraph(
    "Using Python Programming",
    styles["Heading2"]
))
story.append(Spacer(1, 0.5 * inch))

story.append(Paragraph(
    "Project Report",
    styles["Heading1"]
))
story.append(Spacer(1, 2 * inch))

story.append(Paragraph(
    "Dataset: Student Placement Dataset",
    styles["Normal"]
))
story.append(Paragraph(
    "Tools: Python, Pandas, NumPy, Matplotlib, Seaborn",
    styles["Normal"]
))

story.append(PageBreak())

# Introduction
story.append(Paragraph("1. Introduction", styles["Heading1"]))
story.append(Paragraph(
    "This project focuses on cleaning and analyzing a student "
    "placement dataset using Python. The dataset contains academic "
    "performance, technical skills, personal development and "
    "placement information.",
    styles["BodyText"]
))
story.append(Spacer(1, 12))

# Objectives
story.append(Paragraph("2. Project Objectives", styles["Heading1"]))
objectives = [
    "Understand the structure of the dataset.",
    "Identify missing values and duplicate records.",
    "Analyze potential outliers using the IQR method.",
    "Validate data ranges and clean text columns.",
    "Visualize student performance and placement information.",
    "Analyze relationships between numerical features.",
    "Export the cleaned dataset."
]

for item in objectives:
    story.append(Paragraph("• " + item, styles["BodyText"]))

story.append(Spacer(1, 12))

# Dataset information
story.append(Paragraph("3. Dataset Description", styles["Heading1"]))

dataset_info = [
    ["Description", "Value"],
    ["Total Records", str(df.shape[0])],
    ["Total Columns", str(df.shape[1])],
    ["Missing Values", str(df.isnull().sum().sum())],
    ["Duplicate Records", str(df.duplicated().sum())]
]

table = Table(dataset_info, colWidths=[220, 180])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("PADDING", (0, 0), (-1, -1), 8)
]))

story.append(table)
story.append(Spacer(1, 12))

# Cleaning methods
story.append(Paragraph("4. Data Cleaning Process", styles["Heading1"]))
story.append(Paragraph(
    "The dataset was inspected for missing values and duplicate "
    "records. Text columns were stripped of unnecessary leading "
    "and trailing spaces. Data validation and IQR-based outlier "
    "analysis were also performed. Potential outliers were reviewed "
    "rather than automatically deleted.",
    styles["BodyText"]
))
story.append(Spacer(1, 12))

# Visualizations
story.append(Paragraph("5. Data Visualizations", styles["Heading1"]))

graphs = [
    ("CGPA Distribution", "cgpa_distribution.png"),
    ("Placement Status", "placement_status.png"),
    ("Branch-wise Placement", "branch_placement.png"),
    ("Salary Distribution", "salary_distribution.png"),
    ("Correlation Heatmap", "correlation_heatmap.png")
]

for graph_title, filename in graphs:
    graph_path = os.path.join(RESULTS_DIR, filename)

    if os.path.exists(graph_path):
        story.append(Paragraph(graph_title, styles["Heading2"]))
        img = Image(graph_path, width=6 * inch, height=3.3 * inch)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 12))
    else:
        story.append(Paragraph(
            "Graph not found: " + filename,
            styles["BodyText"]
        ))

# Conclusion
story.append(Paragraph("6. Conclusion", styles["Heading1"]))
story.append(Paragraph(
    "This project demonstrated how Python libraries can be used "
    "to inspect, clean, validate and visualize a student placement "
    "dataset. The cleaned dataset and visualizations provide a "
    "useful foundation for further analysis and understanding "
    "of student placement patterns.",
    styles["BodyText"]
))

# Generate PDF
doc.build(story)

print("Project report generated successfully!")
print("PDF Location:", PDF_PATH)
