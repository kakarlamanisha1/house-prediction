# app.py

import streamlit as st
import numpy as np
import pandas as pd 
import joblib

# Load the trained model
model = joblib.load('housing_price_model.pkl')

# Define all valid state_city combinations (based on your dataset)
state_city_list = sorted([
    'andhra pradesh_vijayawada', 'assam_guwahati', 'bihar_gaya', 'bihar_patna',
    'chhattisgarh_bilaspur', 'chhattisgarh_raipur', 'delhi_new delhi', 'delhi_dwarka',
    'gujarat_ahmedabad', 'gujarat_surat', 'haryana_faridabad', 'haryana_gurgaon',
    'jharkhand_jamshedpur', 'jharkhand_ranchi', 'karnataka_bangalore',
    'karnataka_mangalore', 'karnataka_mysore', 'kerala_kochi', 'kerala_trivandrum',
    'madhya pradesh_bhopal', 'madhya pradesh_indore', 'maharashtra_mumbai',
    'maharashtra_pune', 'odisha_bhubaneswar', 'odisha_cuttack',
    'punjab_amritsar', 'punjab_ludhiana', 'rajasthan_jaipur', 'rajasthan_jodhpur',
    'tamil nadu_chennai', 'tamil nadu_coimbatore', 'telangana_hyderabad',
    'telangana_warangal', 'uttar pradesh_lucknow', 'uttar pradesh_noida',
    'uttarakhand_dehradun', 'uttarakhand_haridwar', 'west bengal_durgapur',
    'west bengal_kolkata', 'west bengal_silchar'
])

# Streamlit UI
st.set_page_config(page_title="India Housing Price Predictor", layout="centered")
st.title("India Housing Price Predictor")
st.markdown("Fill in the property details below to estimate the housing price (in Lakhs):")

# --- Inputs ---
property_type = st.selectbox("Property Type", ["Apartment", "Independent House", "Villa"])
bhk = st.number_input("BHK", min_value=1, max_value=10, step=1)
furnished_status = st.selectbox("Furnished Status", ["Unfurnished", "Semi-furnished", "Furnished"])
floor_no = st.number_input("Floor Number", min_value=0, max_value=100)
total_floors = st.number_input("Total Floors", min_value=1, max_value=100)
age_of_property = st.number_input("Age of Property (in years)", min_value=0, max_value=100)
transport_access = st.selectbox("Public Transport Accessibility", ["Low", "Medium", "High"])
parking = st.selectbox("Parking Space", ["Yes", "No"])
security = st.selectbox("Security", ["Yes", "No"])
owner_type = st.selectbox("Owner Type", ["Owner", "Builder", "Broker"])
availability = st.selectbox("Availability Status", ["Ready_to_Move", "Under_Construction"])
facing = st.selectbox("Facing", ["East", "West", "North", "South"])
state_city = st.selectbox("State & City", state_city_list)
price_for_area = st.number_input("Total Area Price (Size × Price per SqFt)", min_value=0.0)
school_and_hospital = st.number_input("Nearby Schools + Hospitals (combined count)", min_value=0, max_value=50)

# --- Amenities ---
st.markdown("### Select Available Amenities:")        
clubhouse = st.checkbox("🏘️ Clubhouse")
garden = st.checkbox("🌳 Garden")
gym = st.checkbox("🏋️ Gym")
playground = st.checkbox("🛝 Playground")
pool = st.checkbox("🏊 Pool")

# --- Prepare Input Data ---
input_data = pd.DataFrame([[
    property_type, bhk, furnished_status, floor_no, total_floors, age_of_property,
    transport_access, parking, security, owner_type, availability, price_for_area,
    school_and_hospital, state_city, facing,
    int(clubhouse), int(garden), int(gym), int(playground), int(pool)
]], columns=[
    'Property_Type', 'BHK', 'Furnished_Status', 'Floor_No', 'Total_Floors', 'Age_of_Property',
    'Public_Transport_Accessibility', 'Parking_Space', 'Security', 'Owner_Type', 'Availability_Status',
    'Price_for_Area', 'School_and_Hospitals', 'State_City', 'Facing',
    'clubhouse', 'garden', 'gym', 'playground', 'pool'
])

# --- Predict --- 
if st.button(" Predict Price"):
    try:
        prediction = model.predict(input_data)[0]
        st.success(f" **Estimated Price: ₹ {prediction:.2f} Lakhs**")
    except Exception as e:
        st.error(f" Prediction failed: {str(e)}")
