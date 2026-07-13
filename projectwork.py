import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Diabetes analysis",page_icon=":notebook:",layout="wide")
st.title("🩺 Diabetes Analytic System")
st.text("Smart Data visualization for Patient's Health")

df=pd.read_csv("Dataset of Diabetes .csv")
with st.sidebar:
    st.title(" 📁 Navigator")
    from streamlit_option_menu import option_menu
    opt=option_menu("Control Deck",["📑 Preface","🤖 Upload & Preview","💡Cleaning & Processing","📈 Graphs and charts","🔎 Insights","✏️ About"])    
if  opt=="📑 Preface":
   total_patients = len(df)
   avg_age = df["AGE"].mean() if "AGE" in df.columns else 0
   avg_bmi = df["BMI"].mean() if "BMI" in df.columns else 0
   avg_hba1c = df["HbA1c"].mean() if "HbA1c" in df.columns else 0
   avg_chol = df["Chol"].mean() if "Chol" in df.columns else 0

   col1, col2, col3, col4, col5 = st.columns(5)

   col1.metric("👥 Total Patients", f"{total_patients}")
   col2.metric("🎂 Avg Age", f"{avg_age:.1f}")
   col3.metric("⚖️ Avg BMI", f"{avg_bmi:.1f}")
   col4.metric("🩸 Avg HbA1c", f"{avg_hba1c:.2f}")
   col5.metric("🧪 Avg Cholesterol", f"{avg_chol:.2f}")

   st.markdown("---") 

      
   import seaborn as sns
   import matplotlib.pyplot as plt

   st.text("👥 Patients with Diabetes by Age")

   diabetes_df = df[df["CLASS"] == "Y"]
   age_bins = [20, 30, 40, 50, 60, 70, 80]   
   age_labels = ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79"]

   diabetes_df["AgeGroup"] = pd.cut(diabetes_df["AGE"], bins=age_bins, labels=age_labels,right=False)

   fig, ax = plt.subplots(figsize=(8,4))
   plt.xticks(rotation=45)
  
   sns.histplot(df[df['CLASS']=='Y']['AGE'], bins=[20,30,40,50,60,70,80], color='green')

   plt.title("Number of Diabetic Patients by Age")
   st.pyplot(fig)
  
