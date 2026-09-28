import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("Students_grade.csv")

# all subject columns
subject_cols = ["Math", "Science", "English", "History", "Computer"]

# ---------------------------------------------------
# 2. CALCULATE STUDENT AVERAGE & GRADE
# ---------------------------------------------------
df["Average"] = df[subject_cols].mean(axis=1)

def grade(x):
    if x >= 90: return "A"
    elif x >= 80: return "B"
    elif x >= 70: return "C"
    elif x >= 60: return "D"
    else: return "F"

df["Grade"] = df["Average"].apply(grade)

# ---------------------------------------------------
# 3. CALCULATE SUBJECT INSIGHTS
# ---------------------------------------------------
subject_averages = df[subject_cols].mean()
subject_highest = df[subject_cols].max()
subject_lowest = df[subject_cols].min()

# ---------------------------------------------------
# 4. CLASS INSIGHTS
# ---------------------------------------------------
class_average = round(df["Average"].mean(), 2)
top_student = df.loc[df["Average"].idxmax()]
lowest_student = df.loc[df["Average"].idxmin()]
grade_distribution = df["Grade"].value_counts()

# ---------------------------------------------------
# 5. PRINT THE RESULTS
# ---------------------------------------------------
print("\n========== STUDENT ANALYSIS REPORT ==========\n")

print("▶ SUBJECT-WISE AVERAGES:")
print(subject_averages)

print("\n▶ HIGHEST SCORE PER SUBJECT:")
print(subject_highest)

print("\n▶ LOWEST SCORE PER SUBJECT:")
print(subject_lowest)

print("\n▶ CLASS AVERAGE:", class_average)

print("\n▶ TOP STUDENT:")
print(top_student[["Name", "Average", "Grade"]])

print("\n▶ LOWEST STUDENT:")
print(lowest_student[["Name", "Average", "Grade"]])

print("\n▶ GRADE DISTRIBUTION:")
print(grade_distribution)

print("\n▶ FINAL DATA TABLE:")
print(df[["Name", "Average", "Grade"]])

# ---------------------------------------------------
# 6. GENERATE CHARTS & SAVE IMAGES
# ---------------------------------------------------

# ------ Chart 1: Subject-wise Average Scores ------
plt.figure(figsize=(8, 5))
plt.bar(subject_cols, subject_averages, color="skyblue")
plt.title("Subject-wise Average Scores")
plt.xlabel("Subjects")
plt.ylabel("Average Score")
plt.tight_layout()
plt.savefig("subject_average_scores.png")
plt.close()

# ------ Chart 2: Highest & Lowest Scores per Subject ------
plt.figure(figsize=(10, 5))
x = range(len(subject_cols))
plt.bar(x, subject_highest, width=0.4, label="Highest", color="green")
plt.bar([i + 0.4 for i in x], subject_lowest, width=0.4, label="Lowest", color="red")
plt.xticks([i + 0.2 for i in x], subject_cols)
plt.title("Highest & Lowest Scores Per Subject")
plt.legend()
plt.tight_layout()
plt.savefig("subject_highest_lowest_scores.png")
plt.close()

# ------ Chart 3: Top 10 Students ------
top10 = df.nlargest(10, "Average")
plt.figure(figsize=(10, 5))
plt.bar(top10["Name"], top10["Average"], color="purple")
plt.xticks(rotation=45)
plt.title("Top 10 Students by Average Score")
plt.xlabel("Students")
plt.ylabel("Average Score")
plt.tight_layout()
plt.savefig("top10_students.png")
plt.close()

# ------ Chart 4: Grade Distribution Pie Chart ------
plt.figure(figsize=(6, 6))
plt.pie(grade_distribution, labels=grade_distribution.index, autopct="%1.1f%%", startangle=140)
plt.title("Grade Distribution")
plt.savefig("grade_distribution_pie.png")
plt.close()

# ------ Chart 5: Histogram of Average Scores ------
plt.figure(figsize=(8, 5))
plt.hist(df["Average"], bins=10, color="orange", edgecolor="black")
plt.title("Distribution of Student Average Scores")
plt.xlabel("Average Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("average_score_distribution.png")
plt.close()

print("\nImages generated:")
print(" - subject_average_scores.png")
print(" - subject_highest_lowest_scores.png")
print(" - top10_students.png")
print(" - grade_distribution_pie.png")
print(" - average_score_distribution.png")

print("\n🎉 DONE! All analysis and charts saved successfully.")


# =========================
# Chart 6: Top 3 Students in Each Subject (Combined Chart)
# =========================

subjects = ["Math", "Science", "English", "History", "Computer"]

plt.figure(figsize=(15, 20))
plt.suptitle("Top 3 Students in Each Subject", fontsize=20)

for i, subj in enumerate(subjects):
    plt.subplot(5, 1, i+1)

    top3 = df.sort_values(by=subj, ascending=False).head(3)

    plt.bar(top3["Name"], top3[subj], color="skyblue", edgecolor="black")
    plt.title(f"Top 3 in {subj}", fontsize=14)
    plt.ylabel("Score")
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("top3_subjects.png")
plt.close()

