import streamlit as st
import mysql.connector
import random
import time
from faker import Faker
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from google.generativeai import GenerativeModel

# Initialize Streamlit app
st.set_page_config(page_title="Crop Management System", layout="wide")
st.title("🌾 Crop Management System")

# Database connection
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Welcome@2020",
        database="crop_management_system"
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS crops (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      crop_name VARCHAR(255),
                      planting_date DATE,
                      harvest_date DATE,
                      growth_stage VARCHAR(255),
                      pest_control_measures TEXT,
                      yield_prediction VARCHAR(255))''')
    conn.commit()
    return conn

conn = init_db()

# Sidebar options
st.sidebar.header("Options")
menu = st.sidebar.radio("Select Option", ["Add Crop", "Generate Random Data", "View Database", "Dashboard"])

# User input form
def add_crop():
    st.subheader("🌱 Add New Crop Record")
    with st.form("crop_form"):
        crop_name = st.text_input("Crop Name")
        planting_date = st.date_input("Planting Date")
        harvest_date = st.date_input("Harvest Date")
        growth_stage = st.selectbox("Growth Stage", ["Seedling", "Vegetative", "Flowering", "Maturity"])
        pest_control_measures = st.text_area("Pest Control Measures")
        yield_prediction = st.text_input("Yield Prediction (in tons)")
        submit = st.form_submit_button("Submit", help="Click to add crop record")
        
        if submit:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Welcome@2020",
                database="crop_management_system"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO crops (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction) VALUES (%s, %s, %s, %s, %s, %s)",
                           (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction))
            conn.commit()
            st.success("Crop record added successfully!")

# Display Database Table
def view_database():
    st.subheader("📋 Crop Records")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Welcome@2020",
        database="crop_management_system"
    )
    df = pd.read_sql("SELECT * FROM crops", conn)
    st.dataframe(df, width=1000)

# Generate Random Data
def generate_random_data():
    st.subheader("🔄 Generate Random Crop Data")
    fake = Faker()
    num_records = st.selectbox("Select number of records to generate", [100, 1000, 10000, 100000, 1000000, 10000000, 100000000])
    if st.button("Generate Records", help="Click to insert random records"):
        progress_bar = st.progress(0)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Welcome@2020",
            database="crop_management_system"
        )
        cursor = conn.cursor()
        for i in range(num_records):
            crop_name = random.choice(["Wheat", "Rice", "Corn", "Barley", "Soybean", "Cotton", "Sugarcane", "Potato"])
            planting_date = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
            harvest_date = (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
            growth_stage = random.choice(["Seedling", "Vegetative", "Flowering", "Maturity"])
            pest_control_measures = fake.sentence()
            yield_prediction = str(round(random.uniform(1.0, 10.0), 2))
            cursor.execute("INSERT INTO crops (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction) VALUES (%s, %s, %s, %s, %s, %s)",
                           (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction))
            conn.commit()
            if (i + 1) % (num_records // 100) == 0:
                progress_bar.progress((i+1) / num_records)
        st.success(f"{num_records} random records added successfully!")

# Dashboard
def dashboard():
    st.subheader("📊 Crop Data Dashboard")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Welcome@2020",
        database="crop_management_system"
    )
    df = pd.read_sql("SELECT * FROM crops", conn)
    if df.empty:
        st.warning("No data available.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Growth Stage Distribution")
        growth_stage_count = df['growth_stage'].value_counts()
        fig, ax = plt.subplots()
        growth_stage_count.plot(kind='bar', color=['skyblue', 'green', 'orange', 'red'], ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.write("### Yield Prediction Distribution")
        df['yield_prediction'] = pd.to_numeric(df['yield_prediction'], errors='coerce')
        fig, ax = plt.subplots()
        df['yield_prediction'].hist(bins=10, color='purple', ax=ax)
        st.pyplot(fig)

# Main execution
if menu == "Add Crop":
    add_crop()
elif menu == "Generate Random Data":
    generate_random_data()
elif menu == "View Database":
    view_database()
elif menu == "Dashboard":
    dashboard()

st.sidebar.markdown("---")
st.sidebar.markdown("<small>Developed by Anushka Gunjal 🚀</small>", unsafe_allow_html=True)