elif opt=="🤖 Upload & Preview":

  t1,t2,t3=st.tabs(["Data set","Data info","Data summary"])
  with t1:
     uploaded_file = st.file_uploader("📂 Upload your Diabetes Dataset (.xlsx or .csv)", type=["xlsx", "csv"])

     if uploaded_file:
      df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
      st.success("✅ Dataset uploaded successfully!")

     else:
      st.warning("Please upload your dataset to begin analysis.")

     st.subheader(" 📌 Patients records")
     st.dataframe(df)
  with t2:
     st.subheader("📜 Data Quality Check")

     dq1, dq2, dq3 = st.columns(3)

     dq1.metric("Missing Values", int(df.isna().sum().sum()))
     dq2.metric("Duplicate Rows", int(df.duplicated().sum()))
     dq3.metric("Columns", df.shape[1])

     st.dataframe(df.isna().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Values"}))
  with t3:
       st.subheader("📝 Data summary")
       st.write(f"**Total Records:** {df.shape[0]}")
       st.write(f"**Columns:** {df.shape[1]}")
       st.write("**Classes:** N = Normal, P = Prediabetes, Y = Diabetes")
       st.write(f"**Age Range:** {df['AGE'].min()} – {df['AGE'].max()} years")
       st.write(f"**Average BMI:** {round(df['BMI'].mean(),2)}")
       st.write(f"**Average HbA1c:** {round(df['HbA1c'].mean(),2)}")
       st.write(f"**Average HDL:** {round(df['HDL'].mean(),2)}")
       st.write(f"**Average Chol:** {round(df['Chol'].mean(),2)}")

elif opt == "📈 Graphs and charts":
    import seaborn as sns
    import matplotlib.pyplot as plt 
    t1,t2,t3,t4=st.tabs(["Pie chart & Bar graph","Histogram","Boxplot & Scatter","Heatmap"])
    st.sidebar.header("🔎 Filter Patients")

    gender_options = sorted(df["Gender"].dropna().unique().tolist()) if "Gender" in df.columns else []
    class_options = sorted(df["CLASS"].dropna().unique().tolist()) if "CLASS" in df.columns else []

    selected_gender = st.sidebar.multiselect("Select Gender", gender_options, default=gender_options)
    selected_class = st.sidebar.multiselect("Select Class", class_options, default=class_options)

    min_age = int(df["AGE"].min()) if "AGE" in df.columns else 0
    max_age = int(df["AGE"].max()) if "AGE" in df.columns else 100

    age_range = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))

    df = df.copy()

    if "Gender" in df.columns:
        df = df[df["Gender"].isin(selected_gender)]

    if "CLASS" in df.columns:
        df = df[df["CLASS"].isin(selected_class)]

    if "AGE" in df.columns:
        df = df[(df["AGE"] >= age_range[0]) &(df["AGE"] <= age_range[1])]

        class_map = { "N": "Normal", "P": "Prediabetes", "Y": "Diabetes"}

    if "CLASS" in df.columns:
        df["Class Label"] = df["CLASS"].map(class_map).fillna(df["CLASS"])
    else:
        df["Class Label"] = "Unknown"
    with t1:
     
      st.subheader("Class Distribution")
      if "Class Label" in df.columns:
            class_counts = df["Class Label"].value_counts().reset_index()
            class_counts.columns = ["Class", "Count"]
            fig_class = px.pie(class_counts, names="Class", values="Count",hole=0.45, color="Class", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_class, use_container_width=True)

    
            st.subheader("Gender Distribution")
      if "Gender" in df.columns:
            gender_counts = df["Gender"].value_counts().reset_index()
            gender_counts.columns = ["Gender", "Count"]
            fig_gender = px.bar(gender_counts, x="Gender", y="Count", color="Gender", text_auto=True, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_gender, use_container_width=True)
    with t2:
    

   
        st.subheader("Age Distribution")
        if "AGE" in df.columns and "Class Label" in df.columns:
            fig_age = px.histogram(df, x="AGE", nbins=20, color="Class Label",barmode="overlay", color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig_age, use_container_width=True)

    
        st.subheader("BMI Distribution")
        if "BMI" in df.columns and "Class Label" in df.columns:
            fig_bmi = px.histogram(df, x="BMI", nbins=20, color="Class Label",barmode="overlay", color_discrete_sequence=px.colors.qualitative.Safe)
            st.plotly_chart(fig_bmi, use_container_width=True)
    with t3:
     
        st.subheader("HbA1c by Class")
        if "HbA1c" in df.columns and "Class Label" in df.columns:
            fig_hba1c = px.box(df, x="Class Label", y="HbA1c", color="Class Label", color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_hba1c, use_container_width=True)

   
        st.subheader("HbA1c vs BMI")
        if {"BMI", "HbA1c", "Class Label"}.issubset(df.columns):
            hover_cols = [col for col in ["Gender", "Chol", "TG", "LDL", "HDL"] if col in df.columns]
            fig_scatter = px.scatter(df, x="BMI", y="HbA1c", color="Class Label",size="AGE" if "AGE" in df.columns else None,hover_data=hover_cols,color_discrete_sequence=px.colors.qualitative.Dark24)
            st.plotly_chart(fig_scatter, use_container_width=True)
    with t4:
        st.subheader("Lipid Profile Comparison")
        lipid_cols = ["Chol", "TG", "HDL", "LDL", "VLDL"]
        available_lipid_cols = [col for col in lipid_cols if col in df.columns]

        if available_lipid_cols and "Class Label" in df.columns:
          lipid_means = df.groupby("Class Label")[available_lipid_cols].mean().reset_index()
          lipid_long = lipid_means.melt(id_vars="Class Label", var_name="Marker", value_name="Average Value")

          fig_lipid = px.bar(lipid_long, x="Marker", y="Average Value", color="Class Label",barmode="group", color_discrete_sequence=px.colors.qualitative.Prism)
          st.plotly_chart(fig_lipid, use_container_width=True)

          st.subheader("Correlation Heatmap")
          numeric_cols = ["AGE", "Urea", "Cr", "HbA1c", "Chol", "TG", "HDL", "LDL", "VLDL", "BMI"]
          heatmap_cols = [col for col in numeric_cols if col in df.columns]

        if len(heatmap_cols) > 1:
          corr = df[heatmap_cols].corr()
          fig, ax = plt.subplots(figsize=(10, 6))
          sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
          st.pyplot(fig)

