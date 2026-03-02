import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Load model
model = pickle.load(open("hospital_model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

st.set_page_config(page_title="Hospital Resource Management", layout="centered")

st.title("🏥 AI-Based Hospital Resource Optimization System")

st.write("Predict Patient Count and Resource Requirements")

st.subheader("Enter Hospital Details")

OPD = st.number_input("OPD Admissions", min_value=0)
IPD = st.number_input("IPD Admissions", min_value=0)
Emergency = st.number_input("Emergency Admissions", min_value=0)
Occupancy = st.number_input("Bed Occupancy Rate (%)", min_value=0.0)
Doctors = st.number_input("Doctors Available", min_value=0)
Nurses = st.number_input("Nurses Available", min_value=0)
Medicine = st.number_input("Medicine Consumption Units", min_value=0)

if st.button("Predict"):

    input_data = {
        "OPD_Admissions": OPD,
        "IPD_Admissions": IPD,
        "Emergency_Admissions": Emergency,
        "Bed_Occupancy_Rate_%": Occupancy,
        "Doctors_Available": Doctors,
        "Nurses_Available": Nurses,
        "Medicine_Consumption_Units": Medicine,
        "Total_Staff": Doctors + Nurses
    }

    input_df = pd.DataFrame([input_data])
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    # 1️⃣ Predict Patient Count
    patient_prediction = int(model.predict(input_df)[0])

    st.subheader("📊 Prediction Results")
    st.success(f"Predicted Total Patient Count: {patient_prediction}")

    # 2️⃣ Bed Requirement
    if Occupancy > 85:
        st.error("⚠ Additional Beds Required!")
    else:
        st.success("✅ Bed Capacity is Sufficient.")

    # 3️⃣ Doctor Requirement
    required_doctors = int(patient_prediction / 20)
    st.write(f"Estimated Doctors Required: {required_doctors}")

    if Doctors < required_doctors:
        st.error("⚠ Additional Doctors Required!")
    else:
        st.success("✅ Doctor Availability is Sufficient.")

    # 4️⃣ Nurse Requirement
    required_nurses = int(patient_prediction / 10)
    st.write(f"Estimated Nurses Required: {required_nurses}")

    if Nurses < required_nurses:
        st.error("⚠ Additional Nurses Required!")
    else:
        st.success("✅ Nurse Availability is Sufficient.")

    
    
