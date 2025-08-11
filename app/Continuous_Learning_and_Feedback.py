import streamlit as st
import pandas as pd
import os
import sys
import datetime
import calendar

# Set up the root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# Import custom modules
from Continuous_learning_and_feedback.feedback import send_feedback_session_invitation
from Continuous_learning_and_feedback.alert import send_alert



def display_alert_meter(avg_rating, negative_feedback_count):
    with st.expander("**Live Feedback Monitoring and Alert Meter**", expanded=False):
        rating_threshold = 3.5
        negative_feedback_threshold = 20

        # Calculate percentages for the alert meter
        rating_percentage = (avg_rating / rating_threshold) 
        negative_feedback_percentage = (negative_feedback_count / negative_feedback_threshold) 

        st.subheader("Alert Meter")
        col1, col2 = st.columns(2)

        with col1:
            st.progress(rating_percentage, text=f"Avg. Rating: {avg_rating:.2f}")
        with col2:
            st.progress(negative_feedback_percentage, text=f"Negative Feedback: {negative_feedback_count}/{negative_feedback_threshold}")

        # Display warnings if thresholds are met
        if rating_percentage >= 1.0 or negative_feedback_percentage >= 0.9:
            st.warning("The system is approaching the alert threshold. Please review the user feedback.")
            send_alert(avg_rating, rating_threshold, negative_feedback_count, negative_feedback_threshold)
        else:
            st.success("The system is performing well based on the user feedback.")
        
        st.markdown("**Note:** When the alert meter bars get full, automatic email alert reports will be sent to the technical lead to resolve the issue.")

def continuous_learning_and_feedback():
    st.title("Continuous Learning and Feedback")
    st.text("Explore all the options below:")

    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Feedback.csv')
    feedback_data = pd.read_csv(data_file_path)

    avg_rating = feedback_data["Feedback Rating"].mean()
    negative_feedback_count = len(feedback_data[feedback_data["Feedback Rating"] < 3])

    display_alert_meter(avg_rating, negative_feedback_count)

    # User Feedback Mechanism
    with st.expander("**Provide Feedback**", expanded=False):
        feedback_form = st.form(key="feedback_form")
        feedback_type = feedback_form.selectbox("Select Feedback Type", ["Plant Leaf Disease Identification", "Responsiveness", "Stability", "Authentication","Overall"])
        feedback_rating = feedback_form.slider("Rate the accuracy and usefulness of the system's output", min_value=1, max_value=5, value=3)
        feedback_comments = feedback_form.text_area("Additional Comments")

        # Check if the submit button was clicked
        submit_feedback = feedback_form.form_submit_button("Submit Feedback")

        if submit_feedback:
            # Data validation: Ensure comments are not empty
            if feedback_comments.strip() == "":
                st.error("Please provide comments before submitting feedback.")
            else:
                # Collect and store the feedback data
                feedback_data = {
                    "Feedback Type": feedback_type,
                    "Feedback Rating": feedback_rating,
                    "Feedback Comments": feedback_comments
                }
                store_feedback_data(feedback_data)
                st.success("Thank you for your feedback!")

    # Knowledge Capture and Documentation
    with st.expander("**Knowledge Base**", expanded=False):   
        st.write("Insights and lessons learned from the continuous feedback process are documented here.")
        display_knowledge_base(feedback_data)

    # Collaborative Learning
    with st.expander("**Feedback Sessions Invitation**", expanded=False):
        organize_feedback_sessions()

def store_feedback_data(feedback_data):
    feedback_file_path = os.path.join(root_dir, 'Component_datasets', 'Feedback.csv')

    # Check if the file path exists
    os.makedirs(os.path.dirname(feedback_file_path), exist_ok=True)

    try:
        feedback_df = pd.read_csv(feedback_file_path)
        new_feedback_df = pd.DataFrame([feedback_data])
        feedback_df = pd.concat([feedback_df, new_feedback_df], ignore_index=True)
        feedback_df.to_csv(feedback_file_path, index=False)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        feedback_df = pd.DataFrame([feedback_data])
        feedback_df.to_csv(feedback_file_path, index=False)
        

def display_knowledge_base(feedback_data):
    # If feedback_data is a dictionary, convert it to a DataFrame
    if isinstance(feedback_data, dict):
        feedback_data = pd.DataFrame([feedback_data])

    # Check if the DataFrame is empty before displaying
    if not feedback_data.empty:
        st.table(feedback_data)
    else:
        st.info("No feedback data available.")


def organize_feedback_sessions():
    st.markdown("### Organize Feedback Sessions")

    # Get user input for feedback session details
    session_date = st.date_input("Select Feedback Session Date")
    session_time = st.time_input("Select Feedback Session Time")

    # Display stakeholder management interface
    st.subheader("Manage Stakeholders")
    stakeholders = get_stakeholder_contact_info()
    st.dataframe(stakeholders)

    if "stakeholders" not in st.session_state:
        st.session_state.stakeholders = stakeholders

    # Allow user to add, edit, or remove stakeholders
    new_stakeholder_name = st.text_input("Add New Stakeholder Name")
    new_stakeholder_position = st.text_input("Add New Stakeholder's Position")
    new_stakeholder_email = st.text_input("Add New Stakeholder Email")
    if st.button("Add Stakeholder"):
        st.session_state.stakeholders.append({"name": new_stakeholder_name, "Position": new_stakeholder_position, "email": new_stakeholder_email})
        st.dataframe(st.session_state.stakeholders)

    # Allow user to select stakeholders to invite
    selected_stakeholders = st.multiselect("Select Stakeholders to Invite", [s["name"] for s in st.session_state.stakeholders])

    st.markdown("**Note**: After selecting the stakeholders for invitation, click outside the dropdown menu or press the 'Esc' key to close the dropdown.")
    
    # Send feedback session invitation
    if st.button("Send Invitation mail"):
        # Initialize an empty list to collect email addresses
        email_addresses = []

        # Iterate over each stakeholder dictionary
        for stakeholder in st.session_state.stakeholders:
            # Extract the email address from the current stakeholder dictionary
            email_addresses.append(stakeholder["email"])

        send_feedback_session_invitation(session_date, session_time, email_addresses)

def get_next_feedback_session_date():
    # Set the feedback session to be held on the first Monday of the month
    target_weekday = calendar.MONDAY
    now = datetime.datetime.now()
    days_until_target = (target_weekday - now.weekday()) % 7
    next_session_date = now + datetime.timedelta(days=days_until_target)
    return next_session_date

def get_stakeholder_contact_info():
    # Retrieve the list of stakeholders and their contact information (e.g., from a database or a CSV file)
    stakeholders = [
        {"name": "Utkrista Acharya",  "Position": "Technical Lead", "email": "autkrista24@britishinternationalcollege.edu.np"},
    ]
    return stakeholders

def main():
    continuous_learning_and_feedback()

if __name__ == "__main__":
    main()