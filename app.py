import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load trained model (you need to save your model as 'rf_model.pkl')
model = joblib.load("rf_model.pkl")

st.set_page_config(page_title="Forest Cover Type Predictor", layout="centered")

st.title("🌲 Forest Cover Type Prediction App")
st.markdown("Enter the environmental features to predict forest cover type")

# Input features
elevation = st.number_input("Elevation (in meters)", min_value=1800, max_value=4000, value=2500)
aspect = st.slider("Aspect (degrees)", 0, 360, 45)
slope = st.slider("Slope (degrees)", 0, 60, 10)

h_dist_hydro = st.slider("Horizontal Distance to Hydrology", 0, 5000, 100)
v_dist_hydro = st.slider("Vertical Distance to Hydrology", -500, 500, 50)
h_dist_road = st.slider("Horizontal Distance to Roadways", 0, 7000, 1000)
h_dist_fire = st.slider("Horizontal Distance to Fire Points", 0, 7000, 1200)

hillshade_9am = st.slider("Hillshade 9am", 0, 255, 150)
hillshade_noon = st.slider("Hillshade Noon", 0, 255, 200)
hillshade_3pm = st.slider("Hillshade 3pm", 0, 255, 120)

# Wilderness Area & Soil Type (simplified)
wilderness_area = st.selectbox("Wilderness Area", ['Area1', 'Area2', 'Area3', 'Area4'])
soil_type = st.selectbox("Soil Type", ['Type1', 'Type2', 'Type3', 'Type4', 'Type5'])

# Convert categorical selections to one-hot encoding
wilderness_cols = ['Wilderness_Area1', 'Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4']
soil_cols = [f'Soil_Type{i}' for i in range(1, 41)]

wilderness_onehot = [1 if f'Wilderness_Area{i}' == f'Wilderness_Area{wilderness_area[-1]}' else 0 for i in range(1, 5)]
soil_onehot = [1 if f'Soil_Type{i}' == f'Soil_Type{soil_type[4:]}' else 0 for i in range(1, 41)]

# Combine all inputs
input_data = [
    elevation, aspect, slope, h_dist_hydro, v_dist_hydro,
    h_dist_road, hillshade_9am, hillshade_noon, hillshade_3pm,
    h_dist_fire
] + wilderness_onehot + soil_onehot

input_df = pd.DataFrame([input_data])

# Predict
if st.button("Predict Cover Type"):
    prediction = model.predict(input_df)[0]
    st.success(f"🌲 Predicted Cover Type: **{prediction}**")