elif opt=="💡Cleaning & Processing":
  t1,t2=st.tabs(["Duplicates & records","Satistical & class distribution"])
  with t1:
      
      st.subheader("📍 Missing Values")
      st.write(df.isnull().sum())
      st.subheader("Duplicate Records")
      st.write(df.duplicated().sum())
      st.subheader("🪄 Cleaned Dataset")
      df = df.drop_duplicates()
      st.dataframe(df.head(20))

  with t2:    
       st.subheader("🔵 Summary Statistics")
       st.write(df.describe())
       st.subheader("🟣 Class Distribution")
       st.bar_chart(df['CLASS'].value_counts())

elif opt=="🔎 Insights":
    
        st.subheader("Class Distribution")
        class_counts = df['CLASS'].value_counts(normalize=True) * 100
        st.write(class_counts.round(2))
        st.write(f"Most patients are {class_counts.idxmax()} ({class_counts.max():.2f}%).")

        
        st.subheader("Age-Based Insights")
        avg_age = df.groupby("CLASS")["AGE"].mean()
        st.write(avg_age)
        st.write("Diabetic patients tend to be older compared to non-diabetic.")

        
        st.subheader("Gender Insights")
        gender_class = df.groupby(["Gender","CLASS"]).size().unstack(fill_value=0)
        st.write(gender_class)
        st.write("Shows diabetes distribution across male and female patients.")

        
        st.subheader("Biochemical Parameter Insights")
        bio_means = df.groupby("CLASS")[["HbA1c","BMI","Chol","LDL"]].mean()
        st.write(bio_means)
        st.write("Diabetic patients have higher HbA1c, BMI, and LDL on average.")

    
        st.subheader("Correlation Insights")
        corr = df[["HbA1c","BMI","LDL","Urea","Cr"]].corr()
        st.write(corr)
        st.write("HbA1c correlates positively with BMI and LDL.")

        
        st.subheader("Risk Factor Insights")
        high_risk = df[(df["HbA1c"] > 6.5) & (df["BMI"] > 30)]
        st.write(f"Patients at highest risk (HbA1c > 6.5 and BMI > 30): {len(high_risk)}")

elif opt =="✏️ About" :
    st.subheader("📘 About Project")
    st.write("""
    This project is a **Diabetes Data Analysis Dashboard** built using Python and Streamlit.
    
    ### Purpose
    The goal is to analyze patient health data and visualize patterns related to diabetes.

    ### Dataset
    The dataset includes patient details such as Age, Gender, HbA1c, BMI, Cholesterol, LDL, HDL, and Class (N = Non-diabetic, P = Prediabetic, Y = Diabetic).

    ### Tools & Libraries
    - **Pandas** for data handling
    - **Streamlit** for interactive dashboard
    - **Plotly, Seaborn, Matplotlib** for visualizations

    ### Features
    - Upload and preview dataset
    - Data cleaning and processing
    - Graphs: Heatmap, Bar chart, Sunburst, Pie chart, Boxplot
    - Insights section with key findings

    ### Outcomes
    - Identify risk factors (high HbA1c, BMI, cholesterol)
    - Show age and gender trends
    - Provide correlations between health parameters """)
