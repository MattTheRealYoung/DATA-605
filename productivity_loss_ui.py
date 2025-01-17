import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import smtplib

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

# Define the send email function
def send_email(sender_email, password):
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Email content
        subject = "Productivity loss enquire"
        body = "I am interested in the productivity loss, and like to know more about the reduce of productivity loss"
        message = f"Subject: {subject}\n\n{body}"

        # Connect to Gmail SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        st.success(f"Email sent successfully to {receiver_email}!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

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
st.write("Enter gmail credentials below:")
sender_email = st.text_input("Sender Email")
password = st.text_input("Password", type="password")
receiver_email = st.text_input("Receiver Email", "rhofmans@eragroup.com")

# Button logic
if st.button("Contact ERA Group"):
    if sender_email and password and receiver_email:
        send_email(sender_email, password, receiver_email)
    else:
        st.error("Please fill in all fields.")

