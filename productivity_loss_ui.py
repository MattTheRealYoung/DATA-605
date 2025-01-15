import streamlit as st
import pandas as pd
import numpy as np
import joblib
import webbrowser
import os

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Construct the relative path to the model file
model_path = os.path.join(current_dir, "models", "linear_regression_model.joblib")

# Load the pre-trained model
model = joblib.load(model_path)

# Set up the page
st.title("Productivity Loss Prediction Tool")

# Define user inputs
def user_input():
    sick_leave_hours = st.sidebar.number_input(
        "Total Sick Leave Hours", min_value=0, value=2000, step=1
    )
    total_hours_worked = st.sidebar.number_input(
        "Total Hours Worked", min_value=0, value = 22848, step = 1
    )
    turnover_month = st.sidebar.number_input(
        "Total Staff Leaving in Month", min_value=0, value=10, step=1
    )

    # Presenteeism input: distribution sliders
    st.markdown("### Presenteeism Distribution")
    slightly_affected = st.slider(
        "Slightly Affected Productivity (%)", min_value=0.0, max_value=1.0, value=0.2, step=0.01
    )
    significantly_affected = st.slider(
        "Significantly Affected Productivity (%)", min_value=0.0, max_value=1.0, value=0.1, step=0.01
    )

    # Productivity mapping
    st.markdown("### Presenteeism Productivity Mapping")
    slight_productivity = st.slider(
        "Productivity Retained (Slightly Affected)", min_value=0.0, max_value=1.0, value=0.8, step=0.01
    )
    significant_productivity = st.slider(
        "Productivity Retained (Significantly Affected)", min_value=0.0, max_value=1.0, value=0.5, step=0.01
    )

    # Calculate presenteeism productivity loss
    presenteeism_productivity_loss = total_hours_worked * slightly_affected * (1 - slight_productivity) * 32.6 + total_hours_worked * significantly_affected * (1 - significant_productivity) * 32.6

    st.markdown(
        f"**Productivity loss from Presenteeism**: ${presenteeism_productivity_loss:.2f}"
    )

    return sick_leave_hours, turnover_month, presenteeism_productivity_loss

# Gather inputs
sick_leave_hours, turnover_month, presenteeism_productivity_loss = user_input()

# Prepare prediction data
input_data = pd.DataFrame({
    'Total Sick Leave Hours': [sick_leave_hours],
    'Total Staff Leaving in Month': [turnover_month],
})

# Predict productivity loss using the model
predicted_loss = model.predict(input_data)[0] + presenteeism_productivity_loss

# Display results
st.subheader("Predicted Productivity Loss")
st.markdown(f"<h1 style='text-align: center; color: red;'>${predicted_loss:,.2f}</h1>", unsafe_allow_html=True)

# Add a button to call ERA
if st.button("Call ERA"):
    webbrowser.open("https://nz.eragroup.com/")
