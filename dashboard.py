import matplotlib
matplotlib.use("Agg")   # Prevent Streamlit blank screen issue

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =====================================================
# LOAD DATA
# =====================================================
df = pd.read_csv("Students_grade.csv")

subject_cols = ["Math", "Science", "English", "History", "Computer"]
df["Average"] = df[subject_cols].mean(axis=1)


# Add grade function
def grade(x):
    if x >= 90: return "A"
    elif x >= 80: return "B"
    elif x >= 70: return "C"
    elif x >= 60: return "D"
    else: return "F"

df["Grade"] = df["Average"].apply(grade)


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Overview",
        "📘 Subject Insights",
        "🏅 Top Performers",
        "🍎 Grade Analysis",
        "📂 Student Profile",
        "🔍 Compare Two Students",
        "🔎 Compare Multiple Students",
        "📥 Download CSV"
    ]
)


# =====================================================
# PAGE 1: OVERVIEW
# =====================================================
if page == "🏠 Overview":
    st.title("📊 Student Performance Analyzer Dashboard")
    st.write("Analyze class performance, subject trends, grades, and top performers.")

    class_avg = round(df["Average"].mean(), 2)
    top_student = df.loc[df["Average"].idxmax()]
    low_student = df.loc[df["Average"].idxmin()]

    col1, col2, col3 = st.columns(3)

    col1.metric("📘 Class Average", class_avg)
    col2.metric("🏆 Top Student", f"{top_student['Name']} ({round(top_student['Average'],1)})")
    col3.metric("⚠️ Lowest Student", f"{low_student['Name']} ({round(low_student['Average'],1)})")

    # Subject-wise averages chart
    st.subheader("📊 Subject-wise Average Scores")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(subject_cols, df[subject_cols].mean(), color="skyblue", edgecolor="black")
    ax.set_ylabel("Score")
    ax.set_title("Average Score per Subject")
    st.pyplot(fig)



# =====================================================
# PAGE 2: SUBJECT INSIGHTS
# =====================================================
if page == "📘 Subject Insights":
    st.title("📘 Subject Insights")

    st.write("Average, highest and lowest scores for each subject.")
    stats_df = pd.DataFrame({
        "Subject": subject_cols,
        "Average": [df[s].mean() for s in subject_cols],
        "Highest": [df[s].max() for s in subject_cols],
        "Lowest": [df[s].min() for s in subject_cols],
    })

    st.dataframe(stats_df)

    # Chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(subject_cols, stats_df["Highest"], marker="o", label="Highest", color="green")
    ax.plot(subject_cols, stats_df["Lowest"], marker="o", label="Lowest", color="red")
    ax.plot(subject_cols, stats_df["Average"], marker="o", label="Average", color="blue")
    ax.legend()
    ax.set_title("Subject Score Trends")
    st.pyplot(fig)



# =====================================================
# PAGE 3: TOP PERFORMERS
# =====================================================
if page == "🏅 Top Performers":
    st.title("🏅 Top 10 Students")

    top10 = df.sort_values("Average", ascending=False).head(10)
    st.dataframe(top10[["Name", "Average", "Grade"]])

    # Chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(top10["Name"], top10["Average"], color="purple")
    plt.xticks(rotation=45)
    ax.set_ylabel("Average Score")
    ax.set_title("Top 10 Students")
    st.pyplot(fig)



# =====================================================
# PAGE 4: GRADE ANALYSIS
# =====================================================
if page == "🍎 Grade Analysis":
    st.title("🍎 Grade Distribution")

    grade_counts = df["Grade"].value_counts()

    st.dataframe(grade_counts)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(grade_counts, labels=grade_counts.index, autopct="%1.1f%%", startangle=140)
    ax.set_title("Grade Distribution Pie Chart")
    st.pyplot(fig)



# =====================================================
# PAGE 5: STUDENT PROFILE VIEW
# =====================================================
if page == "📂 Student Profile":
    st.title("📂 Student Profile")

    student = st.selectbox("Select a student:", df["Name"].unique())

    s = df[df["Name"] == student].iloc[0]

    st.subheader(f"📘 Report Card — {student}")
    st.write(f"**Average Score:** {round(s['Average'],1)}")
    st.write(f"**Grade:** {s['Grade']}")

    # Subject chart
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(subject_cols, s[subject_cols], color="teal")
    ax.set_title(f"{student}'s Subject-wise Performance")
    st.pyplot(fig)



# =====================================================
# PAGE 6: COMPARE TWO STUDENTS
# =====================================================
if page == "🔍 Compare Two Students":
    st.title("🔍 Compare Two Students")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Student 1")
        s1 = st.selectbox("Select Student 1", df["Name"].unique())

    with col2:
        st.header("Student 2")
        s2 = st.selectbox("Select Student 2", df["Name"].unique())

    df1 = df[df["Name"] == s1].iloc[0]
    df2 = df[df["Name"] == s2].iloc[0]

    st.subheader("📊 Comparison Table")
    comparison = pd.DataFrame({
        "Subject": subject_cols,
        s1: df1[subject_cols].values,
        s2: df2[subject_cols].values
    })

    st.dataframe(comparison)

    # Comparison chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(subject_cols, df1[subject_cols], marker="o", label=s1)
    ax.plot(subject_cols, df2[subject_cols], marker="o", label=s2)
    ax.legend()
    ax.set_title("Performance Comparison")
    st.pyplot(fig)



# =====================================================
# PAGE 7: COMPARE MULTIPLE STUDENTS
# =====================================================
if page == "🔎 Compare Multiple Students":
    st.title("🔎 Compare Multiple Students")

    selected = st.multiselect("Select Students", df["Name"].unique())

    if len(selected) >= 1:
        multi_df = df[df["Name"].isin(selected)]

        st.subheader("📘 Comparison Table")
        st.dataframe(multi_df[["Name"] + subject_cols + ["Average", "Grade"]])

        fig, ax = plt.subplots(figsize=(10, 4))
        for _, row in multi_df.iterrows():
            ax.plot(subject_cols, row[subject_cols], marker="o", label=row["Name"])
        ax.legend()
        ax.set_title("Multi-student Performance Comparison")
        st.pyplot(fig)
    else:
        st.warning("Please select at least one student.")



# =====================================================
# PAGE 8: DOWNLOAD CSV
# =====================================================
if page == "📥 Download CSV":
    st.title("📥 Download Processed CSV")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Processed Data", csv, "processed_students.csv")
